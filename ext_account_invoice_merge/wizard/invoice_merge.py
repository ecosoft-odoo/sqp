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
from openerp.tools.translate import _

class invoice_merge(osv.osv_memory):

    _inherit = 'invoice.merge'

    def merge_invoices(self, cr, uid, ids, context):

        data = self.browse(cr, uid, ids, context=context)[0]
        for invoice in data.invoices:
            if invoice.type in ('out_invoice', 'out_refund'):
                raise osv.except_osv(_('Error!'), _('You cannot merge the customer invoices.'))
        
        res =  super(invoice_merge, self).merge_invoices(cr, uid, ids, context)
        return res

invoice_merge()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
