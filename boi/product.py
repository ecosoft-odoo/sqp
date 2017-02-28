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
        'boi_lines': fields.one2many('boi.certificate.line', 'product_id', 'BOI Certificate'),
    }

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        args = args or {}
        context = context or {}
        if context.get('order_id', False):
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, user, context.get('order_id'), context=context)
            product_tag_id = order.product_tag_id.id
            is_international = order.is_international
            partner_id = order.partner_id.id
            product_ids = self.search(cr, user, [('is_international','=',is_international),('tag_ids','in',product_tag_id),'|',('partner_id','=',False),('partner_id','=',partner_id)] + args, limit=limit, context=context)
        else:
            product_ids = self.search(cr, user, args, context=context)
        return self.name_get(cr, user, product_ids, context=context)

product_product()
