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
import time
import netsvc
from osv import osv, fields
import openerp.addons.decimal_precision as dp
from tools.translate import _


class purchase_order(osv.osv):

    _inherit = 'purchase.order'

    _columns = {
        'is_subcontract': fields.boolean('Subcontract', readonly=False, change_default=True),
        'sale_order_id': fields.many2one('sale.order', 'Copy SO Lines', required=False, domain=[('state', '<>', 'draft')], readonly=True, states={'draft': [('readonly', False)]}),
        'ref_attention_2_id': fields.many2one('res.partner', 'Attention 2', readonly=False),
    }

    _defaults = {
        'is_subcontract': lambda s, cr, uid, c: c.get('is_subcontract', False),
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('is_subcontract', False):
            if vals.get('name', '/') == '/' or context.get('force_new_no', False):
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.subcontract') or '/'
        order = super(purchase_order, self).create(cr, uid, vals, context=context)
        return order

    def copy(self, cr, uid, id, default=None, context=None):
        ctx = context.copy()
        if context.get('is_subcontract', False):
            ctx.update({'force_new_no': True})
            default.update({'name': '/'})
        return super(purchase_order, self).copy(cr, uid, id, default, context=ctx)

    def onchange_sale_order_id(self, cr, uid, ids, sale_order_id):
        res = {'value': {'ref_order_id': False, 'order_line': []}}
        order_lines = []
        if sale_order_id:
            sale_order = self.pool.get('sale.order').browse(cr, uid, sale_order_id)
            for line in sale_order.order_line:
                rs = {
                    'state': 'draft',
                    'invoiced': False,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'date_planned': time.strftime('%Y-%m-%d'),
                    'product_so_qty': line.product_uom_qty,
                    'product_qty': 0.0,
                    'product_uom': line.product_uom.id,
                    'taxes_id': line.product_id.supplier_taxes_id and [(6, 0, map(lambda x: x.id, line.product_id.supplier_taxes_id))] or False
                }
                order_lines.append(rs)
            res['value']['order_line'] = order_lines
            res['value']['ref_order_id'] = sale_order_id
        return res

purchase_order()


class purchase_order_line(osv.osv):

    _inherit = 'purchase.order.line'
    _columns = {
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of purchase order lines."),
        'product_so_qty': fields.float('SO Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), readonly=True),
    }
    _defaults = {
        'sequence': 10,
    }
    _order = 'order_id desc, sequence, id'

purchase_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
