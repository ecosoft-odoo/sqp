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

import types
import netsvc
from osv import osv, fields
import openerp.addons.decimal_precision as dp

class invoice_expense_expense(osv.osv):

    _inherit = "invoice.expense.expense"
    _columns = {
        'ref_order_id': fields.many2one('sale.order', 'Ref Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", readonly=False),
        'ref_project_name': fields.char('Ref Project Name', size=128, readonly=False),
        'ref_purchase_id': fields.many2one('purchase.order', 'Ref Purchase Order', domain="[('state','not in',('draft','sent','confirmed'))]", readonly=False),
    }
    
    def onchange_ref_order_id(self, cr, uid, ids, ref_order_id, context=None):
        v = {}
        if ref_order_id:
            order = self.pool.get('sale.order').browse(cr, uid, ref_order_id, context=context)
            if order.ref_project_name:
                v['ref_project_name'] = order.ref_project_name
        return {'value': v}
    
invoice_expense_expense()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
