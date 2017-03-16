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
from tools.translate import _
import time

class account_voucher_line(osv.osv):
    
    def _supplier_invoice_number(self, cursor, user, ids, name, arg, context=None):
        res = dict.fromkeys(ids, False)
        cursor.execute("""SELECT vl.id, i.supplier_invoice_number
                            FROM account_voucher_line vl
                            inner join account_move_line ml on vl.move_line_id = ml.id
                            left outer join account_invoice i on ml.move_id = i.move_id
                            WHERE vl.id IN %s""",(tuple(ids),))
        for line_id, supplier_invoice_number in cursor.fetchall():
            res[line_id] = supplier_invoice_number
        return res
    
    _inherit = 'account.voucher.line'
    
    _columns = {
        'supplier_invoice_number': fields.function(_supplier_invoice_number, string='Supplier Invoice Number', type='char'),
    }

account_voucher_line()


class account_voucher(osv.osv):
    
    _inherit = 'account.voucher'
    
    _columns = {
        'type':fields.selection([
                             ('sale','Sale'),
                             ('purchase','Purchase'),
                             ('payment','Payment'),
                             ('receipt','Receipt'),
                             ('transfer','Transfer'),
                             ],'Default Type', readonly=True, change_default=True, states={'draft':[('readonly',False)]}),               
        'date_doc':fields.date('Cheque Date', readonly=True, select=True, states={'draft':[('readonly',False)]}, help="Document Date"),
        'number_cheque':fields.char('Cheque No.', size=64),
        'reference': fields.char('Ref #', size=64, readonly=False, help="Transaction reference number."),
        'journal_id':fields.many2one('account.journal', 'Journal', readonly=False, required=True),
    }
    _defaults = {
        'date_doc': lambda *a: time.strftime('%Y-%m-%d'),
    }

account_voucher()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
