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


class ws_emvendor(osv.osv):

    _name = "ws.emvendor"
    _auto = False

    _columns = {
        'vendorcode': fields.char('vendorcode'),
        'vendoritle': fields.char('vendoritle'),
        'vendorname': fields.char('vendorname'),
        'vendornameeng': fields.char('vendornameeng'),
        'vendortype': fields.char('vendortype'),
        'creditdays': fields.char('creditdays'),
        'creditamnt': fields.char('creditamnt'),
        'taxid': fields.char('taxid'),
        'vendoraddr1': fields.char('vendoraddr1'),
        'vendoraddr2': fields.char('vendoraddr2'),
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
        'vendorid': fields.char('vendorid'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_emvendor as (
select rp.id, rp.search_key as vendorcode,
    null as vendoritle,
    rp.name as vendorname,
    rp.name as vendornameeng,
    case when rp.is_company = true then 1 else 2 end as vendortype,
    null as creditdays, -- Payment term is property field, can't get easily.
    rp.credit_limit as creditamnt,
    rp.vat as taxid,
    rp.street as vendoraddr1,
    rp.street2 as vendoraddr2,
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
    null as conttel,
    null as contfax,
    null as vendorid
from res_partner rp
where supplier = true
        )""")

ws_emvendor()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
