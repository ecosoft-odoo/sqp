# -*- coding: utf-8 -*-
from osv import osv, fields

_NON_STD_CATEG = ['000006', '000036']


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def _compute_non_standard(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = False
            for line in invoice.invoice_line:
                print line.product_id.categ_id
                search_key = line.product_id and line.product_id.categ_id and \
                    line.product_id.categ_id.search_key
                if search_key in _NON_STD_CATEG:
                    res[invoice.id] = True
        return res

    _columns = {
        'non_standard': fields.function(
            _compute_non_standard, type='boolean', string='Non-Standard',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}:
                                    ids, ['invoice_line'], 20),
            }),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
