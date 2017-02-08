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


class boi_template_line(osv.osv):
    _name = 'boi.template.line'

    _columns = {
        'boi_id': fields.many2one('boi.template', 'Boi'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'categ_id': fields.many2one('product.category', 'Category', required=True),
        'uom_id': fields.many2one('product.uom', 'UOM', required=True),
        'quantity': fields.float('Quantity', required=True),
        'remark': fields.char('Remark'),
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context):
        if not product_id:
            return {'value': {'categ_id': False, 'uom_id': False}}
        product = self.pool.get('product.product').browse(cr, uid, product_id, context)
        val = {
            'categ_id': product.categ_id.id,
            'uom_id': product.uom_id.id,
        }
        return {'value': val}

boi_template_line()

class boi_template(osv.osv):
    _name = 'boi.template'

    _columns = {
        'boi': fields.char('Boi', size=64, required=True),
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'boi_lines': fields.one2many('boi.template.line', 'boi_id', 'Boi Line'),
    }
boi_template()
