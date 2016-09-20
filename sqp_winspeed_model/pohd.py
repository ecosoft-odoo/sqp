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


class ws_pohd(osv.osv):

    _name = "ws.pohd"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'brchcode': fields.char('brchcode'),
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'vendorcode': fields.char('vendorcode'),
        'appvdocuno': fields.char('appvdocuno'),
        'appvdate': fields.char('appvdate'),
        'appvflag': fields.char('appvflag'),
        'reqintime': fields.char('reqintime'),
        'reqindate': fields.char('reqindate'),
        'shipdate': fields.char('shipdate'),
        'crdtdays': fields.char('crdtdays'),
        'transpcode': fields.char('transpcode'),
        'empcode': fields.char('empcode'),
        'sumgoodamnt': fields.char('sumgoodamnt'),
        'billdiscformula': fields.char('billdiscformula'),
        'billdiscamnt': fields.char('billdiscamnt'),
        'billaftrdiscamnt': fields.char('billaftrdiscamnt'),
        'totabaseamnt': fields.char('totabaseamnt'),
        'vattype': fields.char('vattype'),
        'vatrate': fields.char('vatrate'),
        'vatamnt': fields.char('vatamnt'),
        'netamnt': fields.char('netamnt'),
        'goodtype': fields.char('goodtype'),
        'fob': fields.char('fob'),
        'deptcode': fields.char('deptcode'),
        'jobcode': fields.char('jobcode'),
        'multicurrency': fields.char('multicurrency'),
        'exchdate': fields.char('exchdate'),
        'currcode': fields.char('currcode'),
        'currtypecode': fields.char('currtypecode'),
        'exchrate': fields.char('exchrate'),
        'docutype': fields.char('docutype'),
        'vatgroupcode': fields.char('vatgroupcode'),
        'vendorid': fields.char('vendorid'),
        'billtoid': fields.char('billtoid'),
        'vatgroupid': fields.char('vatgroupid'),
        'creditid': fields.char('creditid'),
        'brchid': fields.char('brchid'),
        'transpid': fields.char('transpid'),
        'deptid': fields.char('deptid'),
        'reqbyname': fields.char('reqbyname'),
        'reqbyid': fields.char('reqbyid'),
        'currid': fields.char('currid'),
        'currtypeid': fields.char('currtypeid'),
        'shipdays': fields.char('shipdays'),
        'contact': fields.char('contact'),
        'receplace1': fields.char('receplace1'),
        'receplace2': fields.char('receplace2'),
        'district': fields.char('district'),
        'fixedrate': fields.char('fixedrate'),
        'amphur': fields.char('amphur'),
        'provice': fields.char('provice'),
        'postcode': fields.char('postcode'),
        'printtimes': fields.char('printtimes'),
        'tel': fields.char('tel'),
        'fax': fields.char('fax'),
        'sumincludeamnt': fields.char('sumincludeamnt'),
        'sumexcludeamnt': fields.char('sumexcludeamnt'),
        'basediscamnt': fields.char('basediscamnt'),
        'totaexcludeamnt': fields.char('totaexcludeamnt'),
        'remark': fields.char('remark'),
        'billdisctype': fields.char('billdisctype'),
        'docustatus': fields.char('docustatus'),
        'onhold': fields.char('onhold'),
        'refname': fields.char('refname'),
        'billmisccharg': fields.char('billmisccharg'),
        'billchargamnt': fields.char('billchargamnt'),
        'billaftrchargamnt': fields.char('billaftrchargamnt'),
        'reqcause': fields.char('reqcause'),
        'discintime': fields.char('discintime'),
        'discexpiredate': fields.char('discexpiredate'),
        'discpayintimeformula': fields.char('discpayintimeformula'),
        'appvbyid': fields.char('appvbyid'),
        'discpayintimeamnt': fields.char('discpayintimeamnt'),
        'refdocuno': fields.char('refdocuno'),
        'refdocudate': fields.char('refdocudate'),
        'povendorno': fields.char('povendorno'),
        'cancelflag': fields.char('cancelflag'),
        'canceldate': fields.char('canceldate'),
        'cancelcause': fields.char('cancelcause'),
        'appvremark': fields.char('appvremark'),
        'contactship': fields.char('contactship'),
        'postdocutype': fields.char('postdocutype'),
        'jobid': fields.char('jobid'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_pohd as (
select po.id, po.date_order as date,
    '00000' as brchcode,
    po.name as DocuNo,
    to_char(po.date_order, 'dd/mm/yyyy') as DocuDate,
    rp.search_key as vendorcode,
    po.name as AppvDocuNo,
    to_char(po.date_order, 'dd/mm/yyyy') as AppvDate,
    null as AppvFlag,
    null as ReqInTime,
    to_char(pr.date_end, 'dd/mm/yyyy') as ReqInDate,
    to_char(pol.date_planned, 'dd/mm/yyyy') as ShipDate,
    null as CrdtDays,  -- property field, can't get
    null as transpcode,
    ru.search_key as empcode,
    po.amount_untaxed as SumGoodAmnt,
    po.add_disc_amt as BillDiscFormula,  -- What is this?
    po.add_disc_amt as BillDiscAmnt,
    po.amount_net as BillAftrDiscAmnt,
    po.amount_net as TotabaseAmnt,
    case when po.amount_tax > 0 then 1 else 3 end  as VATType,  -- Has tax = 1, no tax = 3
    case when coalesce(nullif(po.amount_net, 0.0), 0.0) = 0 then 0
    else round((po.amount_total - po.amount_net)
    / po.amount_net * 100, 2) end as VATRate,
    (po.amount_total - po.amount_net) as VatAmnt,
    po.amount_total as Netamnt,
    case when pt.type = 'service' then 2 else 1 end as GoodType, -- In order_line, can mixed.
    null as FOB,
    null as deptcode,
    null as jobcode,
    case when rc.name = 'THB' then 'N' else 'Y' end as MultiCurrency,
    case when rc.name != 'THB' then to_char(po.date_order, 'dd/mm/yyyy') else null end as ExchDate,
    case when rc.name != 'THB' then rc.name else null end as Currcode,
    case when rc.name != 'THB' then rc.name else null end as CurrTypecode,
    case when rc.name != 'THB' then round(cr.rate, 4)  else null end as Exchrate,
    '305' as DocuType,
    case when coalesce(nullif(po.amount_net, 0.0), 0.0) = 0 then 'NO'
    else (
    case when round((po.amount_total - po.amount_net)
        / po.amount_net * 100, 2) = 7
        then 'PO-EX7' else 'NO' end) end as vatgroupcode,
    null as  VendorID,
    null as  BillToID,
    null as  VATGroupID,
    null as  CreditID,
    null as  BrchID,
    null as  TranspID,
    null as  DeptID,
    null as  ReqByName,
    null as  ReqByID,
    null as  CurrID,
    null as  CurrTypeID,
    0 as  ShipDays,
    null as  Contact,
    null as  RecePlace1,
    null as  RecePlace2,
    null as  District,
    null as  FixedRate,
    null as  Amphur,
    null as  Provice,
    null as  PostCode,
    null as  PrintTimes,
    null as  Tel,
    null as  Fax,
    null as  SumIncludeAmnt,
    po.amount_untaxed as SumExcludeAmnt,
    0.0 as  BaseDiscAmnt,
    null as  TotaExcludeAmnt,
    null as  Remark,
    null as  BillDiscType,
    null as  DocuStatus,
    null as  OnHold,
    null as  RefName,
    null as  BillMiscCharg,
    null as  BillChargAmnt,
    null as  BillAftrChargAmnt,
    null as  ReqCause,
    null as  DiscIntime,
    null as  DiscExpireDate,
    null as  DiscPayIntimeFormula,
    1001 as  AppvByID,
    null as  DiscPayIntimeAmnt,
    null as  RefDocuNo,
    null as  RefDocuDate,
    null as  POVendorNo,
    null as  CancelFlag,
    null as  CancelDate,
    null as  CancelCause,
    null as  AppvRemark,
    null as  ContactShip,
    null as  PostDocutype,
    null as  JobID
from purchase_order po
join purchase_order_line pol on pol.id =
(
    select max(id) from purchase_order_line
    where order_id = po.id
)
left outer join product_product pp on pp.id = pol.product_id
    join product_template pt on pt.id = pp.product_tmpl_id
left outer join purchase_requisition pr on pr.id = po.requisition_id
left outer join res_partner rp on rp.id = po.partner_id
left outer join res_users ru     on ru.id = pr.user_id
left outer join account_payment_term apt on apt.id = po.payment_term_id
left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
left outer join product_pricelist ppl on ppl.id = po.pricelist_id
left outer join res_currency rc on rc.id = ppl.currency_id
JOIN res_currency_rate cr ON (cr.currency_id = ppl.currency_id)
    AND
    cr.id IN (SELECT id
      FROM res_currency_rate cr2
      WHERE (cr2.currency_id = ppl.currency_id)
          AND ((po.date_order IS NOT NULL AND cr2.name <= po.date_order)
        OR (po.date_order IS NULL AND cr2.name <= NOW()))
      ORDER BY name DESC LIMIT 1)

where po.state in ('confirmed', 'approved', 'done')
order by po.id desc
        )""")

ws_pohd()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
