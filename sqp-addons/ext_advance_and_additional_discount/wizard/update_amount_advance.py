# -*- coding: utf-8 -*-

import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields


class update_amount_advance(osv.osv_memory):
    _name = "update.amount.advance"

    _columns = {
        "amount_advance": fields.float(
            string="Advance Amt",
            required=True,
            digits_compute=dp.get_precision("Account"),
        )
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(update_amount_advance, self).default_get(
            cr, uid, fields, context=context)
        active_id = context.get("active_id")
        invoice = self.pool.get("account.invoice").browse(
            cr, uid, active_id, context=context)
        res["amount_advance"] = invoice.amount_advance
        return res

    def update_amount_advance(self, cr, uid, ids, context=None):
        active_id = context.get("active_id")
        invoice = self.pool.get("account.invoice").browse(
            cr, uid, active_id, context=context)
        wizards = self.browse(cr, uid, ids, context=context)
        diff_amount_advance = \
            wizards[0].amount_advance - invoice.amount_advance
        cr.execute("""
            update account_invoice
            set amount_advance = %s, amount_beforetax = %s,
                amount_beforeretention = %s, amount_total = %s
            where id = %s
        """, (wizards[0].amount_advance,
              invoice.amount_beforetax - diff_amount_advance,
              invoice.amount_beforeretention - diff_amount_advance,
              invoice.amount_total - diff_amount_advance,
              active_id))
