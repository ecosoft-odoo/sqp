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

class mrp_production(osv.osv):

    _inherit = 'mrp.production'

    def create(self, cr, uid, vals, context=None):
        production_id = super(mrp_production, self).create(cr, uid, vals, context=context)
        if production_id:
            production = self.browse(cr, uid, production_id, context=context)

            # Update name
            if production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI':
                boi_cert_name = (production.order_id and production.order_id.boi_cert_id) \
                                    and production.order_id.boi_cert_id.name \
                                    or 'BOI'
                name = '%s-%s'%(boi_cert_name, production.name[production.name.find('-') + 1:])
                self.write(cr, uid, [production_id], {'name': name}, context=context)
        return production_id

    def write(self, cr, uid, ids, vals, context=None):
        order_obj = self.pool.get('sale.order')
        cert_obj = self.pool.get('boi.certificate')
        order_id = vals.get('order_id', False)
        if order_id:
            order = order_obj.browse(cr, uid, order_id, context=context)
            boi_cert_name = order.boi_cert_id and order.boi_cert_id.name or 'BOI'

            # Update name
            for production in self.browse(cr, uid, ids, context=context):
                vals['name'] = (order.product_tag_id and order.product_tag_id.name == 'BOI') and '%s-%s'%(boi_cert_name, production.name[production.name.find('-') + 1:]) \
                                    or (order.product_tag_id and order.product_tag_id.name != 'BOI') and production.name[production.name.find('-') + 1:] \
                                    or production.name
        return super(mrp_production, self).write(cr, uid, ids, vals, context=context)

    def _create_picking(self, cr, uid, production, production_lines, picking_id=False, context=None):
        picking_id = super(mrp_production, self)._create_picking(cr, uid, production, production_lines, picking_id=picking_id, context=context)
        self.update_boi(cr, uid, picking_id, production, context=context)
        return picking_id

    def _create_bom_picking(self, cr, uid, production, context=None):
        picking_id = super(mrp_production, self)._create_bom_picking(cr, uid, production, context=context)
        self.update_boi(cr, uid, picking_id, production, context=context)
        return picking_id

    def update_boi(self, cr, uid, picking_id, production, context=None):
        picking_obj = self.pool.get('stock.picking')
        if picking_id:
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            name = picking.name
            boi_type = (production.order_id and production.order_id.product_tag_id.name == 'BOI') and 'BOI' or 'NONBOI'
            boi_cert_id = (production.order_id and production.order_id.boi_cert_id) and production.order_id.boi_cert_id.id or False

            # Update name
            if production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI':
                boi_cert_name = (production.order_id and production.order_id.boi_cert_id) and production.order_id.boi_cert_id.name or 'BOI'
                name = '%s-%s'%(boi_cert_name, name[name.find('-') + 1:])
            picking_obj.write(cr, uid, [picking_id], {'name': name, 'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)

    def _prepare_stock_move(self, cr, uid, move_line, picking_id, production, context=None):
        location_obj = self.pool.get('stock.location')
        location_ids = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')], context=context)
        result = super(mrp_production, self)._prepare_stock_move(cr, uid, move_line, picking_id, production, context=context)
        if result:
            production_parent = self.browse(cr, uid, production.parent_id.id, context=context)
            if production_parent.order_id and production_parent.order_id.product_tag_id and production_parent.order_id.product_tag_id.name == 'BOI' and len(location_ids) > 0:
                result.update({'location_id': location_ids[0]})
        return result

mrp_production()


class bom_choice_insulation(osv.osv):

    _inherit = 'bom.choice.insulation'

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        if context.get('order_id', False):
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, user, context.get('order_id'), context=context)
            if order.product_tag_id and order.product_tag_id.name == 'BOI':
                args = [('name', 'in', ['PIR', 'PU', 'PU(DEN80)'])] + args
            else:
                if context.get('object', 'not door') == 'door':
                    args = [('name', '!=', 'PIR')] + args
        return super(bom_choice_insulation, self).name_search(cr, user, name, args=args, operator=operator, context=context, limit=limit)

bom_choice_insulation()
