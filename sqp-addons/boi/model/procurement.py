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

class procurement_order(osv.osv):

    _inherit = 'procurement.order'

    def make_mo(self, cr, uid, ids, context=None):
        result = super(procurement_order, self).make_mo(cr, uid, ids, context=context)
        procurement_obj = self.pool.get('procurement.order')
        production_obj = self.pool.get('mrp.production')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            if result.get(procurement.id, False):
                production = production_obj.browse(cr, uid, result.get(procurement.id), context=context)
                boi_type = (production.order_id and production.order_id.product_tag_id and production.order_id.product_tag_id.name == 'BOI') \
                                and 'BOI' or 'NONBOI'
                production_obj.write(cr, uid, [result.get(procurement.id)], {'name': '%s-%s'%(boi_type,production.name)})
        return result

procurement_order()