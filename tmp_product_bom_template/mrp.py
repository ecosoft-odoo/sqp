# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time

from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from dateutil.relativedelta import relativedelta
import netsvc
from osv import osv, fields
from tools.translate import _


class mrp_production_product_line(osv.osv):

    _inherit = 'mrp.production.product.line'

    # Method override
    def _get_product_line(self, cr, uid, ids, context=None):
        """ return all product_line for the same updated product """
        product_line_ids = []
        for product in self.browse(cr, uid, ids, context=context):
            product_line_ids += self.pool.get('mrp.production.product.line').search(cr, uid, [('product_id','=',product.id)], context=context)
        return product_line_ids

    # Method override
    def _get_machine_setup_params(self, cr, uid, ids, field_name, arg, context=None):
        setup_detail_obj = self.pool.get('mrp.machine.setup.master.line')
        res = {}
        for product_line in self.browse(cr, uid, ids, context=context):
            res[product_line.id] = {
                'W': False, 'L': False, 'T': False,
                'line1_inject1': False, 'line1_inject2': False, 'line2_inject1': False, 'line2_inject2': False, 
                'line3_inject1': False, 'line3_inject2': False, 'line4_inject1': False, 'line4_inject2': False, 
                'line5_inject1': False, 'line5_inject2': False, 
                'line1_settime': False, 'line2_settime': False, 'line3_settime': False, 
                'line4_settime': False, 'line5_settime': False, 
                'cut_area': False, 'remark': False,
            }
            product = product_line.product_id
            # For all Machine Lines, these values are common.
            res[product_line.id] = {
                'W': product.W,
                'L': product.L,
                'T': product.T.value,
                'cut_area': product.cut_area,
                'remark': product.remark,
            }
            # Loop through each machine (1-5) to calculate injection and set time.
            master_ids = setup_detail_obj.search(cr, uid, [('thickness','=', product.T.id)])
            if master_ids:
                W = product.W or 0.0
                L = product.L or 0.0
                T = product.T.value or 0.0                
                sets = setup_detail_obj.browse(cr, uid, master_ids)
                # For each machine (line1, line2, ..., line5), calculate values
                if product_line.is_special:  # kittiu: Additional Calculation
                    for set in sets:
                        factor = set.flowrate or (set.correction_factor and 1/set.correction_factor) or 0.0
                        res[product_line.id].update({
                            set.machine_id.name + '_inject1': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_1/100)+1)/factor - (50*L*T/1000000000)*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                            set.machine_id.name + '_inject2': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_2/100)+1)/factor - (50*L*T/1000000000)*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                            set.machine_id.name + '_settime': set.settime,
                        })
                else:  # --
                    for set in sets:
                        factor = set.flowrate or (set.correction_factor and 1/set.correction_factor) or 0.0
                        res[product_line.id].update({
                            set.machine_id.name + '_inject1': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                            set.machine_id.name + '_inject2': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_2/100)+1)/factor or 0.0,
                            set.machine_id.name + '_settime': set.settime,
                        })
        return res

    _columns = {
        'W':fields.function(_get_machine_setup_params, string="Width (W)", type="float", multi="all",                 
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'L':fields.function(_get_machine_setup_params, string="Length (L)", type="float", multi="all",       
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'T':fields.function(_get_machine_setup_params, string="Thick (T)", type="float", multi="all",                  
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line1_inject1':fields.function(_get_machine_setup_params, string="L1 (am)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line1_inject2':fields.function(_get_machine_setup_params, string="L1 (pm)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line2_inject1':fields.function(_get_machine_setup_params, string="L2 (am)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line2_inject2':fields.function(_get_machine_setup_params, string="L2 (pm)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line3_inject1':fields.function(_get_machine_setup_params, string="L3 (am)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line3_inject2':fields.function(_get_machine_setup_params, string="L3 (pm)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line4_inject1':fields.function(_get_machine_setup_params, string="L4 (am)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line4_inject2':fields.function(_get_machine_setup_params, string="L4 (pm)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line5_inject1':fields.function(_get_machine_setup_params, string="L5 (kg) (am)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line5_inject2':fields.function(_get_machine_setup_params, string="L5 (kg) (pm)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line1_settime':fields.function(_get_machine_setup_params, string="Set Time (L1)", type="float", multi="all",                  
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line2_settime':fields.function(_get_machine_setup_params, string="Set Time (L2)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line3_settime':fields.function(_get_machine_setup_params, string="Set Time (L3)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line4_settime':fields.function(_get_machine_setup_params, string="Set Time (L4)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line5_settime':fields.function(_get_machine_setup_params, string="Set Time (L5)", type="float", multi="all",                   
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'cut_area':fields.function(_get_machine_setup_params, string="Cut Area (sqm)", type="float", multi="all", 
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),        
        'remark':fields.function(_get_machine_setup_params, string="Remark", type="char", multi="all", 
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'is_special': fields.boolean('Special', readonly='False', help='Selection this option will re-calculate injection rate with formula = <exiting> - (50*L*T/1000000000)*density*((overpack_1/100)+1)/factor')
    }

    def toggle_special_product(self, cr, uid, ids, context=None):
        results = self.read(cr, uid, ids, ['is_special'], context=context)
        for result in results:
            if result['is_special']:
                self.write(cr, uid, [result['id']], {'is_special': False}, context=context)
            else:
                self.write(cr, uid, [result['id']], {'is_special': True}, context=context)
        return True

mrp_production_product_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
