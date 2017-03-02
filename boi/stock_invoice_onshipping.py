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

class stock_invoice_onshipping(osv.osv_memory):

    _inherit = 'stock.invoice.onshipping'

    def create_invoice(self, cr, uid, ids, context=None):
        res = super(stock_invoice_onshipping, self).create_invoice(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        invoice_obj = self.pool.get('account.invoice')
        for picking in picking_obj.browse(cr, uid, context.get('active_ids'), context=context):
            if res.get(picking.id, False):
                boi_number_id = picking.boi_number_id and picking.boi_number_id.id or False
                invoice_obj.write(cr, uid, res.get(picking.id), {'boi_type': picking.boi_type, 'boi_number_id': boi_number_id}, context=context)
        return res
