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
from openerp.tools.amount_to_text_en import amount_to_text

class account_invoice(osv.osv):
    
    def _amount_total_text(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cursor, user, ids, context=context):
            a = 'Baht'
            b = 'Satang'
            if invoice.currency_id.name == 'USD':
                a = 'Dollar'
                b = 'Cent'
            if invoice.currency_id.name == 'EUR':
                a = 'Euro'
                b = 'Cent'   
            res[invoice.id] = amount_to_text(invoice.amount_total, 'en', a).replace('Cent', b).replace('Cents', b)
        return res
    
    _inherit = 'account.invoice'
    _columns = {
        'amount_total_text': fields.function(_amount_total_text, string='Amount Total (Text)', type='char'),
    }

account_invoice()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
