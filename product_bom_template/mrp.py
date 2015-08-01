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

import netsvc
from osv import osv, fields
import decimal_precision as dp
from tools.translate import _

class mrp_bom(osv.osv):
    
    _inherit = "mrp.bom"
    _order = 'sequence, id'
    
    def _get_product_sequence(self, cr, uid, ids, name, arg, context=None):
        res = {}
        product_obj = self.pool.get('product.product')
        for product_line in self.browse(cr, uid, ids, context=context):
            result = product_obj.read(cr, uid, [product_line.product_id.id], ['sequence'])
            if result[0]['sequence']:
                res[product_line.id] = result[0]['sequence'] or 10000
        return res    
    _columns = {
        'sequence': fields.function(_get_product_sequence, string='Sequence', type='integer', store=True),
        'is_bom_template':fields.boolean('BOM Template'),
        'bom_template_type':fields.selection([
                                    # Not in this round ('standard','Standard'),
                                      ('formula','Formula')],'BOM Template Type'),
        'product_qty_formula': fields.char('Product Qty-Formula', size=512, required=False, help='Valid formula to calculate quantity, i.e., W*L*T'),
        'bom_lines_formula': fields.one2many('mrp.bom', 'bom_id', 'BoM Lines Formula'),
        # Naming Convention
        'new_name_format': fields.char('New Product Naming Format', size=256, help='Valid for to create new name for product created from this template'),
        # Required Parameters
        'bom_template_id':fields.boolean('BOM Template'),
        'bom_product_type':fields.selection([('panel','Panel'),
                                             ('door','Door'),
                                             ('window','Window'),],'BOM Product Type'),
        'W':fields.boolean('Width (W)'),
        'L':fields.boolean('length (L)'),
        # Options
        'T': fields.many2many('bom.choice.thick', string='Thick (T) Choices'),
        'mat_model_choices': fields.many2many('bom.choice.model', string='Model Choices'),
        'mat_joint_choices': fields.many2many('bom.choice.joint', string='Joint Choices'),
        'mat_inside_skin_choices': fields.many2many('bom.choice.skin', string='Inside Skin Choices'),
        'mat_outside_skin_choices': fields.many2many('bom.choice.skin', string='Outside Skin Choices'),
        'mat_insulation_choices': fields.many2many('bom.choice.insulation', string='Insulation Choices'),
        'mat_camlock_choices': fields.many2many('bom.choice.camlock', string='Camlock Choices'),
        'mat_window_choices': fields.many2many('bom.choice.window', string='Window Choices'),
    }
    
    _defaults = {
        'bom_template_id': True,
        'W': True,
        'L': True,
    }
    
    # A complete overwrite method??
    # Only for normal non Bom Template that this constraint should apply
    def _check_product(self, cr, uid, ids, context=None):
        all_prod = []
        boms = self.browse(cr, uid, ids, context=context)
        # kittiu
        parent_bom = boms[0]
        is_one_time_use = parent_bom.product_id.is_one_time_use
        # -- kittiu
        def check_bom(boms):
            res = True
            for bom in boms:
                # kittiu
                #if bom.product_id.id in all_prod:
                if ((bom.bom_id and not bom.bom_id.is_bom_template and not is_one_time_use) or not bom.bom_id) and bom.product_id.id in all_prod:    
                    res = res and False
                #-- kittiu
                all_prod.append(bom.product_id.id)
                lines = bom.bom_lines
                if lines:
                    res = res and check_bom([bom_id for bom_id in lines if bom_id not in boms])
            return res
        return check_bom(boms)    
    
    _constraints = [
        (_check_product, 'BoM line product should not be same as BoM product.', ['product_id']),
    ]
    
    def update_quantity_by_formula(self, cr, uid, object, line, bom, context=None):
        if context is None:
            context = {}
        for bom_line in bom['bom_lines_formula']:
            try:
                calc_qty = eval(bom_line[2]['product_qty_formula'], {'object': object, 'line': line})
            except Exception, e:
                raise osv.except_osv(_('BOM Formula Error!'), bom_line[2]['product_qty_formula'] + '\n\n' + str(e))
            bom_line[2]['name'] = bom_line[2]['name'].replace(' (copy)','')
            calc_qty = eval(bom_line[2]['product_qty_formula'], {'object': object, 'line': line})
            bom_line[2]['product_qty'] = calc_qty
            self.update_quantity_by_formula(cr, uid, object, line, bom_line[2], context=context)
        return True
    
    # Copy method that use specifically for BOM Formula
    def copy_bom_formula(self, cr, uid, id, object, line, default=None, context=None):
        
        if context is None: 
            context = {}
        context = context.copy()
        context['bom_formula'] = True
        data = False
        if context.get('bom_data', False):
            data = context.get('bom_data', False)
        else:
            data = self.copy_data(cr, uid, id, default, context)
        bom_data = data.copy()
        self.update_quantity_by_formula(cr, uid, object, line, data)
        new_id = self.create(cr, uid, data, context)
        self.copy_translations(cr, uid, id, new_id, context)
        return new_id, bom_data
            
    # Only create record if qty > 0 and of type bom_formula
    def create(self, cr, uid, vals, context=None):
        if context ==  None:
            context = {}
        if context.get('bom_formula', False):
            prec = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
            if round(vals.get('product_qty'), prec) > 0:
                return super(mrp_bom, self).create(cr, uid, vals, context=context)
            else:
                return False
        else:
            return super(mrp_bom, self).create(cr, uid, vals, context=context)

    def action_product_bom_create(self, cr, uid, ids, data, context=None):
        product_id, bom_id = super(mrp_bom, self).action_product_bom_create(cr, uid, ids, data, context=context)
        res = {
            'is_one_time_use': data['is_one_time_use'],
            'ref_order_id': data['ref_order_id'] and data['ref_order_id'][0] or False,
        }
        self.pool.get('product.product').write(cr, uid, product_id, res)
        return product_id, bom_id

