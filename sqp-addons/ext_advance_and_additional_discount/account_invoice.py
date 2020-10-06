# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def action_check_amount_advance(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context=context):
            orders = invoice.sale_order_ids
            if orders and orders[0].advance_type == "advance" and \
               orders[0].invoiced_rate >= 100 and not invoice.is_advance:
                cr.execute("""
                    select sum(
                        case when is_advance = True then amount_net
                        else -amount_advance end) as diff
                    from account_invoice
                    where id in %s and state not in ('cancel')
                """, (tuple([inv.id for inv in orders[0].invoice_ids]), ))
                diff = map(lambda l: l[0], cr.fetchall())[0]
                if round(diff, 2):
                    raise osv.except_osv(
                        _("Error!"), _("Advance Amt is wrong, please check."))
