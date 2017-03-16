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

class product_rapid_create(osv.osv):

    _inherit = 'product.rapid.create'

    def create_product(self, cr, uid, ids, context=None):
        result = super(product_rapid_create, self).create_product(cr, uid, ids, context=context)
        product_obj = self.pool.get('product.product')
        object =  self.browse(cr, uid, ids[0], context=context)
        lines = object.panel_lines + object.door_lines + object.window_lines
        if not len(lines):
            return False
        if result.get('domain', False):
            for domain in result.get('domain'):
                new_product_ids = domain[2]
        index = 0
        for line in lines:
            boi_product_name = line.product_id.name_template
            boi_default_code = line.product_id.default_code
            product_obj.write(cr, uid, [new_product_ids[index]], {'boi_product_name': boi_product_name, 'boi_default_code': boi_default_code}, context=context)
            index = index + 1
        return result

product_rapid_create()


class product_rapid_create_line(osv.osv):

    _inherit = 'product.rapid.create.line'

    _columns = {
        'product_id': fields.many2one('product.product', 'BOI Name'),
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        product_obj = self.pool.get('product.product')
        product = product_obj.browse(cr, uid, product_id, context=context)
        thick = product.T and product.T.id or False
        return {'value': {'T': thick}}

product_rapid_create_line()
