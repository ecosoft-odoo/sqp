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
        'start_date': fields.date('Start Date', required=True),
        'expire_date': fields.date('Expire Date', required=True),
        'boi_name': fields.char('BOI Name', required=True),
        'boi_serial_number': fields.char('BOI Serial No', required=True),
        'boi_cert_type': fields.char('BOI Cert. Type', required=True),
        'promotion_qty': fields.float('Promotion QTY', required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True),
    }

boi_certificate()


class boi_certificate_line(osv.osv):

    _name = 'boi.certificate.line'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'boi_serial_number': fields.many2one('boi.certificate', 'BOI Serial No', required=True),
        'boi_name': fields.char('BOI Name'),
    }

    def onchange_boi_serial_number(self, cr, uid, ids, boi_serial_number, context=None):
        boi_obj = self.pool.get('boi.certificate')
        if boi_serial_number:
            boi = boi_obj.browse(cr, uid, boi_serial_number, context=context)
        return {'value': {'boi_name': boi.boi_name}}

boi_certificate_line()
