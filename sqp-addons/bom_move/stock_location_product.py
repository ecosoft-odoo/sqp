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

class stock_location_product(osv.osv_memory):

    _inherit = "stock.location.product"

    def action_open_window(self, cr, uid, ids, context=None):
        res = super(stock_location_product, self).action_open_window(cr, uid, ids, context=context)
        ctx = res.get('context', {})
        ctx.update({'model_bg': context.get('active_model', False)})
        res.update({'context': ctx})
        return res

stock_location_product()
