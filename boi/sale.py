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
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_number_id': fields.many2one('boi.certificate', 'BOI Number'),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('product_tag_id', True) == False:
            raise osv.except_osv(_('Warning!'),_("Please add product tags is BOI"))
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
        vals.update({'name': vals.get('boi_type', '') + '-' + vals.get('name', '')})
        return super(sale_order, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('product_tag_id', True) == False:
            raise osv.except_osv(_('Warning!'),_("Please add product tags is BOI"))
        if not isinstance(ids, list):
            ids = [ids]
        for order in self.browse(cr, uid, ids, context=context):
            if vals.get('boi_type', True):
                if vals.get('boi_type', False):
                    boi_type = vals.get('boi_type')
                else:
                    boi_type = order.boi_type
                if order.name.find(boi_type) < 0:
                    if order.name.find('BOI') >= 0 and boi_type == 'NONBOI':
                        name = order.name.replace('BOI', 'NONBOI')
                    else:
                        name = boi_type + '-' + order.name
                else:
                    if order.name.find('NONBOI') >= 0 and boi_type == 'BOI':
                        name = order.name.replace('NONBOI', 'BOI')
                    else:
                        name = order.name
                if 'name' not in vals:
                    vals.update({'name': name})
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        res.update({'boi_type': order.boi_type, 'boi_number_id': order.boi_number_id.id, 'name': order.boi_type + '-' + res.get('name', '')})
        return res

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        if boi_type == 'BOI':
            tag_obj = self.pool.get('product.tag')
            tag_ids = tag_obj.search(cr, uid, [('name','=','BOI'),('active','=',True)], context=context)
            if tag_ids != []:
                product_tag_id = tag_ids[0]
            else:
                product_tag_id = False
        else:
            product_tag_id = False
        return {'value': {'boi_number_id': False, 'product_tag_id': product_tag_id}}

sale_order()
