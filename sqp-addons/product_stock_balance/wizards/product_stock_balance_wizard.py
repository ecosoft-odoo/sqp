# -*- coding: utf-8 -*-
from osv import osv, fields


class product_stock_balance_wizard(osv.osv_memory):
    _name = 'product.stock.balance.wizard'

    _columns = {
        'period_id': fields.many2one(
            'account.period',
            string='As of Period',
            required=True,
        ),
        'categ_ids': fields.many2many(
            'product.category',
            'product_category_rel',
            'product_id',
            'categ_id',
            string='Product Categories',
            domain="[('type', '!=', 'view')]",
        ),
        'location_id': fields.many2one(
            'stock.location',
            'Location',
            domain=[('usage', '=', 'internal')],
        ),
    }

    _defaults = {
        'period_id': lambda self, cr, uid, context:
            self.pool.get('account.period').find(cr, uid),
    }

    def run_report(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(
            cr, uid, 'product_stock_balance', 'action_product_stock_balance')
        xml_id = result and result[1] or False
        result = act_obj.read(cr, uid, [xml_id], context=context)[0]

        # Define domain and context
        to_date, location_id, categ_ids = False, False, []
        stock_balance = self.browse(cr, uid, ids, context=context)[0]
        if stock_balance.period_id:
            to_date = stock_balance.period_id.date_stop
        if stock_balance.location_id:
            location_id = stock_balance.location_id.id
        categ_ids = list(set([categ.id for categ in stock_balance.categ_ids]))
        if categ_ids:
            result['domain'] = [('categ_id', 'in', categ_ids)]
        result['context'] = {
            'is_stock_balance_report': True,
            'to_date': to_date,
            'location': location_id,
        }
        return result
