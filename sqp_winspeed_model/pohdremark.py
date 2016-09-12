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


class ws_pohdremark(osv.osv):

    _name = "ws.pohdremark"
    _auto = False

    _columns = {
        'brchcode': fields.char('brchcode'),
        'brchid': fields.char('brchid'),
        'docuno': fields.char('docuno'),
        'vendorcode': fields.char('vendorcode'),
        'poid': fields.char('poid'),
        'listno': fields.char('listno'),
        'remark': fields.char('remark'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_pohdremark as (
select po.id, '00000' as BrchCode,
    null as BrchID,
    replace(po.name, '"', '''') as DocuNo,
    rp.search_key as VendorCode,
    null as POID,
    1 as ListNo,
    left(po.notes, 255) as Remark
from purchase_order po
left outer join res_partner rp on rp.id = po.partner_id
where po.state in ('confirmed', 'approved', 'done')
and po.date_order >= '2016-01-01'
order by po.id desc
        )""")

ws_pohdremark()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
