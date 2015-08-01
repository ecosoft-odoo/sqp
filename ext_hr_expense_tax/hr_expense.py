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
from openerp import netsvc
import openerp.addons.decimal_precision as dp

   
def _sqp_employee_get(obj, cr, uid, context=None):
    if context is None:
        context = {}
    ids = obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
    if ids:
        return ids[0]
    return False

class hr_expense_expense(osv.osv):
 
    _inherit = 'hr.expense.expense'
    
    _columns = {
        'employee_id': fields.many2one('hr.employee', "Employee Account", required=True, readonly=True),
        'sqp_employee_id': fields.many2one('hr.employee', "Employee (SQP)", required=True, readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
    }
    
    _defaults = {
        'sqp_employee_id': _sqp_employee_get,
    }
    
hr_expense_expense()


class hr_expense_line(osv.osv):

    _inherit = 'hr.expense.line'
    _columns = {
        'cost_order_id': fields.many2one('sale.order', 'Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", help="For Invoice without Purchase Order reference, user can directly assign the cost to Sales Order here."),
    }

hr_expense_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
