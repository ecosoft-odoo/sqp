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

class mrp_production(osv.osv):
    
    _inherit = 'mrp.production'

    def _mrp_production_exists(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for production in self.browse(cursor, user, ids, context=context):
            res[production.id] = False
            cursor.execute('''SELECT COUNT(1) from mrp_production
                                 where parent_id = %s''',
                            (production.id,))
            if cursor.fetchone()[0]:
                res[production.id] = True
        return res
    
    def _check_submo_valid(self, cr, uid, ids, context=None):
        for mo in self.browse(cr, uid, ids, context=context):
            if mo.state in ('confirmed', 'ready'):
                # For Super MO, must have only 1 level of sub-MO
                if not mo.parent_id:
                    if len(mo.child_ids) == 0:
                        return False
                    for mo in mo.child_ids:
                        if len(mo.child_ids) > 0:
                            return False
                # For Sub-MO, must have no Sub-MO
                elif mo.parent_id:
                    if len(mo.child_ids) > 0:
                        return False
        return True
    
    _columns = {
        'target_picking_id': fields.many2one('stock.picking.out', 'Target Delivery Order', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'mrp_production_exists': fields.function(_mrp_production_exists, string='MO Exists', 
            type='boolean', help="It indicates that MO has at least one child."),
        'child_ids': fields.one2many('mrp.production', 'parent_id', 'Sub MO', readonly=True),
        'sale_picking_ids': fields.related('order_id', 'picking_ids', type='one2many', relation='stock.picking.out', string='Pickings of related SO', readonly=True),
        'partner_id': fields.related('order_id', 'partner_id', type='many2one', relation='res.partner', string='Customer', readonly=True, store=True),
        'is_printed': fields.boolean('Printed'),
        'note': fields.text('Remark'),
        'short_note': fields.char('Short Note', size=256, required=False, readonly=False),
    }
    _constraints = [
        (_check_submo_valid,
            '\n 1) MO must have 1 level of Sub-MO\n 2) Sub-MO must have no Sub-MO',
            ['child_ids'])]    
    
    def action_view_child_mrp_production(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display childs MOs of given MO ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        if context is None:
            context = {}        
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'mrp', 'mrp_production_action')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #compute the number of MOs to display
        mo_ids = []
        production = self.pool.get('mrp.production')
        mo_ids = production.search(cr, uid, [('parent_id', 'child_of', ids)])
        
        mo_ids.remove(ids[0])
        #choose the view_mode accordingly
        if len(mo_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, mo_ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'mrp', 'mrp_production_form_view')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = mo_ids and mo_ids[0] or False
        # Remove search Default Product
        result['context'] = {'search_default_product_id': False}
        return result
    
    # Cancel MO and sub-MOs
    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        stock_picking_obj = self.pool.get('stock.picking')
        for production in self.browse(cr, uid, ids, context=context):
            # Cancel MOs
            if production.state in ('ready','confirmed') and production.picking_id.state in ('confirmed','assigned'):
                nids = move_obj.search(cr, uid, [ ('picking_id','=',production.picking_id.id) ] )
                move_obj.action_cancel(cr, uid, nids)
                if production.move_created_ids:
                    move_obj.action_cancel(cr, uid, [x.id for x in production.move_created_ids]) 
                if production.move_lines:
                    move_obj.action_cancel(cr, uid, [x.id for x in production.move_lines])
                if production.move_prod_id:
                    move_obj.action_cancel(cr, uid, [production.move_prod_id.id])
                stock_picking_obj.write(cr, uid, [production.picking_id.id], {'state': 'cancel'})
                # Cancel all sub MOs
                for sub_mo in production.child_ids:
                    if sub_mo.state in ('ready','confirmed') and sub_mo.picking_id.state in ('confirmed','assigned'):
                        nids = move_obj.search(cr, uid, [ ('picking_id','=',sub_mo.picking_id.id) ] )
                        move_obj.action_cancel(cr, uid, nids)
                        if sub_mo.move_created_ids:
                            move_obj.action_cancel(cr, uid, [x.id for x in sub_mo.move_created_ids]) 
                        if sub_mo.move_lines:
                            move_obj.action_cancel(cr, uid, [x.id for x in sub_mo.move_lines])
                        if sub_mo.move_prod_id:
                            move_obj.action_cancel(cr, uid, [sub_mo.move_prod_id.id])
                        stock_picking_obj.write(cr, uid, [sub_mo.picking_id.id], {'state': 'cancel'})  
                super(mrp_production, self).action_cancel(cr, uid, [x.id for x in production.child_ids], context=context)              
        
        return super(mrp_production, self).action_cancel(cr, uid, ids, context=context)    
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
                'child_ids': [],
                'status_lines': [],
                'target_picking_id': False,
            })
        return super(mrp_production, self).copy(cr, uid, id, default, context)
    
    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        date_planned = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT) #+ relativedelta(days=line.delay or 0.0) # MO Line has not delay yet.
        date_planned = (date_planned - timedelta(days=order.company_id.security_lead)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return date_planned

    def _prepare_production_picking(self, cr, uid, production, context=None):
        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
        return {
            'name': pick_name,
            'origin': production.name,
            'date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'out',
            'ref_order_id': production.order_id and production.order_id.id,
            'ref_project_name': production.order_id and self.pool.get('sale.order').browse(cr, uid, production.order_id.id, context=context).ref_project_name or False,
            'state': 'draft',
            'move_type': production.order_id and production.order_id.picking_policy or 'direct',
            'sale_id': production.order_id and production.order_id.id or False,
            'partner_id': production.order_id and production.order_id.partner_shipping_id.id or False,
            'note': False,
            'invoice_state': 'none',
            'company_id': production.company_id.id,
        }    

    def _prepare_production_line_move(self, cr, uid, production, line, picking_id, date_planned, context=None):
        location_id = production.order_id and production.order_id.shop_id.warehouse_id.lot_stock_id.id or False
        output_id = production.order_id and production.order_id.shop_id.warehouse_id.lot_output_id.id or False
        return {
            'name': line.name,
            'picking_id': picking_id,
            'product_id': line.product_id.id,
            'date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'date_expected': date_planned,
            'product_qty': line.product_qty,
            'product_uom': line.product_uom.id,
            'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_qty,
            'product_uos': (line.product_uos and line.product_uos.id)\
                    or line.product_uom.id,
            'product_packaging': False, #line.product_packaging.id,
            'partner_id': production.order_id and production.order_id.partner_shipping_id.id or False,
            'location_id': location_id,
            'location_dest_id': output_id,
            'sale_line_id': False,
            'tracking_id': False,
            'state': 'draft',
            #'state': 'waiting',
            'company_id': production.company_id.id,
            'price_unit': line.product_id.standard_price or 0.0
        }

    def _create_picking(self, cr, uid, production, production_lines, picking_id=False, context=None):

        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        sale_obj = self.pool.get('sale.order')

        for line in production_lines:
            #date_planned = self._get_date_planned(cr, uid, production.order_id, production.order_id.order_line, production.order_id.date_order , context=context)
            # Simply use date in MO's scheduled
            date_planned = production.date_planned
            if line.product_id:
                if line.product_id.type in ('product', 'consu'):
                    if not picking_id:
                        picking_id = picking_obj.create(cr, uid, self._prepare_production_picking(cr, uid, production, context=context))
                    move_id = move_obj.create(cr, uid, self._prepare_production_line_move(cr, uid, production, line, picking_id, date_planned, context=context))
                else:
                    # a service has no stock move
                    move_id = False
        # If Ref Order exists, reference this new Picking back to DO.
        if production.order_id:
            picking_obj.write(cr, uid, [picking_id], {'sale_id': production.order_id.id})
            # As DO is created, do not mark SO as done.
            sale_obj.write(cr, uid, [production.order_id.id], {'shipped': False})
        # If state of MO already done, make DO as ready.
        if production.state == 'done':
            picking_obj.draft_force_assign(cr, uid, [picking_id])
            picking_obj.force_assign(cr, uid, [picking_id])
        return picking_id
    
    def action_ship_create(self, cr, uid, ids, context=None):
        for production in self.browse(cr, uid, ids, context=context):
            if not production.target_picking_id and not production.sale_picking_ids:
                picking_id = self._create_picking(cr, uid, production, production.product_lines, None, context=context)
                if picking_id:
                    self.write(cr, uid, [production.id], {'target_picking_id': picking_id})
        return True
     
    def action_confirm(self, cr, uid, ids, context=None):
        # For Super MO only, If the DO is not yet created for it, do it now.
        for production in self.browse(cr, uid, ids):
            # 1) Assign Target Delivery Order when not yet created,
            picking_id = False
            if not production.parent_id and not production.target_picking_id:
                # 1.1) SO of type "On Demand", always create DO from MO
                if production.order_id.order_policy == 'manual': 
                    picking_id = self._create_picking(cr, uid, production, production.product_lines, None, context=context)
                # 1.2) Other SO type, reference if DO exists, 
                elif production.sale_picking_ids and len(production.sale_picking_ids) > 0:
                    picking_id = production.sale_picking_ids[0].id
            if picking_id:
                self.write(cr, uid, [production.id], {'target_picking_id': picking_id})                     
            # 2) If DO is created from SO (Standard AHU), we need to update all.
            if not production.parent_id and production.order_id.order_policy != 'manual': 
                self.pool.get('stock.picking').write(cr, uid, [x.id for x in production.sale_picking_ids], {'origin': production.name})

        res = super(mrp_production, self).action_confirm(cr, uid, ids, context=context)
        return res    
        
    def action_produce(self, cr, uid, production_id, production_qty, production_mode, context=None):
        res = super(mrp_production, self).action_produce(cr, uid, production_id, production_qty, production_mode, context=context)
        production = self.browse(cr, uid, production_id)
        # Make its related picking Ready to Deliver
        picking_obj = self.pool.get('stock.picking')
        picking_id = production.target_picking_id and production.target_picking_id.id
        if picking_id:
            picking_obj.draft_force_assign(cr, uid, [picking_id])
            picking_obj.force_assign(cr, uid, [picking_id])
        return res
    
    # Force RW and FG location
#     def write(self, cr, uid, ids, vals, context=None):
#         res = super(mrp_production, self).write(cr, uid, ids, vals, context=context)
#         location_model, location_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'location_production')
#         prod_obj = self.pool.get('mrp.production')
#         prod_obj.write(cr, uid, ids, {'location_src_id': location_id, 'location_dest_id': location_id}, context=context)
#         return res
    
    def create(self, cr, uid, vals, context=None):
        res = super(mrp_production, self).create(cr, uid, vals, context=context)
        # Default hard coded location for SQP
        location_model, location_factoryfg_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sqp_config_2', 'stock_location_factory_fg')
        location_model, location_prod_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'location_production')
        prod_obj = self.pool.get('mrp.production')
        production = prod_obj.browse(cr, uid, res, context=context)
        if not production.parent_id: # Super MO
            prod_obj.write(cr, uid, [res], {'location_src_id': location_prod_id, 'location_dest_id': location_prod_id}, context=context)
        else: # Sub-MO
            order_id = vals.get('order_id', False)
            if order_id:
                order = self.pool.get('sale.order').browse(cr, uid, order_id)
                location_factoryfg_id = order.shop_id.warehouse_id and order.shop_id.warehouse_id.lot_stock_id.id or location_factoryfg_id
            prod_obj.write(cr, uid, [res], {'location_src_id': location_prod_id, 'location_dest_id': location_factoryfg_id}, context=context)
        return res  
    

    def action_ready(self, cr, uid, ids, context=None):
        """ Changes the production state to Ready and location id of stock move.
        @return: True
        """
        self.write(cr, uid, ids, {'state': 'ready'})

        for production in self.browse(cr, uid, ids, context=context):
            if not production.move_created_ids:
                produce_move_id = self._make_production_produce_line(cr, uid, production, context=context)
                for scheduled in production.product_lines:
                    self._make_production_line_procurement(cr, uid, scheduled, False, context=context)
                    
        return True        
mrp_production()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
