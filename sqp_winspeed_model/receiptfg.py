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


class ws_receiptfg(osv.osv):

    _name = "ws.receiptfg"
    _auto = False

    _columns = {
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'deptcode': fields.char('deptcode'),
        'deptname': fields.char('deptname'),
        'jobcodehd': fields.char('jobcodehd'),
        'jobnamehd': fields.char('jobnamehd'),
        'remark': fields.char('remark'),
        'empcode': fields.char('empcode'),
        'empname': fields.char('empname'),
        'receempcode': fields.char('receempcode'),
        'receempname': fields.char('receempname'),
        'goodcode': fields.char('goodcode'),
        'goodname': fields.char('goodname'),
        'inventory': fields.char('inventory'),
        'location': fields.char('location'),
        'goodunit': fields.char('goodunit'),
        'goodqty': fields.char('goodqty'),
        'goodprice': fields.char('goodprice'),
        'goodamnt': fields.char('goodamnt'),
        'jobcodedt': fields.char('jobcodedt'),
        'jobnamedt': fields.char('jobnamedt'),
        'goodunitrate': fields.char('goodunitrate'),
        'description': fields.char('description'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_receiptfg as (
select sm.id, sm.name as docuno,  -- By MO, no picking
    to_char(sm.date, 'dd/mm/yyyy') as docudate,
    null as deptcode,
    null as deptname,
    null as jobcodehd,
    null as jobnamehd,
    null as remark,
    ru.search_key as empcode,
    ru.login as empname,
    ru.search_key as receempcode,
    ru.login as receempname,
    pp.search_key as goodcode,
    replace(pp.name_template, '"', '''') as goodname,
    'FC_FG' as inventory,
    'FC_FG' as location,
    pu.name as goodunit,
    (case when dst.name = 'FC_FG' then sm.product_qty else -sm.product_qty end) as goodqty,
    round(pt.standard_price, 4) as goodprice,
    round((case when dst.name = 'FC_FG' then sm.product_qty else -sm.product_qty end) * pt.standard_price, 4) as goodamnt,
    null as jobcodedt,
    null as jobnamedt,
    round(1/pu.factor) as goodunitrate,
    null as description

from stock_move sm
left outer join stock_location src on src.id = sm.location_id
left outer join stock_location dst on dst.id = sm.location_dest_id
left outer join res_users ru on ru.id = sm.write_uid
left outer join product_product pp on pp.id = sm.product_id
left outer join product_template pt on pt.id = pp.product_tmpl_id
left outer join product_uom pu on pu.id = sm.product_uom
where sm.state = 'done'
and ((src.name = 'Production' and dst.name = 'FC_FG') or (src.name = 'FC_FG' and dst.name = 'Production'))
and is_one_time_use = false  -- Not include 1 time use product.
and sm.date >= '2016-09-01'
order by sm.date desc
        )""")

ws_receiptfg()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
