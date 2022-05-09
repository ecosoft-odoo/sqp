# -*- coding: utf-8 -*-
#
#    Jamotion GmbH, Your Odoo implementation partner
#    Copyright (C) 2013-2015 Jamotion GmbH.
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
#    Created by Boris on 15.03.16.
#

from openerp.osv import fields, osv


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _reset_sequence(self, cr, uid, ids, context=None):
        orders = self.browse(cr, uid, ids, context=context)
        for rec in orders:
            current_sequence = 1
            for line in rec.order_line:
                line.write(cr, uid, {'sequence': current_sequence}, context=context)
                current_sequence += 1

    # reset line sequence number during create
    def create(self, cr, uid, vals, context=None):
        res = super(sale_order, self).create(cr, uid, vals, context=context)
        self._reset_sequence(cr, uid, res, context=context)
        return res

    # reset line sequence number during write
    def write(self, cr, uid, ids, vals, context=None):
        res = super(sale_order, self).write(cr, uid, ids, vals, context=context)

        self._reset_sequence(cr, uid, ids, context=context)

        return res

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    _columns = {
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of sales order lines."),
    }

    _defaults = {
        'sequence': 99999,
    }
