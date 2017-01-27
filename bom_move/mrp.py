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

from osv import osv, fields


class mrp_production(osv.osv):

    _inherit = 'mrp.production'
    #
    # def action_confirm(self, cr, uid, ids, context=None):
    #     # query record from mrp_production
    #     for production in self.browse(cr, uid, ids):
    #         if not production.parent_id:
    #             # Map data between mrp_production and stock_picking
    #             name = self.pool.get('stock.picking').pool.get('ir.sequence').get(cr, uid, 'bom.move')
    #             data = {
    #                 'name': name,
    #                 'partner_id': production.partner_id.id,
    #                 'ref_mo_id': production.id,
    #                 'origin': production.name,
    #                 'ref_order_id': production.order_id.id,
    #                 'is_bom_move': True,
    #                 'type': 'out',
    #             }
    #             # Create data into stock picking
    #             stock_picking = self.pool.get('stock.picking').create(cr, uid, data, context)
    #     res = super(mrp_production, self).action_confirm(cr, uid, ids, context)
    #     return res
    #
    # def action_view_sqp_bom_move(self, cr, uid, ids, context=None):
    #     '''
    #     This function returns an action that display Bom Moves of given bom move ids. It can either be a in a list or in a form view
    #     '''
    #     if context is None:
    #         context = {}
    #     mod_obj = self.pool.get('ir.model.data')
    #     act_obj = self.pool.get('ir.actions.act_window')
    #
    #     result = mod_obj.get_object_reference(cr, uid, 'bom_move', 'action_picking_tree')
    #     id =  result and result[1] or False
    #     result = act_obj.read(cr, uid, [id], context=context)[0]
    #
    #     # compute the number of bom moves to display
    #     bom_move_ids = []
    #     stock_picking = self.pool.get('stock.picking')
    #     mrp_production =  self.browse(cr, uid, ids)
    #     mo_name = mrp_production[0].name
    #     bom_move_ids = stock_picking.search(cr, uid, [('origin','=',mo_name),('is_bom_move','=',True),('type','=','out')])
    #
    #     #choose the view_mode accordingly
    #     res_tree = mod_obj.get_object_reference(cr, uid, 'stock', 'view_picking_out_tree')
    #     res_form = mod_obj.get_object_reference(cr, uid, 'stock', 'view_picking_out_form')
    #     res_calendar = mod_obj.get_object_reference(cr, uid, 'stock', 'stock_picking_out_calendar')
    #     result['domain'] = "[('id','in',["+','.join(map(str, bom_move_ids))+"])]"
    #     result['views'] = [(res_tree and res_tree[1] or False, 'tree'), (res_form and res_form[1] or False, 'form'), (res_calendar and res_calendar[1] or False, 'calendar')]
    #     result['res_id'] = bom_move_ids and bom_move_ids[0] or False
    #     return result

mrp_production()
