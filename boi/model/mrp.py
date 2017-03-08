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
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mrp.production')
            order_obj = self.pool.get('sale.order')
            if vals.get('order_id', False):
                order = order_obj.browse(cr, uid, vals.get('order_id'), context=context)
                if order.product_tag_id:
                    if order.product_tag_id.name == 'BOI':
                        vals['name'] = '%s-%s'%('BOI',vals.get('name'))
                    else:
                        vals['name'] = '%s-%s'%('NONBOI',vals.get('name'))
        return super(mrp_production, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
        res = super(mrp_production, self).copy(cr, uid, id, default=default, context=context)
        if res:
            production = self.browse(cr, uid, res, context=context)
            if production.order_id:
                if production.order_id.product_tag_id:
                    if production.order_id.product_tag_id.name == 'BOI':
                        boi_type = 'BOI'
                    else:
                        boi_type = 'NONBOI'
                    name = '%s-%s'%(boi_type,production.name)
                    self.write(cr, uid, [res], {'name': name}, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            order_obj = self.pool.get('sale.order')
            boi_type = False
            for production in self.browse(cr, uid, ids, context=context):
                if vals.get('order_id', False):
                    order = order_obj.browse(cr, uid, vals.get('order_id'), context=context)
                    if order.product_tag_id:
                        if order.product_tag_id.name == 'BOI':
                            boi_type = 'BOI'
                        else:
                            boi_type = 'NONBOI'
                if boi_type:
                    if production.name.find(boi_type) < 0:
                        if production.name.find('BOI') >= 0 and boi_type == 'NONBOI':
                            name = production.name.replace('BOI', 'NONBOI')
                        else:
                            name = '%s-%s'%(boi_type,production.name)
                    else:
                        if production.name.find('NONBOI') >=0 and boi_type == 'BOI':
                            name = production.name.replace('NONBOI', 'BOI')
                        else:
                            name = production.name
                    vals.update({'name': name})
        return super(mrp_production, self).write(cr, uid, ids, vals, context=context)

    def _create_picking(self, cr, uid, production, production_lines, picking_id=False, context=None):
        if context is None:
            context = {}
        res = super(mrp_production, self)._create_picking(cr, uid, production, production_lines, picking_id=picking_id, context=context)
        if res:
            picking_obj = self.pool.get('stock.picking')
            picking = picking_obj.browse(cr, uid, res, context=context)
            if production.order_id:
                if production.order_id.product_tag_id:
                    if production.order_id.product_tag_id.name == 'BOI':
                        boi_type = 'BOI'
                    else:
                        boi_type = 'NONBOI'
                    boi_number_id = production.order_id.boi_number_id.id
                    name = '%s-%s'%(boi_type,picking.name)
                    picking_obj.write(cr, uid, res, {'name': name, 'boi_type': boi_type, 'boi_number_id': boi_number_id}, context=context)
        return res

    def _create_bom_picking(self, cr, uid, production, context=None):
        if context is None:
            context = {}
        res = super(mrp_production, self)._create_bom_picking(cr, uid, production, context=context)
        if res:
            picking_obj = self.pool.get('stock.picking')
            picking = picking_obj.browse(cr, uid, res, context=context)
            if production.order_id:
                if production.order_id.product_tag_id:
                    if production.order_id.product_tag_id.name == 'BOI':
                        boi_type = 'BOI'
                    else:
                        boi_type = 'NONBOI'
                    boi_number_id = production.order_id.boi_number_id.id
                    name = '%s-%s'%(boi_type,picking.name)
                    picking_obj.write(cr, uid, res, {'name': name, 'boi_type': boi_type, 'boi_number_id': boi_number_id}, context=context)
        return res

    def _prepare_stock_move(self, cr, uid, move_line, picking_id, production, context=None):
        if context is None:
            context = {}
        location_obj = self.pool.get('stock.location')
        location_ids = location_obj.search(cr, uid, [('name','=','FC_RM_BOI')], context=context)
        result = super(mrp_production, self)._prepare_stock_move(cr, uid, move_line, picking_id, production, context=context)
        if result:
            production_parent = self.browse(cr, uid, production.parent_id.id, context=context)
            if production_parent.order_id:
                if production_parent.order_id.product_tag_id:
                    if production_parent.order_id.product_tag_id.name == 'BOI':
                        if len(location_ids) > 0:
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
            if order.product_tag_id:
                if order.product_tag_id.name == 'BOI':
                    insulation_ids = self.search(cr, user, [('name', '=', 'PIR')] + args, limit=limit, context=context)
        return self.name_get(cr, user, insulation_ids, context=context)

bom_choice_insulation()
