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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import float_compare

class stock_picking(osv.osv):

    _inherit = 'stock.picking'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        if context is None:
            context = {}
        res = super(stock_picking, self).do_partial(cr, uid, ids, partial_datas, context=None)
        return res

stock_picking()


class stock_picking_out(osv.osv):

    _inherit = 'stock.picking.out'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            if context.get('is_delivery_order', False) or context.get('is_bom_move', False):
                if context.get('is_delivery_order', False):
                    seq_obj_name =  self._name
                    vals['name'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
                else:
                    vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'bom.move')
                boi_type = vals.get('boi_type', False)
                if boi_type:
                    boi_type = boi_type == 'BOI' and 'BOI' or 'NONBOI'
                    vals.update({'name': '%s-%s'%(boi_type,vals.get('name'))})
        return super(stock_picking_out, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        picking_id = super(stock_picking_out, self).copy(cr, uid, id, default=default, context=context)
        if picking_id:
            if context.get('is_delivery_order', False) or context.get('is_bom_move', False):
                picking_obj = self.pool.get('stock.picking')
                picking = picking_obj.browse(cr, uid, picking_id, context=context)
                boi_type = picking.boi_type == 'BOI' and 'BOI' or 'NONBOI'
                name = '%s-%s'%(boi_type,picking.name)
                picking_obj.write(cr, uid, picking_id, {'name': name}, context=context)
        return picking_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        boi_type = vals.get('boi_type', False)
        if boi_type and (context.get('is_delivery_order', False) or context.get('is_bom_move', False)):
            boi_type = boi_type == 'BOI' and 'BOI' or 'NONBOI'
            picking_obj = self.pool.get('stock.picking')
            for picking in picking_obj.browse(cr, uid, ids, context=context):
                vals['name'] = picking.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(stock_picking_out, self).write(cr, uid, ids, vals, context=context)

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_cert_id': False}}

    def create_extra_move(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        picking_obj = self.pool.get('stock.picking')
        rm_boi_location = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')], context=context)
        rm_location = location_obj.search(cr, uid, [('name','=','FC_RM')], context=context)
        if len(rm_boi_location) > 0:
            rm_boi_location = rm_boi_location[0]
        if len(rm_location) > 0:
            rm_location = rm_location[0]
        location_id = False
        move_ids = []
        boi_type = 'NONBOI'
        not_create_extra_move = False
        context.update({
            'states': ['done'],
            'what': ['in','out']
        })
        if len(ids) > 0:
            picking = picking_obj.browse(cr, uid, ids[0], context=context)
            boi_type = picking.boi_type
            location_id = picking.boi_type == 'BOI' and rm_boi_location or rm_location
            move_ids = move_obj.search(cr, uid, [('picking_id','=',ids[0])], context=context)
        for move in move_obj.browse(cr, uid, move_ids, context=context):
            available_rm_product_quantity = 0.0
            available_rm_boi_product_quantity = 0.0
            product_id = move.product_id and move.product_id.id or False
            # Check product qty in FC_RM
            context.update({
                'location': rm_location
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_rm_product_quantity = available_product_detail.values()[0]
            # Check product qty in FC_RM_BOI
            context.update({
                'location': location_id
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_rm_boi_product_quantity = available_product_detail.values()[0]
            compare = float_compare(available_rm_boi_product_quantity, move.product_qty, 3)
            if compare >= 0 or available_rm_product_quantity <= 0.0:
                not_create_extra_move = True
            else:
                not_create_extra_move = False
                break
        if not_create_extra_move:
            raise osv.except_osv(_('Warning!'), _('Not Create Extra Move'))
        picking_ids = []
        pick_name = ''
        if len(ids) > 0:
            picking_ids = picking_obj.search(cr, uid, [('picking_id_ref','=',ids[0]),('state','!=','done')], context=context)
        for picking in picking_obj.browse(cr, uid, picking_ids, context=context):
            cr.execute('select name from stock_picking where id = %s',(picking.id,))
            pick_name = cr.fetchone()[0]
            pick_name = (pick_name.find('BOI') >= 0 and pick_name.find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                and pick_name.replace('BOI','NONBOI') \
                                or (pick_name.find('NONBOI') >= 0 and boi_type == 'BOI') \
                                and pick_name.replace('NONBOI','BOI')  \
                                or pick_name
            cr.execute('delete from stock_move where picking_id = %s',(picking.id,))
            cr.execute('delete from stock_picking where id = %s',(picking.id,))
        if len(picking_ids) == 0:
            pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking')
            pick_name = '%s-%s'%(boi_type,pick_name)
        if len(ids) > 0:
            picking_id = self._create_stock_picking(cr, uid, ids, pick_name, context=context)
            if picking_id:
                self._create_stock_moves(cr, uid, ids, picking_id, context=context)
        result = self._view_stock_picking(cr, uid, ids, context=context)
        return result

    def _create_stock_picking(self, cr, uid, ids, pick_name, context=None):
        picking_obj = self.pool.get('stock.picking')
        new_picking_id = False
        if len(ids) > 0:
            picking = picking_obj.browse(cr, uid, ids[0], context=context)
            prepare_stock_picking = self._prepare_stock_picking(cr, uid, ids, picking, pick_name, context=context)
            new_picking_id = picking_obj.create(cr, uid, prepare_stock_picking, context=context)
        return new_picking_id

    def _prepare_stock_picking(self, cr, uid, ids, picking, pick_name, context=None):
        prepare_stock_picking = {
            'name': pick_name,
            'origin': picking.name,
            'partner_id': picking.partner_id and picking.partner_id.id or False,
            'stock_journal_id': picking.stock_journal_id and picking.stock_journal_id.id or False,
            'location_id': picking.location_id and picking.location_id.id or False,
            'move_type': picking.move_type,
            'company_id': picking.company_id and picking.company_id.id or False,
            'invoice_state': picking.invoice_state,
            'note': picking.note,
            'state': 'draft',
            'location_dest_id': picking.location_dest_id and picking.location_dest_id.id or False,
            'auto_picking': False,
            'type': 'internal',
            'purchase_id': picking.purchase_id and picking.purchase_id.id or False,
            'sale_id': picking.sale_id and picking.sale_id.id or False,
            'picking_id_ref': ids[0],
            'is_supply_list': False,
            'product_categ_id': picking.product_categ_id and picking.product_categ_id.id or False,
            'ref_order_id': picking.ref_order_id and picking.ref_order_id.id or False,
            'ref_project_name': picking.ref_project_name,
            'contact_name': picking.contact_name,
            'car_plate': picking.car_plate,
            'is_printed': picking.is_printed,
            'tag_no': picking.tag_no,
            'invoice_id': picking.invoice_id and picking.invoice_id.id or False,
            'ref_partner_id': picking.ref_partner_id and picking.ref_partner_id.id or False,
            'ref_mo_id': picking.ref_mo_id and picking.ref_mo_id.id or False,
            'department_id': picking.department_id and picking.department_id.id or False,
            'is_bom_move': False
        }
        return prepare_stock_picking

    def _create_stock_moves(self, cr, uid, ids, picking_id, context=None):
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        picking_obj = self.pool.get('stock.picking')
        rm_boi_location = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')], context=context)
        rm_location = location_obj.search(cr, uid, [('name','=','FC_RM')], context=context)
        if len(rm_boi_location) > 0:
            rm_boi_location = rm_boi_location[0]
        if len(rm_location) > 0:
            rm_location = rm_location[0]
        location_id = False
        move_ids = []
        context.update({
            'states': ['done'],
            'what': ['in','out']
        })
        if len(ids) > 0:
            picking = picking_obj.browse(cr, uid, ids[0], context=context)
            location_id = picking.boi_type == 'BOI' and rm_boi_location or False
            move_ids = move_obj.search(cr, uid, [('picking_id','=',ids[0])], context=context)
        result = []
        for move in move_obj.browse(cr, uid, move_ids, context=context):
            available_rm_product_quantity = 0.0
            available_rm_boi_product_quantity = 0.0
            product_id = move.product_id and move.product_id.id or False
            # FC_RM location
            context.update({
                'location': rm_location
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_rm_product_quantity = available_product_detail.values()[0]
            if available_rm_product_quantity <= 0.0:
                continue
            # FC_RM_BOI location
            context.update({
                'location': location_id
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_rm_boi_product_quantity = available_product_detail.values()[0]
            compare = float_compare(available_rm_boi_product_quantity, move.product_qty, 3)
            if compare == -1:
                compare = float_compare(move.product_qty - available_rm_boi_product_quantity, available_rm_product_quantity, 3)
                if compare >= 0:
                    product_qty = available_rm_product_quantity
                else:
                    product_qty = move.product_qty - available_rm_boi_product_quantity
                prepare_stock_move = self._prepare_stock_move(cr, uid, picking_id, move, picking, rm_location, rm_boi_location, product_qty, context=context)
                move_id = move_obj.create(cr, uid, prepare_stock_move, context=context)
                result.append(move_id)
        return result

    def _prepare_stock_move(self, cr, uid, picking_id, move, picking, location_id, location_dest_id, product_qty, context=None):
        prepare_stock_move = {
            'origin': picking.name,
            'product_uos_qty': move.product_uos_qty,
            'product_uom': move.product_uom and move.product_uom.id or False,
            'price_unit': move.price_unit,
            'prodlot_id': move.prodlot_id and move.prodlot_id.id or False,
            'move_dest_id': move.move_dest_id and move.move_dest_id.id or False,
            'product_qty': product_qty,
            'product_uos': move.product_uos,
            'partner_id': move.partner_id and move.partner_id.id or False,
            'name': move.name,
            'note': move.note,
            'product_id': move.product_id and move.product_id.id or False,
            'auto_validate': False,
            'price_currency_id': move.price_currency_id.id or False,
            'location_id': location_id,
            'company_id': move.company_id and move.company_id.id or False,
            'picking_id': picking_id,
            'priority': move.priority,
            'state': 'draft',
            'location_dest_id': location_dest_id,
            'tracking_id': move.tracking_id and move.tracking_id.id or False,
            'product_packaging': move.product_packaging,
            'purchase_line_id': move.purchase_line_id and move.purchase_line_id.id or False,
            'sale_line_id': move.sale_line_id and move.sale_line_id.id or False,
            'production_id': move.production_id and move.production_id.id or False,
            'purchase_id': move.purchase_id and move.purchase_id.id or False,
            'order_qty': move.order_qty,
            'invoice_line_id': move.invoice_line_id and move.invoice_line_id.id or False,
            'generate_asset': move.generate_asset
        }
        return prepare_stock_move

    def _view_stock_picking(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        picking_obj = self.pool.get('stock.picking')

        result = mod_obj.get_object_reference(cr, uid, 'stock',
                                              'action_picking_tree6')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        picking_ids = picking_obj.search(cr, uid, [('type','=','internal'),('picking_id_ref','=',ids[0]),('state','!=','done')], context=context)

        # choose the view_mode accordingly
        res_tree = mod_obj.get_object_reference(
            cr, uid, 'stock', 'vpicktree')
        res_form = mod_obj.get_object_reference(
            cr, uid, 'stock', 'view_picking_form')
        res_calendar = mod_obj.get_object_reference(
            cr, uid, 'stock', 'stock_picking_calendar')
        result['domain'] = \
            "[('id','in',["+','.join(map(str, picking_ids))+"])]"
        result['views'] = \
            [(res_tree and res_tree[1] or False, 'tree'),
             (res_form and res_form[1] or False, 'form'),
             (res_calendar and res_calendar[1] or False, 'calendar')]
        result['res_id'] = picking_ids and picking_ids[0] or False
        result['context'] = {}
        result['context'].update({'contact_display': 'partner_address', 'search_default_available': 0})
        return result

stock_picking_out()


class stock_picking_in(osv.osv):

    _inherit = 'stock.picking.in'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            seq_obj_name =  self._name
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name) or '/'
            if vals.get('boi_type', False) and context.get('default_type', '') == 'in':
                boi_type = vals.get('boi_type','') == 'BOI' and 'BOI' or 'NONBOI'
                vals.update({'name': '%s-%s'%(boi_type, vals.get('name', '/'))})
        return super(stock_picking_in, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        picking_id = super(stock_picking_in, self).copy(cr, uid, id, default=default, context=context)
        picking_obj = self.pool.get('stock.picking')
        if picking_id and context.get('default_type','') == 'in':
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            boi_type = picking.boi_type == 'BOI' and 'BOI' or 'NONBOI'
            name = '%s-%s'%(boi_type,picking.name)
            picking_obj.write(cr, uid, [picking_id], {'name': name}, context=context)
        return picking_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        boi_type = vals.get('boi_type', False)
        picking_obj = self.pool.get('stock.picking')
        if boi_type and context.get('default_type','') == 'in':
            boi_type = boi_type == 'BOI' and 'BOI' or 'NONBOI'
            for picking in picking_obj.browse(cr, uid, ids, context=context):
                vals['name'] = picking.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(stock_picking_in, self).write(cr, uid, ids, vals, context=context)

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_cert_id': False}}

stock_picking_in()


class stock_move(osv.osv):

    _inherit = 'stock.move'

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        result = super(stock_move, self).action_confirm(cr, uid, ids, context=context)
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        rm_boi_location = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')], context=context)
        rm_location = location_obj.search(cr, uid, [('name','=','FC_RM')], context=context)
        if len(rm_boi_location) > 0:
            rm_boi_location = rm_boi_location[0]
        if len(rm_location) > 0:
            rm_location = rm_location[0]
        location_id = False
        picking = False
        if len(ids) > 0:
            move = move_obj.browse(cr, uid, ids[0], context=context)
            picking_id = move.picking_id and move.picking_id.id or False
            if picking_id:
                picking = picking_obj.browse(cr, uid, picking_id, context=context)
                # If not bom move, let return result
                if not picking.is_bom_move:
                    return result
                location_id = picking.boi_type == 'BOI' and rm_boi_location or rm_location
        context.update({
            'states': ['done'],
            'what': ['in','out']
        })
        # Check Stock
        not_product_in_stock = False
        for move in self.browse(cr, uid, ids, context=context):
            available_rm_product_quantity = 0.0
            available_source_product_quantity = 0.0
            product_id = move.product_id and move.product_id.id or False
            # Check product qty in FC_RM
            context.update({
                'location': rm_location
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_rm_product_quantity = available_product_detail.values()[0]
            # Check product qty follow boi_type, if boi_type = 'BOI' check in FC_RM_BOI else check in FC_RM
            context.update({
                'location': location_id
            })
            if product_id:
                available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
                if available_product_detail.values():
                    available_source_product_quantity = available_product_detail.values()[0]
            compare = float_compare(available_source_product_quantity, move.product_qty, 3)
            if compare == -1 and picking and picking.boi_type == 'BOI' and available_rm_product_quantity > 0.0:
                raise osv.except_osv(_('Warning!'), _('Create Extra Move for BOI'))
            if picking and picking.boi_type == 'BOI' and available_rm_product_quantity <= 0.0 and available_source_product_quantity <= 0.0:
                not_product_in_stock = True
            else:
                not_product_in_stock = False
                break
        if not_product_in_stock:
            raise osv.except_osv(_('Warning!'), _('No have product quantity in stock FC_RM_BOI and FC_RM'))
        return result
