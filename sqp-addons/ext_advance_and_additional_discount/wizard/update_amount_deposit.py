# -*- coding: utf-8 -*-

import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields


class update_amount_deposit(osv.osv_memory):
    _name = "update.amount.deposit"

    _columns = {
        "amount_deposit": fields.float(
            string="Deposit Amt",
            required=True,
            digits_compute=dp.get_precision("Account"),
        ),
        "tax_line": fields.one2many(
            "update.account.invoice.tax",
            "update_deposit_id",
            string="Tax Line",
        )
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(update_amount_deposit, self).default_get(
            cr, uid, fields, context=context)
        active_id = context.get("active_id")
        invoice = self.pool.get("account.invoice").browse(
            cr, uid, active_id, context=context)
        res.update({
            "amount_deposit": invoice.amount_deposit,
            "tax_line": [
                (0, 0, {
                    "tax_id": tax.id,
                    "base": tax.base,
                    "amount": tax.amount}) for tax in invoice.tax_line]
        })
        return res

    def update_amount_deposit(self, cr, uid, ids, context=None):
        active_id = context.get("active_id")
        invoice = self.pool.get("account.invoice").browse(
            cr, uid, active_id, context=context)
        wizards = self.browse(cr, uid, ids, context=context)
        # Deposit Amt
        amount_deposit = wizards[0].amount_advance
        # Before Taxes
        amount_beforetax = invoice.amount_net - amount_deposit - \
            invoice.amount_advance
        # Tax
        amount_tax = sum([
            line.amount for line in wizards[0].tax_line
            if not line.tax_id.is_wht])
        # Before Retention
        amount_beforeretention = amount_beforetax + amount_tax
        # Total
        amount_total = amount_beforeretention - invoice.amount_retention
        # Update invoice
        cr.execute("""
            update account_invoice
            set amount_deposit = %s, amount_beforetax = %s, amount_tax = %s,
                amount_beforeretention = %s, amount_total = %s
            where id = %s
        """, (amount_deposit, amount_beforetax, amount_tax,
              amount_beforeretention, amount_total, active_id))
        # Update tax line
        cur_obj = self.pool.get('res.currency')
        for line in wizards[0].tax_line:
            base_amount = cur_obj.compute(
                cr, uid, invoice.currency_id.id,
                invoice.company_id.currency_id.id, line.base,
                context={
                    "date": invoice.date_invoice or
                    fields.date.context_today(
                        self, cr, uid, context=context)}, round=False)
            base_amount = cur_obj.round(
                cr, uid, invoice.currency_id, base_amount)
            tax_amount = cur_obj.compute(
                cr, uid, invoice.currency_id.id,
                invoice.company_id.currency_id.id, line.amount,
                context={
                    "date": invoice.date_invoice or
                    fields.date.context_today(
                        self, cr, uid, context=context)}, round=False)
            tax_amount = cur_obj.round(
                cr, uid, invoice.currency_id, tax_amount)
            cr.execute("""
                update account_invoice_tax
                set base = %s, base_amount = %s, amount = %s, tax_amount = %s
                where id = %s
            """, (line.base, base_amount, line.amount, tax_amount,
                  line.tax_id.id))


class update_account_invoice_tax(osv.osv_memory):
    _inherit = "update.account.invoice.tax"

    _columns = {
        "tax_id": fields.many2one(
            "account.invoice.tax",
            string="Tax",
        ),
        "base": fields.float(
            string="Base",
            digits_compute=dp.get_precision("Account"),
        ),
        "amount": fields.float(
            string="Amount",
            digits_compute=dp.get_precision("Account"),
        ),
        "update_deposit_id": fields.many2one(
            "update.amount.deposit",
        )
    }
