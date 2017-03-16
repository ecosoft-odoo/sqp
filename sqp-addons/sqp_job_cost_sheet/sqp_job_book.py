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

from openerp import netsvc
from openerp.osv import osv, fields


class sqp_job_book(osv.osv):

    _description = 'Job Booking'
    _name = 'sqp.job.book'
    _columns = {
        'sale_order_id': fields.many2one('sale.order', 'Sales Order', required="True"),
        'labor_line': fields.one2many('sqp.job.book.labor', 'book_id', 'Labor Lines'),
        'transport_line': fields.one2many('sqp.job.book.transport', 'book_id', 'Transport Lines'),
        'electric_line': fields.one2many('sqp.job.book.electric', 'book_id', 'Transport Lines'),
    }
    _sql_constraints = [
        ('order_uniq', 'unique (sale_order_id)', 'This Sales Order has been used!')
    ]

sqp_job_book()


class sqp_job_book_labor(osv.osv):
    _description = 'Job Labor Line'
    _name = 'sqp.job.book.labor'
    _columns = {
        'book_id': fields.many2one('sqp.job.book', 'Sales Order'),
        'order_id': fields.related('book_id', 'sale_order_id', type="many2one", relation="sale.order", string='Sales Order', store=True),
        'name': fields.text('Description'),
        'date': fields.date('Date'),
        'amount': fields.float('Amount'),
    }

sqp_job_book_labor()


class sqp_job_book_transport(osv.osv):

    _description = 'Job Transport Line'
    _name = 'sqp.job.book.transport'
    _columns = {
        'book_id': fields.many2one('sqp.job.book', 'Sales Order'),
        'order_id': fields.related('book_id', 'sale_order_id', type="many2one", relation="sale.order", string='Sales Order', store=True),
        'name': fields.text('Description'),
        'date': fields.date('Date'),
        'amount': fields.float('Amount'),
    }

sqp_job_book_transport()


class sqp_job_book_electric(osv.osv):

    _description = 'Job Electric Line'
    _name = 'sqp.job.book.electric'
    _columns = {
        'book_id': fields.many2one('sqp.job.book', 'Sales Order'),
        'order_id': fields.related('book_id', 'sale_order_id', type="many2one", relation="sale.order", string='Sales Order', store=True),
        'name': fields.text('Description'),
        'date': fields.date('Date'),
        'amount': fields.float('Amount'),
    }

sqp_job_book_electric()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
