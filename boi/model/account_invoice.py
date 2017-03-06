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
        'boi_number_id': fields.many2one('boi.certificate', 'BOI Number'),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def action_number(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(account_invoice, self).action_number(cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, invoice.id, {'number': '%s-%s'%(invoice.boi_type,invoice.number)}, context=context)
        return res

    def refund(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None, context=None):
        if context is None:
            context = {}
        res = super(account_invoice, self).refund(cr, uid, ids, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        invoice_obj = self.pool.get('account.invoice')
        if context.get('active_ids', False):
            for invoice in invoice_obj.browse(cr, uid, context.get('active_ids')):
                boi_number_id = invoice.boi_number_id and invoice.boi_number_id.id or False
                invoice_obj.write(cr, uid, res, {'boi_type': invoice.boi_type, 'boi_number_id': boi_number_id}, context=context)
        return res

    def debitnote(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None, context=None):
        if context is None:
            context = {}
        res = super(account_invoice, self).debitnote(cr, uid, ids, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        if res and context.get('active_id', False):
            invoice = self.browse(cr, uid, context.get('active_id'), context=context)
            boi_number_id = invoice.boi_number_id and invoice.boi_number_id.id or False
            self.write(cr, uid, res, {'boi_type': invoice.boi_type, 'boi_number_id': boi_number_id}, context=context)
        return res

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_number_id': False}}

account_invoice()
