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

    def _get_name(self, cr, uid, vals, context=None):
        product_obj = self.pool.get('product.product')
        order_obj = self.pool.get('sale.order')
        name = '/'
        if vals.get('active_ids', False):
            for product in product_obj.browse(cr, uid, vals.get('active_ids')):
                if product.ref_order_id:
                    name = self.pool.get('ir.sequence').get(cr, uid, 'mrp.production')
                    tag_name = product.ref_order_id.product_tag_id and product.ref_order_id.product_tag_id.name or False
                    name = (tag_name == 'BOI') and ('%s-%s'%('BOI',name)) or ('%s-%s'%('NONBOI',name))
        return name

    _defaults = {
        'name': _get_name
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mrp.production') or '/'
            order_obj = self.pool.get('sale.order')
            order_id = vals.get('order_id',False)
            if order_id:
                order = order_obj.browse(cr, uid, order_id, context=context)
                boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                                and 'BOI' or 'NONBOI'
                vals.update({'name': '%s-%s'%(boi_type, vals.get('name', '/'))})
        return super(mrp_production, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        production_id = super(mrp_production, self).copy(cr, uid, id, default=default, context=context)
        production = self.browse(cr, uid, production_id, context=context)
        boi_type = (production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI') \
                        and 'BOI' or 'NONBOI'
        name = '%s-%s'%(boi_type,production.name)
        self.write(cr, uid, [production_id], {'name': name}, context=context)
        return production_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        order_id = vals.get('order_id', False)
        if order_id:
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, uid, order_id, context=context)
            boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            for production in self.browse(cr, uid, ids, context=context):
                vals['name'] = production.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(mrp_production, self).write(cr, uid, ids, vals, context=context)

    def _create_picking(self, cr, uid, production, production_lines, picking_id=False, context=None):
        picking_id = super(mrp_production, self)._create_picking(cr, uid, production, production_lines, picking_id=picking_id, context=context)
        if picking_id:
            picking_obj = self.pool.get('stock.picking')
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            boi_type = (production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            boi_cert_id = (production.order_id and production.order_id.boi_cert_id) \
                                and production.order_id.boi_cert_id.id or False
            name = '%s-%s'%(boi_type,picking.name)
            picking_obj.write(cr, uid, picking_id, {'name': name, 'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)
            return picking_id

    def _create_bom_picking(self, cr, uid, production, context=None):
        picking_id = super(mrp_production, self)._create_bom_picking(cr, uid, production, context=context)
        if picking_id:
            picking_obj = self.pool.get('stock.picking')
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            boi_type = (production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            boi_cert_id = (production.order_id and production.order_id.boi_cert_id) \
                                and production.order_id.boi_cert_id.id or False
            name = '%s-%s'%(boi_type,picking.name)
            picking_obj.write(cr, uid, picking_id, {'name': name, 'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)
        return picking_id

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
        insulation_ids = self.search(cr, user, args, limit=limit, context=context)
        if context.get('order_id', False):
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, user, context.get('order_id'), context=context)
            if order.product_tag_id and order.product_tag_id.name == 'BOI':
                insulation_ids = self.search(cr, user, [('name', '=', 'PIR')] + args, limit=limit, context=context)
            else:
                if context.get('object', 'not door') == 'door':
                    insulation_ids = self.search(cr, user, [('name', '!=', 'PIR')] + args, limit=limit, context=context)
        return self.name_get(cr, user, insulation_ids, context=context)

bom_choice_insulation()
