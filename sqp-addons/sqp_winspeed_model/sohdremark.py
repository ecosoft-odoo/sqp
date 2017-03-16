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


class ws_sohdremark(osv.osv):

    _name = "ws.sohdremark"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'brchcode': fields.char('brchcode'),
        'brchid': fields.char('brchid'),
        'docuno': fields.char('docuno'),
        'custcode': fields.char('custcode'),
        'soid': fields.char('soid'),
        'listno': fields.char('listno'),
        'remark': fields.char('remark'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_sohdremark as (
select so.id, so.date_order as date,
    '00000' as BrchCode,
    null as BrchID,
    replace(so.name, '"', '''') as DocuNo,
    rp.search_key as CustCode,
    null as SOID,
    1 as ListNo,
    left(regexp_replace(so.note, E'[\\n\\r\\u2028]+', ' ', 'g' ), 245) as Remark
from sale_order so
left outer join res_partner rp on rp.id = so.partner_id
where so.state in ('progress', 'manual', 'done')
order by so.id desc
        )""")

ws_sohdremark()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
