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

    def create_invoices(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(sale_advance_payment_inv, self).create_invoices(cr, uid, ids, context=context)
        if context.get('active_id', False) and res.get('res_id', False):
            order_obj = self.pool.get('sale.order')
            invoice_obj = self.pool.get('account.invoice')
            order = order_obj.browse(cr, uid, context.get('active_id', False), context=context)
            boi_type = (order.id and order.product_tag_id and order.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            boi_cert_id = (order.id and order.boi_cert_id) and order.boi_cert_id.id or False
            invoice_obj.write(cr, uid, res.get('res_id'), {'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)
        return res
