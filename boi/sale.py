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

class sale_order(osv.osv):

    _inherit = 'sale.order'

    _columns = {
        'boi_number_id': fields.many2one('boi.certificate', 'BOI Number'),
        'is_boi': fields.boolean('BOI', default=False),
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
            tag_obj = self.pool.get('product.tag')
            tag = tag_obj.browse(cr, uid, vals.get('product_tag_id'), context=context)
            if tag.name == 'BOI':
                boi_type = 'BOI'
            else:
                boi_type = 'NONBOI'
            vals.update({'name': '%s-%s'%(boi_type, vals.get('name'))})
        return super(sale_order, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
        res = super(sale_order, self).copy(cr, uid, id, default, context=context)
        if res:
            order = self.browse(cr, uid, res, context=context)
            if order.product_tag_id:
                if order.product_tag_id.name == 'BOI':
                    boi_type = 'BOI'
                else:
                    boi_type = 'NONBOI'
                name = '%s-%s'%(boi_type,order.name)
                self.write(cr, uid, res, {'name': name}, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if not isinstance(ids, list):
            ids = [ids]
        if vals.get('name', '/') == '/':
            tag_obj = self.pool.get('product.tag')
            for order in self.browse(cr, uid, ids, context=context):
                if vals.get('product_tag_id', False):
                    product_tag_id = vals.get('product_tag_id')
                else:
                    product_tag_id = order.product_tag_id.id
                tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
                if tag.name == 'BOI':
                    boi_type = 'BOI'
                else:
                    boi_type = 'NONBOI'
                if order.name.find(boi_type) < 0:
                    if order.name.find('BOI') >= 0 and boi_type == 'NONBOI':
                        name = order.name.replace('BOI', 'NONBOI')
                    else:
                        name = '%s-%s'%(boi_type,order.name)
                else:
                    if order.name.find('NONBOI') >= 0 and boi_type == 'BOI':
                        name = order.name.replace('NONBOI', 'BOI')
                    else:
                        name = order.name
                vals.update({'name': name})
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    def action_button_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
        order = self.browse(cr, uid, ids[0])
        if order.product_tag_id and order.product_tag_id.name == 'BOI':
            boi_type = 'BOI'
        else:
            boi_type = 'NONBOI'
        if boi_type:
            if order.name.find(boi_type) < 0:
                if order.name.find('BOI') >= 0 and boi_type == 'NONBOI':
                    name = order.name.replace('BOI', 'NONBOI')
                else:
                    name = '%s-%s'%(boi_type,order.name)
            else:
                if order.name.find('NONBOI') >= 0 and boi_type == 'BOI':
                    name = order.name.replace('NONBOI', 'BOI')
                else:
                    name = order.name
        self.write(cr, uid, ids[0], {'name': name}, context=context)

    def _prepare_order_picking(self, cr, uid, order, context=None):
        if context is None:
            context = {}
        res = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        if order.product_tag_id:
            if order.product_tag_id.name == 'BOI':
                boi_type = 'BOI'
            else:
                boi_type = 'NONBOI'
            boi_number_id = order.boi_number_id and order.boi_number_id.id or False
            res.update({'boi_type': boi_type, 'boi_number_id': boi_number_id, 'name': '%s-%s'%(boi_type,res.get('name'))})
        return res

    def onchange_product_tag_id(self, cr, uid, ids, product_tag_id, context=None):
        if context is None:
            context = {}
        tag_obj = self.pool.get('product.tag')
        is_boi = False
        if product_tag_id:
            tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
            if tag.name == 'BOI':
                is_boi = True
            else:
                is_boi = False
        return {'value': {'is_boi': is_boi, 'boi_number_id': False}}

sale_order()
