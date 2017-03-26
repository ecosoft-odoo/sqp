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

class product_rapid_create(osv.osv):

    _inherit = 'product.rapid.create'

    def _check_boi_name(self,cr,uid,ids):
        line_obj = self.pool.get('product.rapid.create.line')
        product_rapid_create = self.browse(cr, uid, ids)
        for create in product_rapid_create:
            quotation_type = (create.order_id and create.order_id.product_tag_id) \
                                and create.order_id.product_tag_id.name or False
            boi_type = quotation_type == 'BOI' and 'BOI' or 'NONBOI'
            if boi_type == 'BOI':
                line_ids = line_obj.search(cr, uid, [('wizard_id','=',create.id)])
                for line in line_obj.browse(cr, uid, line_ids):
                    if not line.product_id:
                        return False
        return True

    _columns = {
        'is_boi': fields.boolean('IS BOI', default=False)
    }

    _constraints = [(_check_boi_name, 'Please specific BOI Name !', ['BOI Name'])]

    def _prepare_product(self, cr, uid, ids, new_product_name, line, object, context=None):
        result = super(product_rapid_create, self)._prepare_product(cr, uid, ids, new_product_name, line, object, context=context)
        boi_product_name = line.product_id and line.product_id.name_template or False
        boi_default_code = line.product_id and line.product_id.default_code or False
        result.update({'boi_product_name': boi_product_name, 'boi_default_code': boi_default_code})
        return result

    def onchange_order_id(self, cr, uid, ids, order_id, context=None):
        order_obj = self.pool.get('sale.order')
        is_boi = False
        if order_id:
            order = order_obj.browse(cr, uid, order_id, context=context)
            boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            is_boi = boi_type == 'BOI' and True or False
        return {'value': {'is_boi': is_boi}}

product_rapid_create()


class product_rapid_create_line(osv.osv):

    _inherit = 'product.rapid.create.line'

    _columns = {
        'product_id': fields.many2one('product.product', 'BOI Name', ondelete="restrict"),
        # 'is_boi': fields.boolean('IS_BOI', default=False)
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        product_obj = self.pool.get('product.product')
        thick = False
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            thick = product.T and product.T.id or False
        return {'value': {'T': thick}}

product_rapid_create_line()
