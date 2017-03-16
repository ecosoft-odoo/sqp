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

import netsvc
from osv import osv, fields

class product_product(osv.osv):

    _inherit = "product.product"
    _columns = {
        'tag_ids': fields.many2many('product.tag', string='Tags', help="Tagged products are products to be shown in Sales Order."),
        'partner_id': fields.many2one('res.partner', 'Product Customer', help="Specify customer that this product belongs to (not share with others)"),
    }
product_product()


class product_tag(osv.osv):
    _description = 'Product Tags'
    _name = 'product.tag'
    _order = 'name'
    _columns = {
        'name': fields.char('Product Tag Name', size=128, required=True),
        'note': fields.text('Notes'),
        'product_ids': fields.many2many('product.product', string='Products'),
        'active': fields.boolean('Active')
    }

product_tag()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
