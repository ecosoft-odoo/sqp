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
    
    def _get_ref_sale_order(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'ref_order_id': invoice.purchase_order_ids and invoice.purchase_order_ids[0] and invoice.purchase_order_ids[0].ref_order_id.id or False,
                'ref_project_name': invoice.purchase_order_ids and invoice.purchase_order_ids[0] and invoice.purchase_order_ids[0].ref_project_name or False
            }
        return res    
        
    _columns = {
        'ref_order_id': fields.function(_get_ref_sale_order, type='many2one', relation='sale.order', string='Ref Sales Order', multi='po'),
        'ref_project_name': fields.function(_get_ref_sale_order, type='char', string='Ref Project Name', multi='po'),
        'ref_purchase_id': fields.many2one('purchase.order', 'Ref Purchase Order', domain="[('state','not in',('draft','sent','confirmed'))]", readonly=False),
        'cost_order_id': fields.many2one('sale.order', 'Cost-> Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", help="For Invoice without Purchase Order reference, user can directly assign the cost to Sales Order here."),
    }

account_invoice
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
