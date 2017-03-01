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

class stock_partial_picking(osv.osv_memory):

    _inherit = 'stock.partial.picking'

    def do_partial(self, cr, uid, ids, context=None):
        res = super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        if res.get('context', False):
            for picking in picking_obj.browse(cr, uid, res['context']['active_ids']):
                if picking.boi_type:
                    name = picking.boi_type + '-' + picking.name
                    picking_obj.write(cr, uid, res['context']['active_ids'], {'name': name})
        return res
