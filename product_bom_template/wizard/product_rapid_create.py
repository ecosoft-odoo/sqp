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

from osv import fields, osv
from tools.translate import _

class product_rapid_create_line(osv.osv):

    def onchange_bom_template_id(self, cr, uid, ids, bom_template_id, context=None):

        if bom_template_id:
            bom = self.pool.get('mrp.bom').browse(cr, uid, bom_template_id, context=context)
            return {'value': {'is_W_required': bom.W,
                              'is_L_required': bom.L,
                              'is_T_required': len(bom.T) > 0,
                              # Choices
                              'is_mat_model_choices_required': len(bom.mat_model_choices) > 0,
                              'is_mat_joint_choices_required': len(bom.mat_joint_choices) > 0,
                              'is_mat_inside_skin_choices_required': len(bom.mat_inside_skin_choices) > 0,
                              'is_mat_outside_skin_choices_required': len(bom.mat_outside_skin_choices) > 0,
                              'is_mat_insulation_choices_required': len(bom.mat_insulation_choices) > 0,
                              'is_mat_camlock_choices_required': len(bom.mat_camlock_choices) > 0,
                              'is_mat_window_choices_required': len(bom.mat_camlock_choices) > 0},
                    }

        return {}
    
    def _get_bom_product_type(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('bom_product_type', False)
    
    _name = 'product.rapid.create.line'
    _rec_name = 'part_name'
    _order = 'id desc'
    _columns = {
        'wizard_id':fields.many2one('product.rapid.create', 'Wizard Ref', required=True, ondelete='CASCADE', select=True),
        'sequence': fields.integer('Seq.', help="Gives the sequence order, this will be used when create Manufacturing Order"),
        'part_name':fields.char('Part Name', size=128, required=True, help='Naming with format, <zone>_<part_name>, ie.., Z1_W1', select=True),
        'part_code':fields.char('Part Code', size=64, required=False),
        'bom_product_type':fields.selection([('panel','Panel'),
                                             ('door','Door'),
                                             ('window','Window'),],'BOM Product Type', required=True),
        'bom_template_id':fields.many2one('mrp.bom', 'BOM Template', required=True, ondelete='CASCADE', select=True),
        'W':fields.float('Width (W)', ondelete='CASCADE', select=True),
        'L':fields.float('Length (L)', ondelete='CASCADE', select=True),
        'T':fields.many2one('bom.choice.thick', 'Thick (T)', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_model_choices':fields.many2one('bom.choice.model', 'Model', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_joint_choices':fields.many2one('bom.choice.joint', 'Joint', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_inside_skin_choices':fields.many2one('bom.choice.skin', 'Inside Skin', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_outside_skin_choices':fields.many2one('bom.choice.skin', 'Outside Skin', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_insulation_choices':fields.many2one('bom.choice.insulation', 'Insulation', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_camlock_choices':fields.many2one('bom.choice.camlock', 'Camlock', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        'mat_window_choices':fields.many2one('bom.choice.window', 'Window', domain="[('bom_ids','in',[bom_template_id or 0])]", required=False, ondelete='CASCADE', select=True),
        # Required Flag
        'is_W_required':fields.boolean('Width Required', ondelete='CASCADE', select=True),
        'is_L_required':fields.boolean('Length Required', ondelete='CASCADE', select=True),
        'is_T_required':fields.boolean('Thick Required', ondelete='CASCADE', select=True),
        'is_mat_model_choices_required':fields.boolean('Model Required', ondelete='CASCADE', select=True),
        'is_mat_joint_choices_required':fields.boolean('Joint Required', ondelete='CASCADE', select=True),
        'is_mat_inside_skin_choices_required':fields.boolean('Inside Skin Required', ondelete='CASCADE', select=True),
        'is_mat_outside_skin_choices_required':fields.boolean('Outside Skin Required', ondelete='CASCADE', select=True),
        'is_mat_insulation_choices_required':fields.boolean('Insulation Required', ondelete='CASCADE', select=True),
        'is_mat_camlock_choices_required':fields.boolean('Camlock Required', ondelete='CASCADE', select=True),
        'is_mat_window_choices_required':fields.boolean('Window Required', ondelete='CASCADE', select=True),
        'cut_area':fields.float('Cut Area (sqm)'),
        'remark':fields.char('Remarks', size=128),
        'partner_id': fields.many2one('res.partner', 'Product Customer'),
        'list_price': fields.float('List Price'),
    }
    _defaults = {
        'bom_product_type': _get_bom_product_type,
    }
    
    
    
product_rapid_create_line()

class product_rapid_create(osv.osv):
    """
    Rapid Create Part
    """   
    _name = 'product.rapid.create'
    _rec_name = 'order_id'    
    
    def _get_type(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type', False)
        
    _columns = {
        'state': fields.selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ], 'Status', readonly=True, track_visibility='onchange', select=True),
        'order_id':fields.many2one('sale.order', 'Sales Order Ref', domain="[('state','not in',('draft','sent','cancel'))]", readonly=True, states={'draft': [('readonly', False)]}),
        'description': fields.text('Description'),
        'user_id':fields.many2one('res.users', 'User', readonly=True),
        'is_one_time_use': fields.boolean('One-Time Use', required=False, help="One time used product are those product created from Rapid Product Creation wizard as they are linked to specific SO"),
        'sale_ok': fields.boolean('Can be Sold'),
        'tag_ids': fields.many2many('product.tag', string='Tags', help="Tagged products are products to be shown in Sales Order."),   
        'product_categ_id': fields.many2one('product.category', 'Category', required=True, readonly=False),        
        'type': fields.selection([('product','Stockable Product'),('consu', 'Consumable'),('service','Service')], 'Product Type', required=True, help="Consumable: Will not imply stock management for this product. \nStockable product: Will imply stock management for this product."),
        'procure_method': fields.selection([('make_to_stock','Make to Stock'),('make_to_order','Make to Order')], 'Procurement Method', required=True, help="Make to Stock: When needed, the product is taken from the stock or we wait for replenishment. \nMake to Order: When needed, the product is purchased or produced."),
        'cost_method': fields.selection([('standard','Standard Price'), ('average','Average Price')], 'Costing Method', required=True,
            help="Standard Price: The cost price is manually updated at the end of a specific period (usually every year). \nAverage Price: The cost price is recomputed at each incoming shipment."),
        'supply_method': fields.selection([('produce','Manufacture'),('buy','Buy')], 'Supply Method', required=True, help="Manufacture: When procuring the product, a manufacturing order or a task will be generated, depending on the product type. \nBuy: When procuring the product, a purchase order will be generated."),
        'valuation':fields.selection([('manual_periodic', 'Periodical (manual)'),
                                        ('real_time','Real Time (automated)'),], 'Inventory Valuation',
                                        help="If real-time valuation is enabled for a product, the system will automatically write journal entries corresponding to stock moves." \
                                             "The inventory variation account set on the product category will represent the current inventory value, and the stock input and stock output account will hold the counterpart moves for incoming and outgoing products."
                                        , required=True),
        'panel_lines': fields.one2many('product.rapid.create.line', 'wizard_id', 'Panel Lines', domain=[('bom_product_type','=','panel')], readonly=True, states={'draft': [('readonly', False)]},),
        'door_lines': fields.one2many('product.rapid.create.line', 'wizard_id', 'Door Lines', domain=[('bom_product_type','=','door')], readonly=True, states={'draft': [('readonly', False)]},),
        'window_lines': fields.one2many('product.rapid.create.line', 'wizard_id', 'Window Lines', domain=[('bom_product_type','=','window')], readonly=True, states={'draft': [('readonly', False)]},),
        'num_panel_lines':fields.integer('Copy Panel Lines', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'num_door_lines':fields.integer('Copy Door Lines', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'num_window_lines':fields.integer('Copy Window Lines', required=False, readonly=True, states={'draft': [('readonly', False)]}),
    }
    _defaults = {
        'state': 'draft',
        'user_id': lambda self, cr, uid, c: uid,
        'num_panel_lines': 1,
        'num_door_lines': 1,
        'num_window_lines': 1,
        'is_one_time_use' : True,
        'type': 'product',
        'procure_method': 'make_to_order',
        'cost_method': 'average',
        'supply_method': 'produce',
        'valuation': 'manual_periodic',
    }
    
    def copy_lines(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        num_lines = context.get('num_lines', False)
        if not num_lines:
            return False
        
        rapid_create = self.browse(cr, uid, ids[0])
        line_obj = self.pool.get('product.rapid.create.line')        
        cr.execute("select max(id) as id \
                        from product_rapid_create_line \
                        where wizard_id = %s \
                        and bom_product_type = %s",
                       (ids[0], context.get('bom_product_type', False)))        
        line_id = cr.fetchone()[0] or False
        
        if line_id:
            default = {}
            rs = line_obj.copy_data(cr, uid, line_id, default, context=context)
            i = 0
            while i < num_lines:
                line_obj.create(cr, uid, rs, context=context)           
                i += 1         
        else:
            return False
        
        return {
                'type': 'ir.actions.client',
                'tag': 'reload'
                }       
           
    def create_product(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        # Get the selected BOM Template
        object =  self.browse(cr, uid, ids[0], context=context)
        lines = object.panel_lines + object.door_lines + object.window_lines
        
        result = []
        
        if not len(lines):
            return False
        
        new_id, old_id = 0, 0
        
        for line in lines:
            bom_template = line.bom_template_id
            # If template, then continue, else, stop
            if bom_template.is_bom_template:
                product_obj = self.pool.get('product.product')
                bom_obj = self.pool.get('mrp.bom')
                # Create new object by copy the existing one, then change name using predefined format
                product_template = product_obj.browse(cr, uid, bom_template.product_id.id)
                new_product_name = eval(bom_template.new_name_format, {'object':object, 'line':line})
                res = {
                    'name': new_product_name,
                    'sequence': line.sequence,
                    'default_code': line.part_code,
                    'sale_ok': object.sale_ok,
                    'purchase_ok': False,
                    'ref_order_id': object.order_id.id,
                    'tag_ids': [(6, 0, [x.id for x in object.tag_ids])],
                    'is_one_time_use': object.is_one_time_use,
                    'categ_id': object.product_categ_id.id,
                    'type': object.type,
                    'procure_method': object.procure_method,
                    'cost_method': object.cost_method,
                    'supply_method': object.supply_method,
                    'valuation': object.valuation,     
                    'bom_product_type': line.bom_template_id.bom_product_type,         
                    'W': line.W,
                    'L': line.L,
                    'T': line.T.id,
                    'mat_inside_skin_choices': line.mat_inside_skin_choices.id,
                    'mat_outside_skin_choices': line.mat_outside_skin_choices.id,
                    'mat_insulation_choices': line.mat_insulation_choices.id,
                    'cut_area': line.cut_area,
                    'remark': line.remark,
                    'partner_id': line.partner_id and line.partner_id.id,
                    'list_price': line.list_price
                }
                new_product_id = product_obj.copy(cr, uid, product_template.id, default = {}, context=context)
                result.append(new_product_id)
                product_obj.write(cr, uid, new_product_id, res)
                
                # Copy Bill of Material
                res = {
                    'name': new_product_name,
                    'product_id':new_product_id,
                    'is_bom_template': False,
                    'bom_template_type': None
                }                
                
                # Performance Tuning
                new_id = bom_template.id
                if new_id != old_id:
                    context.update({'bom_data': False})
                new_bom_id, bom_data = bom_obj.copy_bom_formula(cr, uid, bom_template.id,
                                          object, line,
                                          default = {}, 
                                          context=context)
                old_id = bom_template.id
                context.update({'bom_data': bom_data})
                # --
                bom_obj.write(cr, uid, new_bom_id, res)
                
        # Return
        data_obj = self.pool.get('ir.model.data')
        if result and len(result):
            
            self.write(cr, uid, ids[0], {'state': 'done'})
            
            #res_id = result[0]
            form_view_id = data_obj._get_id(cr, uid, 'product', 'product_normal_form_view')
            form_view = data_obj.read(cr, uid, form_view_id, ['res_id'])
            tree_view_id = data_obj._get_id(cr, uid, 'product', 'product_product_tree_view')
            tree_view = data_obj.read(cr, uid, tree_view_id, ['res_id'])
            search_view_id = data_obj._get_id(cr, uid, 'product', 'product_search_form_view')
            search_view = data_obj.read(cr, uid, search_view_id, ['res_id'])
            return {
                'name': _('Product'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'product.product',
                'view_id': False,
                'domain':[('id','in',result)],
                #'res_id': res_id,
                'views': [(tree_view['res_id'],'tree'),(form_view['res_id'],'form')],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view['res_id'],
                'nodestroy': True
        }                
        return False

product_rapid_create()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
