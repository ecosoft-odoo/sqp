# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools.translate import _


class account_invoice(osv.Model):
    _inherit = "account.invoice"

    def invoice_validate(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context=context):
            orders = invoice.sale_order_ids
            if orders and orders[0].advance_type == "advance" and \
               orders[0].invoiced_rate == 100 and not invoice.is_advance:
                diff = 0
                for inv in orders[0].invoice_ids:
                    if inv.is_advance:
                        diff += inv.amount_net
                    else:
                        diff -= inv.amount_advance
                if diff:
                    raise osv.except_osv(
                        _("Error!"), _("Advance Amt is wrong, please check."))
        return super(account_invoice, self).invoice_validate(
            cr, uid, ids, context=context)
