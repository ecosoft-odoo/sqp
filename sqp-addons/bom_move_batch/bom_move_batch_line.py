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

from osv import osv, fields

class bom_move_batch_line(osv.osv):
    _name = 'bom.move.batch.line'
    _columns = {
        'name': fields.char('Desciption', size=64, required=True),
        'bom_move_batch_id': fields.many2one('bom.move.batch', 'Batch', ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'product_qty': fields.float('Qunatity', required=True),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'order_qty': fields.float('Order Quantity', required=True),
    }

bom_move_batch_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: