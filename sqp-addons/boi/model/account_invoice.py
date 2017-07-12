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


class account_invoice(osv.osv):

    _inherit = 'account.invoice'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict", domain="[('start_date','!=',False),('active','!=',False)]"),
        'boi_picking_ids': fields.many2many('stock.picking.out', 'account_stock_rel', 'invoice_id', 'picking_id', string="BOI's Picking"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def action_number(self, cr, uid, ids, *args, **kargs):
        result = super(account_invoice, self).action_number(cr, uid, ids, *args, **kargs)
        for invoice in self.browse(cr, uid, ids):
            # Update name for BOI
            if invoice.boi_type == 'BOI':
                boi_cert_name = invoice.boi_cert_id and invoice.boi_cert_id.name or 'BOI'
                number = '%s-%s'%(boi_cert_name,invoice.number[invoice.number.find('-') + 1:])
                self.write(cr, uid, [invoice.id], {'number': number})
        return result

    def refund(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None, context=None):
        invoice_ids = super(account_invoice, self).refund(cr, uid, ids, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        self.update_boi(cr, uid, ids, context.get('active_ids', False), invoice_ids, context=context)
        return invoice_ids

    def debitnote(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None, context=None):
        invoice_ids = super(account_invoice, self).debitnote(cr, uid, ids, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        self.update_boi(cr, uid, ids, context.get('active_ids', False), invoice_ids, context=context)
        return invoice_ids

    def update_boi(self, cr, uid, ids, active_ids, invoice_ids, context=None):
        if context is None:
            context = {}
        if active_ids and len(invoice_ids) > 0:
            for invoice in self.browse(cr, uid, active_ids, context=context):
                boi_type = invoice.boi_type
                boi_cert_id = invoice.boi_cert_id and invoice.boi_cert_id.id or False
                self.write(cr, uid, invoice_ids, {'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_cert_id': False}}

account_invoice()
