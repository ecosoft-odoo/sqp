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


class ws_transferout(osv.osv):

    _name = "ws.transferout"
    _auto = False

    _columns = {
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'remark': fields.char('remark'),
        'appvempcode': fields.char('appvempcode'),
        'appvempname': fields.char('appvempname'),
        'receempcode': fields.char('receempcode'),
        'receempname': fields.char('receempname'),
        'goodcode': fields.char('goodcode'),
        'goodname': fields.char('goodname'),
        'goodqty': fields.char('goodqty'),
        'goodunit': fields.char('goodunit'),
        'goodprice': fields.char('goodprice'),
        'outtr_branch': fields.char('outtr_branch'),
        'outtr_inventory': fields.char('outtr_inventory'),
        'outtr_location': fields.char('outtr_location'),
        'intr_branch': fields.char('intr_branch'),
        'intr_inventory': fields.char('intr_inventory'),
        'intr_location': fields.char('intr_location'),
        'jobcodedt': fields.char('jobcodedt'),
        'jobnamedt': fields.char('jobnamedt'),
        'goodunitrate': fields.char('goodunitrate'),
        'lot_no': fields.char('lot_no'),
        'description': fields.char('description'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_transferout as (
select sm.id, sp.name as docuno,
    to_char(sp.date + interval '543 years', 'dd/mm/yyyy') as docudate,
    sp.note as remark,
    ru.search_key as appvempcode,
    ru.login as appvempname,
    ru.search_key as receempcode,
    ru.login as receempname,
    pp.search_key as goodcode,
    replace(pp.name_template, '"', '''') as goodname,
    sm.product_qty as goodqty,
    pu.name as goodunit,
    round(pt.standard_price, 4) as goodprice,
    null as outtr_branch,
    src.name as outtr_inventory,
    src.name as outtr_location,
    null as intr_branch,
    dst.name as intr_inventory,
    dst.name as intr_location,
    null as jobcodedt,
    null as jobnamedt,
    round(1/pu.factor) as goodunitrate,
    null as lot_no,
    null as description

from stock_picking sp
join stock_move sm on sm.picking_id = sp.id
left outer join stock_location src on src.id = sm.location_id
left outer join stock_location dst on dst.id = sm.location_dest_id
left outer join res_users ru on ru.id = sp.write_uid
left outer join product_product pp on pp.id = sm.product_id
left outer join product_template pt on pt.id = pp.product_tmpl_id
left outer join product_uom pu on pu.id = sm.product_uom
where sp.type = 'internal'
and sm.state = 'done'
and not (src.name = 'FC_RM' and dst.name = 'Production')
and not (src.name = 'Production' and dst.name = 'FC_RM')
and not (src.name = 'Production' and dst.name = 'FC_FG')
and not (src.name = 'FC_FG' and dst.name = 'Production')
and not (src.name = dst.name)
and src.name not in ('Suppliers', 'Customers', 'Output', 'Procurements', 'Scrapped')
and dst.name not in ('Suppliers', 'Customers', 'Output', 'Procurements', 'Scrapped')
and sp.date >= '2016-09-01'
order by sp.id
        )""")

ws_transferout()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
