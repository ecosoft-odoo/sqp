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

class product_product(osv.osv):

    _inherit = 'product.product'

    _columns = {
        'boi_lines': fields.one2many('product.product.boi.certificate', 'product_id', 'BOI Certificate'),
        'boi_product_name': fields.char('BOI Product Name'),
        'boi_default_code': fields.char('BOI Default Code'),
    }

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        product_ids = []
        if not context.get('order_id', False):
            return super(product_product, self).name_search(cr, user, name, args=args, operator=operator, context=context, limit=limit)
        else:
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, user, context.get('order_id'), context=context)
            is_international = order.is_international
            product_tag_id = order.product_tag_id and order.product_tag_id.id or False
            partner_id = order.partner_id and order.partner_id.id or False
            if order.product_tag_id and order.product_tag_id.name == 'BOI' and context.get('bom_template_id', False):
                product_ids = self.search(cr, user, [('is_international','=',is_international),('tag_ids','in',product_tag_id),'|',('partner_id','=',False),('partner_id','=',partner_id)] + args, limit=limit, context=context)
        return self.name_get(cr, user, product_ids, context=context)

product_product()
