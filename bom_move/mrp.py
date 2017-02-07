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

LOCATION_FC_RM = 15
LOCATION_PRODUCTION = 7


class mrp_production(osv.osv):

    _inherit = 'mrp.production'

    def _mrp_bom_move_exists(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for production in self.browse(cursor, user, ids, context=context):
            res[production.id] = False
            cursor.execute("""
                select count(1) from stock_picking
                where ref_mo_id = %s""", (production.id,))
            if cursor.fetchone()[0]:
                res[production.id] = True
        return res

    _columns = {
        'mrp_bom_move_exists': fields.function(
            _mrp_bom_move_exists, string='MO Exists', type='boolean',
            help="It indicates that MO has at least one child."),
    }

    def action_confirm(self, cr, uid, ids, context=None):
        uncompute_ids = filter(lambda x: x,
                               [not x.product_lines and x.id or False
                                for x in self.browse(cr, uid, ids,
                                                     context=context)])
        self.action_compute(cr, uid, uncompute_ids, context=context)
        res = super(mrp_production, self).action_confirm(cr, uid, ids, context)
        picking_id = False
        move_list = []
        for production in self.browse(cr, uid, ids):
            if production.parent_id:
                continue
            picking_id = self._create_bom_picking(cr, uid, production, context)
            production_ids = self.search(
                cr, uid, [('parent_id', '=', ids[0])], context)
            for production in self.browse(cr, uid, production_ids):
                move_list = self._stock_move_list(
                    cr, uid, production, picking_id, move_list, context)
            move_list = self._sum(cr, uid, move_list, context)
            self._create_stock_move(cr, uid, move_list, context)
        return res

    def _create_bom_picking(self, cr, uid, production, context=None):
        picking_obj = self.pool.get('stock.picking')
        picking_data = self._prepare_picking(cr, uid, production, context)
        picking_id = picking_obj.create(cr, uid, picking_data, context)
        return picking_id

    def _prepare_picking(self, cr, uid, production, context=None):
        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'bom.move')
        return {
            'name': pick_name,
            'origin': production.name,
            'type': 'out',
            'state': 'draft',
            'partner_id': production.partner_id.id,
            'note': production.note,
            'is_bom_move': True,
            'ref_mo_id': production.id,
            'ref_order_id': production.order_id.id,
            'ref_project_name': production.product_id.name_template,
            'is_printed': production.is_printed,
        }

    def _stock_move_list(self, cr, uid, production,
                         picking_id, move_list, context=None):
        for move_line in production.move_lines:
            move_data = self._prepare_stock_move(cr, uid, move_line,
                                                 picking_id, production,
                                                 context)
            move_list.append(move_data)
        return move_list

    def _prepare_stock_move(self, cr, uid, move_line,
                            picking_id, production, context=None):
        return {
            'picking_id': picking_id,
            'product_uom': move_line.product_uom.id,
            'name': move_line.product_id.name,
            'product_id': move_line.product_id.id,
            # 'location_id': move_line.location_id.id,
            # 'location_dest_id': move_line.location_dest_id.id,
            'location_id': LOCATION_FC_RM,
            'location_dest_id': LOCATION_PRODUCTION,
            'product_qty': move_line.product_qty,
            'product_uos_qty': move_line.product_uos_qty,
            'product_uos': move_line.product_uos,
            'order_qty': move_line.order_qty,
        }

    def _sum(self, cr, uid, move_list, context):
        result_list = []
        product_dict = {}
        for move_line in move_list:
            picking_id = move_line['picking_id']
            product_uom = move_line['product_uom']
            name = move_line['name']
            product_id = move_line['product_id']
            location_id = move_line['location_id']
            location_dest_id = move_line['location_dest_id']
            product_qty = move_line['product_qty']
            product_uos_qty = move_line['product_uos_qty']
            product_uos = move_line['product_uos']
            order_qty = move_line['order_qty']
            if product_id in product_dict:
                pos = product_dict[product_id]
                result_list[pos] = {
                    'picking_id': picking_id,
                    'product_uom': product_uom,
                    'name': name,
                    'product_id': product_id,
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'order_qty': (result_list[pos]['order_qty'] +
                            order_qty),
                    'product_qty': (result_list[pos]['product_qty'] +
                                    product_qty),
                    'product_uos_qty': (result_list[pos]['product_uos_qty'] +
                                        product_uos_qty),
                    'product_uos': product_uos,
                    }
            else:
                result_list.append(move_line)
                product_dict[product_id] = len(result_list) - 1
        return result_list

    def _create_stock_move(self, cr, uid, move_list, context):
        move_obj = self.pool.get('stock.move')
        for move_line in move_list:
            move_obj.create(cr, uid, move_line, context)
        return True

    def action_view_sqp_bom_move(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display Bom Moves of given
        bom move ids. It can either be a in a list or in a form view
        '''
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'bom_move',
                                              'action_bom_move_tree')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]

        # compute the number of bom moves to display
        bom_move_ids = []
        stock_picking = self.pool.get('stock.picking')
        for production in self.browse(cr, uid, ids):
            if not production.parent_id:
                mo_name = production.name
                break
        bom_move_ids = stock_picking.search(cr, uid,
                                            [('origin', '=', mo_name),
                                             ('is_bom_move', '=', True),
                                             ('type', '=', 'out')])

        # choose the view_mode accordingly
        res_tree = mod_obj.get_object_reference(
            cr, uid, 'stock', 'view_picking_out_tree')
        res_form = mod_obj.get_object_reference(
            cr, uid, 'stock', 'view_picking_out_form')
        res_calendar = mod_obj.get_object_reference(
            cr, uid, 'stock', 'stock_picking_out_calendar')
        result['domain'] = \
            "[('id','in',["+','.join(map(str, bom_move_ids))+"])]"
        result['views'] = \
            [(res_tree and res_tree[1] or False, 'tree'),
             (res_form and res_form[1] or False, 'form'),
             (res_calendar and res_calendar[1] or False, 'calendar')]
        result['res_id'] = bom_move_ids and bom_move_ids[0] or False
        return result

    def action_cancel(self, cr, uid, ids, context=None):
        res = super(mrp_production, self).action_cancel(cr, uid, ids, context)
        picking_obj = self.pool.get('stock.picking')
        cr.execute("select id from stock_picking where is_bom_move = true and type = 'out'")
        bom_move = cr.fetchall()
        if len(bom_move) == 1:
            for production in self.browse(cr, uid, ids):
                mo_name = production.name
            picking = picking_obj.browse(cr, uid, bom_move[0][0])
            ref_mo_name = picking.ref_mo_id.name
            state = picking.state
            if mo_name == ref_mo_name and state == 'draft':
                picking_obj.write(cr, uid, bom_move[0][0], {'state': 'cancel'})
        return res

mrp_production()
