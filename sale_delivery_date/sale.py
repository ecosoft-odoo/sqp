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
import time
import datetime
from datetime import date, timedelta

class sale_order(osv.osv):
    _inherit = "sale.order"
    
    _columns = {
        'date_expected': fields.date('Expected Delivery Date', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    }
    
    _defaults = {
        'date_expected': lambda *a: datetime.datetime.now().strftime('%Y-%m-%d'),
    }
    
sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def _delay_calculation(self, cr, uid, ids, field_name, field_value, context):
        result = {}
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        for line in self.browse(cr, uid, ids, context=context):
            date_planned = datetime.datetime.strptime(line.order_id.date_expected,'%Y-%m-%d')
            delay = date_planned - datetime.datetime.now() 
            #adding company security lead days (correction for date_expected on stock_moves)
            delay += timedelta(days=company.security_lead)
            #convert delay on days (1 day = 86400 seconds)
            result[line.id] = delay.days + (delay.seconds / 86400.0)

        return result

    _columns = {
        'delay': fields.function(_delay_calculation, method=True, type="float", string='Calculated delay'),  
    }

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