mrp_bom()    

class mrp_production_product_line(osv.osv):
    
    _inherit = 'mrp.production.product.line'
    
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
                for set in sets:
                    factor = set.flowrate or (set.correction_factor and 1/set.correction_factor) or 0.0
                    res[product_line.id].update({
                        set.machine_id.name + '_inject1': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_1/100)+1)/factor or 0.0,
                        set.machine_id.name + '_inject2': factor and (W*L*T/1000000000-(product.cut_area*T/1000))*set.density*((set.overpack_2/100)+1)/factor or 0.0,
                        set.machine_id.name + '_settime': set.settime,
                    })
                                      
        return res
    
    def _get_product_line(self, cr, uid, ids, context=None):
        """ return all product_line for the same updated product """
        product_line_ids = []
        for product in self.browse(cr, uid, ids, context=context):
            product_line_ids += self.pool.get('mrp.production.product.line').search(cr, uid, [('product_id','=',product.id)], context=context)
        return product_line_ids  
    
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
    }
    
class bom_choice_thick(osv.osv):
    _name = 'bom.choice.thick'
    _description = 'Thickness Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=10, required=True),
        'value': fields.float('Value', required=True),  
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_thick()

class bom_choice_model(osv.osv):
    _name = 'bom.choice.model'
    _description = 'Model Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),  
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_model()

class bom_choice_joint(osv.osv):
    _name = 'bom.choice.joint'
    _description = 'Joint Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),  
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_joint()

class bom_choice_skin(osv.osv):
    _name = 'bom.choice.skin'
    _description = 'Skin Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),    
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_skin()

class bom_choice_insulation(osv.osv):
    _name = 'bom.choice.insulation'
    _description = 'Skin Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),    
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_skin()

class bom_choice_camlock(osv.osv):
    _name = 'bom.choice.camlock'
    _description = 'Camlock Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),    
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_camlock()


class bom_choice_window(osv.osv):
    _name = 'bom.choice.window'
    _description = 'Window Choice when create BOM'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=10, required=True),    
        'bom_ids': fields.many2many('mrp.bom', string='BOMs'),
    }
    
bom_choice_camlock()

class mrp_machine_setup_master(osv.osv):
    _name = 'mrp.machine.setup.master'
    _description = 'Master Data for Machine Setup'
    _columns = {
        'name': fields.selection([('line1','Line 1'),
                                     ('line2','Line 2'),
                                     ('line3','Line 3'),
                                     ('line4','Line 4'),
                                     ('line5','Line 5'),],'Machine'),
        'description': fields.text('Description')  ,   
        'line_ids': fields.one2many('mrp.machine.setup.master.line', 'machine_id', 'Machine Setup Detail')
    }
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'No duplication of machine allowed!'),
    ]    
    
mrp_machine_setup_master()


class mrp_machine_setup_master_line(osv.osv):
    _name = 'mrp.machine.setup.master.line'
    _description = 'Machine Setup Detail'
    _columns = {
        'machine_id': fields.many2one('mrp.machine.setup.master', 'Machine', ondelete='cascade'),
        'thickness': fields.many2one('bom.choice.thick', string='Thickness (mm)'),
        'flowrate': fields.float('Flowrate (kg/sec)', digits=(16,3)),
        'density': fields.float('Density (kg/m3)'),
        'correction_factor': fields.float('Correction Factor'),
        'overpack_1': fields.float('% Overpack (morning)'),     
        'overpack_2': fields.float('% Overpack (afternoon)'),     
        'settime': fields.float('Set Time'),
    }
    _sql_constraints = [
        ('value_unique', 'unique(machine_id, thickness)', 'No duplication of thickness allowed!'),
    ]        
    
mrp_machine_setup_master_line()

class mrp_production(osv.osv):
    
    _inherit = "mrp.production"
 
    def _get_ref_order_id(self, cr, uid, context=None):
        if context == None:
            context = {}
        product_id = context.get('active_id', False)
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id)
            return product.ref_order_id and product.ref_order_id.id or False
        return False
     
    _defaults = {
        'order_id': _get_ref_order_id,
    }
    
mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
