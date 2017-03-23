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

class stock_partial_picking(osv.osv_memory):

    _inherit = 'stock.partial.picking'

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(stock_partial_picking, self).default_get(cr, uid, fields, context=context)
        picking_obj = self.pool.get('stock.picking')
        picking_ids = context.get('active_ids', [])
        active_model = context.get('active_model')
        if not picking_ids or len(picking_ids) != 1:
            return res
        assert active_model in ('stock.picking', 'stock.picking.in', 'stock.picking.out'), 'Bad context propagation'
        for picking in picking_obj.browse(cr, uid, picking_ids, context=context):
            if picking.is_bom_move and picking.boi_type == 'BOI':
                move_ids = res.get('move_ids', [])
                move_ids = [move_id for move_id in move_ids if move_id != {}]
                res.update(move_ids=move_ids)
        return res

    def do_partial(self, cr, uid, ids, context=None):
        result = super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        move_obj = self.pool.get('stock.move')
        partial = self.browse(cr, uid, ids[0], context=context)
        picking_id = partial.picking_id and partial.picking_id.id or False
        if picking_id:
            boi_type = partial.picking_id.boi_type
            is_bom_move = partial.picking_id.is_bom_move
            if boi_type:
                name = partial.picking_id.name
                name = '%s-%s'%(boi_type,name)
                picking_obj.write(cr, uid, [picking_id], {'name': name}, context=context)
            if is_bom_move:
                picking_obj.write(cr, uid, [picking_id], {'state': 'draft'}, context=context)
                move_ids = move_obj.search(cr, uid, [('picking_id','=',picking_id)], context=context)
                move_obj.write(cr, uid, move_ids, {'state': 'draft'}, context=context)
        return result

    def _partial_move_for(self, cr, uid, move):
        context = {}
        prepare_partial_move = super(stock_partial_picking, self)._partial_move_for(cr, uid, move)
        picking_obj = self.pool.get('stock.picking')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        boi_location = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')])
        product_id = move.product_id and move.product_id.id or False
        context.update({
            'states': ['done'],
            'what': ['in','out'],
            'location': boi_location
        })
        available_product_quantity = 0.0
        product_qty = 0.0
        if product_id:
            available_product_detail = product_obj.get_product_available(cr, uid, [product_id], context=context)
            if available_product_detail.values():
                available_product_quantity = available_product_detail.values()[0]
        picking_ids = context.get('active_ids', [])
        for picking in picking_obj.browse(cr, uid, picking_ids):
            if not picking.is_bom_move or picking.boi_type != 'BOI':
                return prepare_partial_move
            if available_product_quantity == 0:
                return {}
            compare = float_compare(move.product_qty, available_product_quantity, 3)
            if compare >= 0:
                product_qty = available_product_quantity
            else:
                product_qty = move.product_qty
            prepare_partial_move = self._prepare_partial_move(cr, uid, move, product_qty)
        return prepare_partial_move

    def _prepare_partial_move(self, cr, uid, move, product_qty, context=None):
        prepare_partial_move = {
            'product_id' : move.product_id.id,
            'quantity' : product_qty if move.state == 'assigned' or move.picking_id.type == 'in' else 0,
            'product_uom' : move.product_uom.id,
            'prodlot_id' : move.prodlot_id.id,
            'move_id' : move.id,
            'location_id' : move.location_id.id,
            'location_dest_id' : move.location_dest_id.id,
            'currency': move.picking_id and move.picking_id.company_id.currency_id.id or False,
        }
        return prepare_partial_move

stock_partial_picking()
