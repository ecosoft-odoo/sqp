# -*- coding: utf-8 -*-
from osv import osv, fields
from lxml import etree
import openerp.addons.decimal_precision as dp


class product_stock_balance(osv.osv):
    _inherit = 'product.product'

    def qty_stock_balance(self, cr, uid, ids, field_names=None, arg=False,
                          context=None):
        if not field_names:
            field_names = []
        if context is None:
            context = {}
        res = {}
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0.0)
        for f in field_names:
            c = context.copy()
            if f == 'qty_stock_balance':
                c.update({'states': ('done',), 'what': ('in', 'out')})
            stock = self.get_product_available(cr, uid, ids, context=c)
            for id in ids:
                res[id][f] = stock.get(id, 0.0)
        return res

    def amount_stock_balance(self, cr, uid, ids, field_names=None,
                             arg=False, context=None):
        res = dict.fromkeys(ids, 0.0)
        for product in self.browse(cr, uid, ids, context=context):
            res[product.id] = \
                product.qty_stock_balance * product.standard_price
        return res

    _columns = {
        'qty_stock_balance': fields.function(
            qty_stock_balance,
            multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='On Hand',
        ),
        'amt_stock_bal': fields.function(
            amount_stock_balance,
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='On Hand',
        ),
    }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        res = super(product_stock_balance, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)
        if context is None:
            context = {}
        if context.get('is_stock_balance_report', False):
            root = etree.fromstring(res['arch'])
            root.set('create', 'false')
            root.set('edit', 'false')
            root.set('delete', 'false')
            res['arch'] = etree.tostring(root)
        return res
