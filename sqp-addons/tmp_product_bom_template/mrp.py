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
                'line5_inject1': False, 'line5_inject2': False, 'line_pir1_pir': False, 'line_pir1_pu': False,
                'line_pir2_pir': False, 'line_pir2_pu': False, 'line_pir3_pir': False, 'line_pir3_pu': False,
                'line1_settime': False, 'line2_settime': False, 'line3_settime': False,
                'line4_settime': False, 'line5_settime': False, 'line_pir1_pir_settime': False,
                'line_pir2_pir_settime': False, 'line_pir3_pir_settime': False,
                'cut_area': False, 'remark': False,
                # For continuous line
                'line_slipjoint_pir': False, 'line_slipjoint_pu': False, 'line_secretjoint_pir': False, 'line_secretjoint_pu': False,
                'line_roofjoint_pir': False, 'line_roofjoint_pu': False, 'line_board_pir': False, 'line_board_pu': False,
                'line_slipjoint_pir_settime': False, 'line_slipjoint_pu_settime': False, 'line_secretjoint_pir_settime': False, 'line_secretjoint_pu_settime': False,
                'line_roofjoint_pir_settime': False, 'line_roofjoint_pu_settime': False, 'line_board_pir_settime': False, 'line_board_pu_settime': False,
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
                # For each machine (line1, line2, ..., line_7_pu), calculate values
                # if product_line.is_special:  # kittiu: Additional Calculation
                #     for set in sets:
                #         factor = set.flowrate or (set.correction_factor and 1/set.correction_factor) or 0.0
                #         res[product_line.id].update({
                #             set.machine_id.name + '_inject1': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_1/100)+1)/factor - (50*L*T/1000000000)*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                #             set.machine_id.name + '_inject2': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_2/100)+1)/factor - (50*L*T/1000000000)*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                #             set.machine_id.name + '_settime': set.settime,
                #         })
                # else:  # --
                #     for set in sets:
                #         factor = set.flowrate or (set.correction_factor and 1/set.correction_factor) or 0.0
                #         res[product_line.id].update({
                #             set.machine_id.name + '_inject1': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                #             set.machine_id.name + '_inject2': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_2/100)+1)/factor or 0.0,
                #             set.machine_id.name + '_settime': set.settime,
                #         })

                # Not used 20/10/2020
                # area = W*L/1000000-product.cut_area
                # for set in sets:
                #     if set.machine_id.name in ['line1', 'line2', 'line3', 'line4']:
                #         res[product_line.id].update({
                #             set.machine_id.name + '_inject1': round(round(area*T/1000*set.density,2)*((set.overpack_1/100)+1)/set.flowrate,2) or 0.0,
                #             set.machine_id.name + '_inject2': round(round(area*T/1000*set.density,2)*((set.overpack_1/100)+1)/set.flowrate,2) or 0.0,
                #             set.machine_id.name + '_settime': set.settime,
                #         })
                #     else:
                #         res[product_line.id].update({
                #             set.machine_id.name: round(round(area*T/1000*set.density,2)*((set.overpack_1/100)+1)/set.flowrate,2) or 0.0,
                #             set.machine_id.name + '_settime': set.settime,
                #         })

                # Customization by Pod (20/10/2020)
                area = W*L/1000000-product.cut_area
                for set in sets:
                    flowrate = self._get_val(cr, uid, product_line.id, set.str_flowrate, W, L, context=context)
                    density = self._get_val(cr, uid, product_line.id, set.str_density, W, L, context=context)
                    overpack_1 = self._get_val(cr, uid, product_line.id, set.str_overpack_1, W, L, context=context)
                    settime = self._get_val(cr, uid, product_line.id, set.str_settime, W, L, context=context)
                    if not product_line.production_id.is_continuous_line:
                        if set.machine_id.name in ['line1', 'line2', 'line3', 'line4', 'line5']:
                            res[product_line.id].update({
                                set.machine_id.name + '_inject1': round(round(area*T/1000*density,2)*((overpack_1/100)+1)/flowrate,2) or 0.0,
                                set.machine_id.name + '_inject2': round(round(area*T/1000*density,2)*((overpack_1/100)+1)/flowrate,2) or 0.0,
                                set.machine_id.name + '_settime': settime,
                            })
                        elif set.machine_id.name in ['line_pir1_pir', 'line_pir1_pu', 'line_pir2_pir', 'line_pir2_pu', 'line_pir3_pir', 'line_pir3_pu']:
                            res[product_line.id].update({
                                set.machine_id.name: round(round(area*T/1000*density,2)*((overpack_1/100)+1)/flowrate,2) or 0.0,
                                set.machine_id.name + '_settime': settime,
                            })
                    else:
                        if any([m in set.machine_id.name for m in ['line_slipjoint', 'line_secretjoint', 'line_roofjoint', 'line_board']]):
                            if product.bom_template_id == set.machine_id.bom_template_id and product.mat_insulation_choices.code.lower() in set.machine_id.name:
                                res[product_line.id].update({
                                    set.machine_id.name: round(W * T * density * settime / 1000000, 2),
                                    set.machine_id.name + "_settime": settime,
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
        'line_pir1_pir':fields.function(_get_machine_setup_params, string="L1 (PIR) (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir1_pu':fields.function(_get_machine_setup_params, string="L1 (PIR)(PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir2_pir':fields.function(_get_machine_setup_params, string="L2 (PIR) (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir2_pu':fields.function(_get_machine_setup_params, string="L2 (PIR) (PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir3_pir':fields.function(_get_machine_setup_params, string="L3 (PIR) (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir3_pu':fields.function(_get_machine_setup_params, string="L3 (PIR) (PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_slipjoint_pir':fields.function(_get_machine_setup_params, string="Slip Joint (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_slipjoint_pu':fields.function(_get_machine_setup_params, string="Slip Joint (PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_secretjoint_pir':fields.function(_get_machine_setup_params, string="Secret Joint (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_secretjoint_pu':fields.function(_get_machine_setup_params, string="Secret Joint (PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_roofjoint_pir':fields.function(_get_machine_setup_params, string="Roof Joint (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_roofjoint_pu':fields.function(_get_machine_setup_params, string="Roof Joint (PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_board_pir':fields.function(_get_machine_setup_params, string="Board (PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_board_pu':fields.function(_get_machine_setup_params, string="Board (PU)", type="float", multi="all",
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
        'line_pir1_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR1)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir2_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR2)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir3_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR3)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir1_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR1)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir2_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR2)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_pir3_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (LINE PIR3)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_slipjoint_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (Slip Joint PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_slipjoint_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (Slip Joint PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_secretjoint_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (Secret Joint PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_secretjoint_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (Secret Joint PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_roofjoint_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (Roof Joint PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_roofjoint_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (Roof Joint PU)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_board_pir_settime':fields.function(_get_machine_setup_params, string="Set Time (Board PIR)", type="float", multi="all",
                store={
                   'mrp.production.product.line': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                   'product.product': (_get_product_line, ['W','L','T','bom_product_type','cut_area','remark'], 10)
                   }),
        'line_board_pu_settime':fields.function(_get_machine_setup_params, string="Set Time (Board PU)", type="float", multi="all",
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

    def _get_val(self, cr, uid, id, val, W, L, context=None):
        val = val.replace('W', str(W)).replace('L', str(L))
        result = eval(val)
        if not isinstance(result, (int, float)):
            raise osv.except_osv(
                _('Error!'),
                _('Can not compute sheduled products, '
                  'please check the machine setup master.'),
            )
        return float(result)

mrp_production_product_line()


class mrp_machine_setup_master(osv.osv):
    _inherit = 'mrp.machine.setup.master'
    _columns = {
        'name': fields.selection([('line1','Line 1'),
                                  ('line2','Line 2'),
                                  ('line3','Line 3'),
                                  ('line4','Line 4'),
                                  ('line5','Line 5'),
                                  ('line_pir1_pir','Line PIR1 (PIR)'),
                                  ('line_pir1_pu','Line PIR1 (PU)'),
                                  ('line_pir2_pir','Line PIR2 (PIR)'),
                                  ('line_pir2_pu','Line PIR2 (PU)'),
                                  ('line_pir3_pir','Line PIR3 (PIR)'),
                                  ('line_pir3_pu','Line PIR3 (PU)'),
                                  ('line_slipjoint_pir','Line Slip Joint (PIR)'),
                                  ('line_slipjoint_pu','Line Slip Joint (PU)'),
                                  ('line_secretjoint_pir','Line Secret Joint (PIR)'),
                                  ('line_secretjoint_pu','Line Secret Joint (PU)'),
                                  ('line_roofjoint_pir','Line Roof Joint (PIR)'),
                                  ('line_roofjoint_pu','Line Roof Joint (PU)'),
                                  ('line_board_pir','Line Board (PIR)'),
                                  ('line_board_pu','Line Board (PU)'),
                                     ],'Machine'),
    }

mrp_machine_setup_master()


class mrp_machine_setup_master_line(osv.osv):
    _inherit = 'mrp.machine.setup.master.line'
    _columns = {
        'str_flowrate': fields.char('Flowrate (kg/sec)', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
        'str_density': fields.char('Density (kg/m3)', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
        'str_correction_factor': fields.char('Correction Factor', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
        'str_overpack_1': fields.char('% Overpack (morning)', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
        'str_overpack_2': fields.char('% Overpack (afternoon)', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
        'str_settime': fields.char('Set Time', help="You can pass variable to this field \n 'W': Product's width \n 'L': Product's Length \n Ex: L > 1000 and 10 or 20"),
    }

    _defaults = {
        'str_flowrate': '0.000',
        'str_density': '0.00',
        'str_correction_factor': '0.00',
        'str_overpack_1': '0.00',
        'str_overpack_2': '0.00',
        'str_settime': '0.00',
    }

    def _check_machine_line(self, cr, uid, ids, context=None):
        fields = ['str_flowrate', 'str_density', 'str_correction_factor',
                  'str_overpack_1', 'str_overpack_2', 'str_settime']
        for record in self.browse(cr, uid, ids, context=context):
            for field in fields:
                result = False
                try:
                    # This can pass Width(W), Length(L) from the product.
                    val = record[field].replace(
                        'W', 'False').replace('L', 'False')
                    result = eval(val)
                except Exception:
                    raise osv.except_osv(
                        _('Error!'),
                        _('%s of %s is not correct.') % (
                            self._columns[field].string,
                            record.thickness.name))
                if result and not isinstance(result, (int, float)):
                    raise osv.except_osv(
                        _('Error!'),
                        _('%s of %s must be the number.' % (
                            self._columns[field].string,
                            record.thickness.name))
                    )
        return True

    _constraints = [
        (_check_machine_line, 'Machine setup is not correct.',
         ['str_flowrate', 'str_density', 'str_correction_factor',
          'str_overpack_1', 'str_overpack_2', 'str_settime'])
    ]

mrp_machine_setup_master_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
