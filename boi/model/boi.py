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


class boi_certificate(osv.osv):

    _name = 'boi.certificate'
    _rec_name = 'boi_serial_number'

    _columns = {
        'approve_date': fields.date('Approve Date', required=True),
        'start_date': fields.date('Start Date'),
        'expire_date': fields.date('Expire Date'),
        'boi_name': fields.char('BOI Name', required=True),
        'boi_serial_number': fields.char('BOI Serial No', required=True),
        'boi_cert_type': fields.char('BOI Cert. Type', required=True),
        'promotion_qty': fields.float('Promotion QTY', required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True),
    }

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        certificate_ids = self.search(cr, user, [('start_date','!=',False)] + args, limit=limit, context=context)
        return self.name_get(cr, user, certificate_ids, context=context)

boi_certificate()


class product_product_boi_certificate(osv.osv):

    _name = 'product.product.boi.certificate'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', ondelete='cascade'),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Serial No', required=True),
        'boi_name': fields.related('boi_cert_id', 'boi_name', string='BOI Name', type='char', readonly=True),
    }

product_product_boi_certificate()
