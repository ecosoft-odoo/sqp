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

from openerp.osv import osv, fields

class sale_order_line_make_invoice(osv.osv_memory):

    _inherit = "sale.order.line.make.invoice"

    def make_invoices(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(sale_order_line_make_invoice, self).make_invoices(cr, uid, ids, context=context)
        order_obj = self.pool.get('sale.order')
        invoice_obj = self.pool.get('account.invoice')
        if context.get('active_id', False):
            order = order_obj.browse(cr, uid, context.get('active_id'), context=context)
            if order.product_tag_id.name == 'BOI':
                boi_type = 'BOI'
            else:
                boi_type = 'NONBOI'
            invoice_obj.write(cr, uid, res.get('res_id'), {'boi_type': boi_type, 'boi_number_id': order.boi_number_id.id}, context=context)
        return res
