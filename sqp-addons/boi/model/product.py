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
        if context.get('order_id', False):
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, user, context.get('order_id'), context=context)
            product_tag_id = order.product_tag_id.id
            is_international = order.is_international
            partner_id = order.partner_id.id
            if order.product_tag_id and order.product_tag_id.name == 'BOI' and context.get('bom_template_id', False):
                product_ids = self.search(cr, user, [('is_international','=',is_international),('tag_ids','in',product_tag_id),'|',('partner_id','=',False),('partner_id','=',partner_id)] + args, limit=limit, context=context)
            else:
                return False
        else:
            if context.get('order_id', True) == False:
                return False
            product_ids = self.search(cr, user, args, context=context)
        return self.name_get(cr, user, product_ids, context=context)

product_product()
