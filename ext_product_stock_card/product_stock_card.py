# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Mentis d.o.o. (<http://www.mentis.si/openerp>).
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
from openerp.tools.sql import drop_view_if_exists


class product_stock_card(osv.osv):

    _inherit = "product.stock.card"
    _columns = {
        'ref_order_id': fields.many2one('sale.order', 'Sales Order', readonly=True),
        'ref_project_name': fields.char('Project Name', size=128, readonly=False),
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'product_stock_card')
        cr.execute("""CREATE OR REPLACE VIEW product_stock_card AS
                      (SELECT sm.id AS id,
                              sm.product_id AS product_id,
                              sp.id AS picking_id,
                              sm.date AS date,
                              pa.id AS partner_id,
                              CASE
                                WHEN sp.type = 'in'
                                  THEN pai.id
                                WHEN sp.type = 'out'
                                  THEN sai.id
                                ELSE NULL
                              END AS invoice_id,
                              sm.price_unit AS price_unit,
                              sm.product_qty * sm.price_unit AS amount,
                              case WHEN sp.name is null THEN sm.name ELSE sp.name END as name,
                              sm.location_id as location_id,
                              sm.location_dest_id as location_dest_id,
                              CASE WHEN sp.type = 'internal' and
                                  (select usage from stock_location sl WHERE sl.id = sm.location_id) = (select usage from stock_location sl WHERE sl.id = sm.location_dest_id)
                                  THEN 'move'
                                  WHEN sp.type is null THEN 'adjust'
                                  ELSE sp.type
                              END as type,
                              sm.product_qty as picking_qty,
                              pt.uom_id as default_uom,
                              sm.product_uom as move_uom,
                              sp.ref_order_id as ref_order_id,
                              sp.ref_project_name as ref_project_name
                         FROM stock_move AS sm
                              LEFT OUTER JOIN res_partner AS pa ON pa.id = sm.partner_id
                              LEFT OUTER JOIN stock_picking AS sp ON sp.id = sm.picking_id
                              LEFT OUTER JOIN sale_order_line_invoice_rel AS solir ON solir.order_line_id = sm.sale_line_id
                              LEFT OUTER JOIN purchase_order_line_invoice_rel AS polir ON polir.order_line_id = sm.purchase_line_id
                              LEFT OUTER JOIN account_invoice_line AS sail ON sail.id = solir.invoice_id
                              LEFT OUTER JOIN account_invoice AS sai ON sai.id = sail.invoice_id
                              LEFT OUTER JOIN account_invoice_line AS pail ON pail.id = polir.invoice_id
                              LEFT OUTER JOIN account_invoice AS pai ON pai.id = pail.invoice_id
                              LEFT OUTER JOIN product_product d on (d.id=sm.product_id)
                              LEFT OUTER JOIN product_template pt on (pt.id=d.product_tmpl_id)
                        WHERE sm.state = 'done' and  sm.location_id <> sm.location_dest_id);""")

product_stock_card()
