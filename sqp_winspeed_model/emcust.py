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


class ws_emcust(osv.osv):

    _name = "ws.emcust"
    _auto = False

    _columns = {
        'custcode': fields.char('custcode'),
        'custitle': fields.char('custitle'),
        'custname': fields.char('custname'),
        'custnameeng': fields.char('custnameeng'),
        'custtype': fields.char('custtype'),
        'creditdays': fields.char('creditdays'),
        'creditamnt': fields.char('creditamnt'),
        'taxid': fields.char('taxid'),
        'custaddr1': fields.char('custaddr1'),
        'custaddr2': fields.char('custaddr2'),
        'district': fields.char('district'),
        'amphur': fields.char('amphur'),
        'province': fields.char('province'),
        'postcode': fields.char('postcode'),
        'contaddr1': fields.char('contaddr1'),
        'contaddr2': fields.char('contaddr2'),
        'contdistrict': fields.char('contdistrict'),
        'contamphur': fields.char('contamphur'),
        'contprovince': fields.char('contprovince'),
        'contpostcode': fields.char('contpostcode'),
        'conttel': fields.char('conttel'),
        'contfax': fields.char('contfax'),
        'custid': fields.char('custid'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_emcust as (
select  rp.id, rp.search_key as custcode,
    null as custitle,
    rp.name as custname,
    null as custnameeng,
    case when rp.is_company = true then 1 else 2 end as custtype,
    null as creditdays, -- Payment term is property field, can't get easily.
    rp.credit_limit as creditamnt,
    rp.vat as taxid,
    rp.street as custaddr1,
    rp.street2 as custaddr2,
    null as district,
    null as amphur,
    rp.city as province,
    rp.zip as postcode,
    rp.street as contaddr1,
    rp.street2 as contaddr2,
    null as contdistrict,
    null as contamphur,
    rp.city as contprovince,
    rp.zip as contpostcode,
    rp.phone as conttel,
    rp.fax as contfax,
    null as custid
from res_partner rp
where customer = true
        )""")

ws_emcust()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
