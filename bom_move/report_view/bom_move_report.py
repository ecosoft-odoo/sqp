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

from openerp import tools
from openerp.osv import fields, osv

class bom_move_report(osv.osv):
    _name = "bom.move.report"
    _description = "Bom Move Report"
    _auto = False
    _columns = {
        'id': fields.integer('Id', readonly=True),
        'ref_mo_id': fields.many2one('mrp.production', 'Ref MO', readonly=True),
        'ref_order_id': fields.many2one('sale.order', 'Ref Sales Order', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'name': fields.char('Description', readonly=True),
        'product_qty': fields.float('Quantity', readonly=True),
        'order_qty': fields.float('Order QTY', readonly=True),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure', readonly=True),
        'location_id': fields.many2one('stock.location', 'Source Location', readonly=True),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', readonly=True),
        'state': fields.selection([
            ('draft', 'New'),
            ('cancel', 'Cancelled'),
            ('waiting', 'Waiting Another Move'),
            ('confirmed', 'Waiting Availability'),
            ('assigned', 'Available'),
            ('done', 'Done'),
            ], 'Status', readonly=True, select=True, track_visibility='onchange',
        ),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'bom_move_report')
        cr.execute("""
            create or replace view bom_move_report as (
                select
                    sm.id as id,
                    sp.ref_mo_id as ref_mo_id,
                    sp.ref_order_id as ref_order_id,
                    sp.partner_id as partner_id,
                    sm.product_id as product_id,
                    sm.name as name,
                    sm.product_qty as product_qty,
                    sm.order_qty as order_qty,
                    sm.product_uom as product_uom,
                    sm.location_id as location_id,
                    sm.location_dest_id as location_dest_id,
                    sm.state as state
                from
                    stock_picking sp
                      inner join stock_move sm on (sp.id = sm.picking_id)
                where
                    sp.is_bom_move = True and sp.type = 'out'
            )
        """)
bom_move_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
