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

import netsvc
from osv import osv, fields

class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    _columns = {
        'note': fields.text('Note'),
        'supplier_invoice_number': fields.char('Supplier Invoice Number', size=64, help="The reference of this invoice as provided by the supplier.", readonly=False),
        'print_text_in_english': fields.boolean('Print Amount Text in English'),
        'date_due': fields.date('Due Date', readonly=False, select=True,
            help="If you use payment terms, the due date will be computed automatically at the generation "\
                "of accounting entries. The payment term may compute several due dates, for example 50% now and 50% in one month, but if you want to force a due date, make sure that the payment term is not set on the invoice. If you keep the payment term and the due date empty, it means direct payment."),
    }

    # go from canceled state to draft state, should also set state from 2binvoiced to invoiced
    def action_cancel_draft(self, cr, uid, ids, *args):
        res = super(account_invoice, self).action_cancel_draft(cr, uid, ids, *args)
        for invoice in self.browse(cr, uid, ids):
            for picking in invoice.picking_ids:
                if picking.invoice_state == '2binvoiced':
                    self.pool.get('stock.picking').write(cr, uid, picking.id, {'invoice_state': 'invoiced'})
        return res
    
account_invoice()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
