# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
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
from openerp import netsvc
from openerp.tools.translate import _


class product_item(osv.osv):
    _name = "product.item"
    _description = "Product Item for Bundle products"

    _columns = {
        'sequence': fields.integer('Sequence'),
        'product_id': fields.many2one('product.product', 'Bundle Product', ondelete='cascade', required=True),
        'item_id': fields.many2one('product.product', 'Item', required=True),
        'uom_id': fields.many2one('product.uom', 'UoM', required=True),
        'qty_uom': fields.integer('Quantity', required=True),
        #'editable': fields.boolean('Allow changes in DO ?', help="Allow the user to change this item (quantity or item itself) in the Delivery Orders."),
    }
    _defaults = {
        #'editable': lambda *a: True,
    }

    def onchange_item_id(self, cr, uid, ids, item_id, context=None):
        context = context or {}
        domain = {}
        result = {}

        if item_id:
            item = self.pool.get('product.product').browse(cr, uid, item_id, context=context)

        if item:
            result.update({'uom_id': item.uom_id.id})
            domain = {'uom_id': [('category_id', '=', item.uom_id.category_id.id)]}

        return {'value': result, 'domain': domain}

product_item()


class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
        'item_ids': fields.one2many('product.item', 'product_id', 'Item sets'),
    }

    def _validate_bundle(self, cr, uid, product_id, context=None):
        product = self.browse(cr, uid, product_id, context)
        if product.supply_method == 'bundle':
            for item in product.item_ids:
                if item.item_id.supply_method == 'bundle':
                    raise osv.except_osv(_('Product bundle exception!'),
                        _('No product bundle allowed inside this product bundle!'))

    def create(self, cr, uid, vals, context=None):
        res_id = super(product_product, self).create(cr, uid, vals, context=context)
        self._validate_bundle(cr, uid, res_id, context)
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(product_product, self).write(cr, uid, ids, vals, context=context)
        for res_id in ids:
            self._validate_bundle(cr, uid, res_id, context)
        return res

product_product()


class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'supply_method': fields.selection([('produce', 'Manufacture'), ('buy', 'Buy'), ('bundle', 'Bundle')], 'Supply Method', required=True, help="Manufacture: When procuring the product, a manufacturing order or a task will be generated, depending on the product type. \nBuy: When procuring the product, a purchase order will be generated. \nBundle: When procuring the product, a PO or MO will be generated for each item of the Bundle product (depending on their own Supply Method) but nothing for the Bundle product itself."),
    }
    _defaults = {
        'supply_method': lambda *a: 'buy',
    }
product_template()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
