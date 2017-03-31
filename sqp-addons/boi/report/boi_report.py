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

class boi_report(osv.osv):
    _name = "boi.report"
    _description = "BOI Report"
    _auto = False
    _columns = {
        'id': fields.integer('Id', readonly=True),
        'do_no': fields.char('DO No.', readonly=True),
        'mo_no': fields.char('MO No.', readonly=True),
        'so_no': fields.char('SO No.', readonly=True),
        'inv_no': fields.char('INV No.', readonly=True),
        'cust_ref': fields.char('Customer Reference', readonly=True),
        'part_no': fields.char('Part no./Model', readonly=True),
        'product_name': fields.char('Product Name', readonly=True),
        'qty': fields.float('Quantity (sqm)', readonly=True),
        'date_done': fields.date('Transfer Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'month': fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'boi_report')
        cr.execute("""
            create or replace view boi_report as (
                select
                    row_number() over (order by sp.id) as id,
                    sp.name as do_no,
                    (case when sp.origin like '%MO%' then sp.origin else '' end) as mo_no,
                    so.name as so_no,
                    ai.number as inv_no,
                    ai.name as cust_ref,
                    pp.boi_default_code as part_no,
                    pp.boi_product_name as product_name,
                    (pp."W" * pp."L" / 1000000 * sm.product_qty) - (pp.cut_area) as qty,
                    sp.date_done as date_done,
                    to_char(sp.date_done, 'YYYY') as year,
                    to_char(sp.date_done, 'MM') as month,
                    to_char(sp.date_done, 'YYYY-MM-DD') as day
                from stock_picking sp
                left join sale_order so on sp.ref_order_id = so.id
                left join account_invoice ai on so.name = ai.origin
                left join stock_move sm on sp.id = sm.picking_id
                left join product_product pp on sm.product_id = pp.id
                where sp.type = 'out' and (sp.is_supply_list = False or sp.is_supply_list is null) and (sp.is_bom_move = False or sp.is_bom_move is null) and sp.state = 'done' and sp.boi_type = 'BOI'
            )
        """)

boi_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
