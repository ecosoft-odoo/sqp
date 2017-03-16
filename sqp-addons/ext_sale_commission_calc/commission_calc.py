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


class commission_worksheet(osv.osv):

    _inherit = 'commission.worksheet'

    def _get_base_amount(self, invoice):
        # Case with Additional Discount
        tax_amt = 0.0
        for tax in invoice.tax_line:
            tax_amt += tax.amount
        base_amt = invoice.amount_total - tax_amt
        return base_amt

    def _prepare_worksheet_line(self, worksheet, invoice, base_amt, commission_amt, context=None):
        res = super(commission_worksheet, self)._prepare_worksheet_line(worksheet, invoice, base_amt, commission_amt, context=context)
        res.update({
            'invoice_amt': invoice.amount_total,  # For SQP, amount total will be the full amount.
            'amount_net': base_amt,  # Additional field.
        })
        return res

commission_worksheet()


class commission_worksheet_line(osv.osv):

    _inherit = 'commission.worksheet.line'

    def _check_commission_line_status(self, cr, uid, line, params, context=None):
        res = super(commission_worksheet_line, self)._check_commission_line_status(cr, uid, line, params, context=context)
        if not line.force and not line.unlocked:
            res.update({'commission_state': 'draft'})
        return res

    def _update_commission_state(self, cr, uid, line, unlocked, context=None):
        if not line.force:
            params = self._get_commission_params(cr, uid, [line.id], context=context)
            commission_state = super(commission_worksheet_line, self)._check_commission_line_status(cr, uid, line, params, context=context)['commission_state']
            if not unlocked:
                commission_state = 'draft'
            if commission_state != line.commission_state:
                cr.execute('update commission_worksheet_line set commission_state = %s where id = %s', (commission_state, line.id))
        return True

    def _get_order(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        # Worksheet Lines
        for line in self.browse(cr, uid, ids, context):
            order = line.invoice_id.sale_order_ids and line.invoice_id.sale_order_ids[0] or False
            # This line will be unlocked when, SO's Final Amount = all paid invoice amount
            unlocked = False
            if order:
                inv_amt = 0.0
                for invoice in order.invoice_ids:
                    inv_amt += invoice.state == 'paid' and invoice.amount_total or 0.0
                if order.amount_final <= inv_amt:
                    unlocked = True
            # --
            res[line.id] = {
                'order_id': order and order.id or False,
                'amount_init': order and (order.amount_total - order.amount_tax) or False,
                'amount_final': order and order.amount_final or False,
                'unlocked': unlocked,
            }
            # Final check status again.
            self._update_commission_state(cr, uid, line, unlocked, context=context)
        return res

    def _get_unlock(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        # Worksheet Lines
        for line in self.browse(cr, uid, ids, context):
            order = line.invoice_id.sale_order_ids and line.invoice_id.sale_order_ids[0] or False
            res[line.id] = {
                'order_id': order and order.id or False,
                'amount_init': order and (order.amount_total - order.amount_tax) or False,
                'amount_final': order and order.amount_final or False,
            }
        return res

    def _line_from_order(self, cr, uid, ids, context=None):
        wks_line_obj = self.pool.get('commission.worksheet.line')
        for order in self.browse(cr, uid, ids, context=context):
            worksheet_ids = wks_line_obj.search(cr, uid, [('order_id', '=', order.id)], context=context)
        return worksheet_ids

    _columns = {
        'order_id': fields.function(_get_order, type='many2one', relation='sale.order', string='Sales Order', multi='get_order',
            store={
                'commission.worksheet.line': (lambda self, cr, uid, ids, c={}: ids, None, 5)
            }),
        'amount_init': fields.function(_get_order, type='float', string='Order Amount', multi='get_order',
            store={
                'commission.worksheet.line': (lambda self, cr, uid, ids, c={}: ids, None, 5)
            }),
        'amount_final': fields.function(_get_order, type='float', string='Final Amount', multi='get_order',
            store={
                'sale.order': (_line_from_order, ['amount_final'], 10),  # Possible to be updated from sale.order
                'commission.worksheet.line': (lambda self, cr, uid, ids, c={}: ids, None, 5)
            }),
        'unlocked': fields.function(_get_order, type='boolean', string='Unlocked', multi='get_order',
            store={
                'sale.order': (_line_from_order, ['amount_final'], 10),  # Possible to be updated from sale.order
                'commission.worksheet.line': (lambda self, cr, uid, ids, c={}: ids, None, 5)
            }),
        'amount_net': fields.float('Untaxed', readonly=True),
    }

commission_worksheet_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
