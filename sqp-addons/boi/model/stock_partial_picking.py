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
from openerp.tools import float_compare
from openerp.tools.translate import _

class stock_partial_picking(osv.osv_memory):

    _inherit = 'stock.partial.picking'

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(stock_partial_picking, self).default_get(cr, uid, fields, context=context)
        picking_obj = self.pool.get('stock.picking')
        picking_ids = context.get('active_ids', [])
        for picking in picking_obj.browse(cr, uid, picking_ids, context=context):
            # If not bom move or not BOI
            if not picking.is_bom_move or picking.boi_type != 'BOI':
                return res

            # If bom move and BOI
            if 'move_ids' in fields:
                move_ids = res.get('move_ids', [])
                moves = [move_id for move_id in move_ids if move_id.get('quantity', 0.0) != 0.0]
                if len(moves) == 0:
                    raise osv.except_osv(_('Error!'), _('Create Extra Move for BOI !'))
                res.update(move_ids=moves)
        return res

    def do_partial(self, cr, uid, ids, context=None):
        result = super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        for partial in self.browse(cr, uid, ids, context=context):
            picking_id = partial.picking_id and partial.picking_id.id or False
            boi_type = partial.picking_id and partial.picking_id.boi_type or False
            name = partial.picking_id and partial.picking_id.name or False
            if boi_type and name and picking_id:
                name = '%s-%s'%(boi_type,name)
                picking_obj.write(cr, uid, [picking_id], {'name': name}, context=context)
        return result

    def _partial_move_for(self, cr, uid, move):
        context = {}
        available_product_quantity = 0.0
        move_product_quantity = 0.0
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        prepare_partial_move = super(stock_partial_picking, self)._partial_move_for(cr, uid, move)

        # If not bom move or not BOI
        if move.picking_id and not move.picking_id.is_bom_move or move.picking_id.boi_type != 'BOI':
            return prepare_partial_move

        # Check bol location > 0
        boi_location = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')])
        if len(boi_location) == 0:
            raise osv.except_osv(_('Error!'), _('No FC_RM_BOI location !'))

        # Check product qty in stock FC_RM_BOI of each product
        product_id = move.product_id and move.product_id.id or False
        context.update({
            'states': ['done'],
            'what': ['in','out'],
            'location': boi_location
        })
        if product_id:
            available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
            if available_product_detail.values():
                available_product_quantity = available_product_detail.values()[0]

        # Compare between product qty in stock and move product qty
        compare = float_compare(move.product_qty, available_product_quantity, 3)
        if compare >= 0:
            move_product_quantity = round(available_product_quantity, 2)
        else:
            move_product_quantity = round(move.product_qty, 2)
        prepare_partial_move.update({'quantity': move_product_quantity if move.state == 'assigned' else 0})
        return prepare_partial_move

stock_partial_picking()
