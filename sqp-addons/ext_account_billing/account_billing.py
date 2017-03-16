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

class account_billing(osv.osv):
    
    _inherit = 'account.billing'
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, date, context=None):
        if context is None:
            context = {}
        # Additional Condition for Matching Billing Date
        #context.update({'billing_date_condition': ['|',('date_maturity', '=', False),('date_maturity', '<=', date)]})
        if not journal_id:
            return {}
        res = self.recompute_billing_lines(cr, uid, ids, partner_id, journal_id, amount, currency_id, date, context=context)
        vals = self.recompute_payment_rate(cr, uid, ids, res, currency_id, date, journal_id, amount, context=context)
        for key in vals.keys():
            res[key].update(vals[key])

        return res

account_billing()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
