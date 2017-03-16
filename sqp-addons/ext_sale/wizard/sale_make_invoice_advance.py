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


class sale_advance_payment_inv(osv.osv_memory):

    _inherit = "sale.advance.payment.inv"

    def _get_advance_payment_method(self, cr, uid, context=None):
        res = []
        if context.get('active_model', False) == 'sale.order':
            sale_id = context.get('active_id', False)
            if sale_id:
                sale = self.pool.get('sale.order').browse(cr, uid, sale_id)
                # Advance option not available when, There are at least 1 non-cancelled invoice created
                num_valid_invoice = 0
                for i in sale.invoice_ids:
                    if i.state not in ['cancel']:
                        num_valid_invoice += 1
                # Remove these 2 options from according to SQP requirement
                if sale.order_policy == 'manual' and (num_valid_invoice or not context.get('advance_type', False)):
                    res.append(('line_percentage', 'Line Percentage'))
                if not num_valid_invoice and context.get('advance_type', False):
                    res.append(('percentage', 'Percentage'))
                    res.append(('fixed', 'Fixed price (deposit)'))

        return res

    _columns = {
        'advance_payment_method': fields.selection(_get_advance_payment_method,
            'What do you want to invoice?', required=True,
            help="""Use All to create the final invoice.
                Use Percentage to invoice a percentage of the total amount.
                Use Fixed Price to invoice a specific amound in advance.
                Use Some Order Lines to invoice a selection of the sales order lines."""),
        }

sale_advance_payment_inv()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
