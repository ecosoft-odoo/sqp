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


class boi_certificate(osv.osv):

    _name = 'boi.certificate'

    _columns = {
        'name': fields.char('BOI Serial No', required=True),
        'boi_name': fields.char('BOI Name', required=True),
        'approve_date': fields.date('Approve Date', required=True),
        'start_date': fields.date('Start Date'),
        'expire_date': fields.date('Expire Date'),
        'boi_cert_type': fields.char('BOI Cert. Type', required=True),
        'promotion_qty': fields.float('Promotion QTY', required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True, ondelete="restrict"),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
    }

    def create(self, cr, uid, vals, context=None):
        self.func_show_error(cr, uid, vals, context=context)
        return super(boi_certificate, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, ids, default=None, context=None):
        return super(boi_certificate, self).copy(cr, uid, ids, default=default, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        self.func_show_error(cr, uid, vals, context=context)
        return super(boi_certificate, self).write(cr, uid, ids, vals, context=context)

    def func_show_error(self, cr, uid, vals, context=None):
        if vals.get('name', False):
            certificate_ids = self.search(cr, uid, [('name','=',vals.get('name'))], context=context)
            if len(certificate_ids) > 0:
                raise osv.except_osv(_('Error!'), _('Must not duplicate BOI Serial No'))
        return True

boi_certificate()


class product_product_boi_certificate(osv.osv):

    _name = 'product.product.boi.certificate'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', ondelete='cascade'),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Serial No', required=True, ondelete="restrict", domain="[('start_date','!=',False),('active','!=',False)]" ),
        'boi_name': fields.related('boi_cert_id', 'boi_name', string='BOI Name', type='char', readonly=True),
    }

product_product_boi_certificate()
