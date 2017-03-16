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


class ws_sohd(osv.osv):

    _name = "ws.sohd"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'brchcode': fields.char('brchcode'),
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'custcode': fields.char('custcode'),
        'custname': fields.char('custname'),
        'contactname': fields.char('contactname'),
        'validdays': fields.char('validdays'),
        'expiredate': fields.char('expiredate'),
        'shipdate': fields.char('shipdate'),
        'creditdays': fields.char('creditdays'),
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
        'commission': fields.char('commission'),
        'commissionamnt': fields.char('commissionamnt'),
        'saleareacode': fields.char('saleareacode'),
        'deptcode': fields.char('deptcode'),
        'jobcode': fields.char('jobcode'),
        'multicurrency': fields.char('multicurrency'),
        'exchdate': fields.char('exchdate'),
        'currcode': fields.char('currcode'),
        'currtypecode': fields.char('currtypecode'),
        'exchrate': fields.char('exchrate'),
        'docutype': fields.char('docutype'),
        'vatgroupcode': fields.char('vatgroupcode'),
        'soid': fields.char('soid'),
        'currid': fields.char('currid'),
        'currtypeid': fields.char('currtypeid'),
        'organname': fields.char('organname'),
        'saleareaid': fields.char('saleareaid'),
        'vatgroupid': fields.char('vatgroupid'),
        'empid': fields.char('empid'),
        'creditid': fields.char('creditid'),
        'brchid': fields.char('brchid'),
        'transpareaid': fields.char('transpareaid'),
        'transpid': fields.char('transpid'),
        'custid': fields.char('custid'),
        'deptid': fields.char('deptid'),
        'onhold': fields.char('onhold'),
        'shiptoaddr1': fields.char('shiptoaddr1'),
        'shiptoaddr2': fields.char('shiptoaddr2'),
        'district': fields.char('district'),
        'amphur': fields.char('amphur'),
        'province': fields.char('province'),
        'postcode': fields.char('postcode'),
        'tel': fields.char('tel'),
        'fax': fields.char('fax'),
        'condition': fields.char('condition'),
        'shipdays': fields.char('shipdays'),
        'credittermtype': fields.char('credittermtype'),
        'fixedrate': fields.char('fixedrate'),
        'printtime': fields.char('printtime'),
        'sumincludeamnt': fields.char('sumincludeamnt'),
        'sumexcludeamnt': fields.char('sumexcludeamnt'),
        'basediscamnt': fields.char('basediscamnt'),
        'totaexcludeamnt': fields.char('totaexcludeamnt'),
        'attach': fields.char('attach'),
        'remark': fields.char('remark'),
        'custpodate': fields.char('custpodate'),
        'statusremark': fields.char('statusremark'),
        'custpono': fields.char('custpono'),
        'vateffc': fields.char('vateffc'),
        'refsoid': fields.char('refsoid'),
        'refno': fields.char('refno'),
        'refdate': fields.char('refdate'),
        'clearso': fields.char('clearso'),
        'fob': fields.char('fob'),
        'discvateffc': fields.char('discvateffc'),
        'endcreditdate': fields.char('endcreditdate'),
        'miscchargformula': fields.char('miscchargformula'),
        'miscchargamnt': fields.char('miscchargamnt'),
        'miscchargremark': fields.char('miscchargremark'),
        'exchtype': fields.char('exchtype'),
        'fromflag': fields.char('fromflag'),
        'resvstr1': fields.char('resvstr1'),
        'resvstr2': fields.char('resvstr2'),
        'resvstr3': fields.char('resvstr3'),
        'resvstr4': fields.char('resvstr4'),
        'resvstr5': fields.char('resvstr5'),
        'resvstr6': fields.char('resvstr6'),
        'resvstr7': fields.char('resvstr7'),
        'resvamnt1': fields.char('resvamnt1'),
        'resvamnt2': fields.char('resvamnt2'),
        'resvamnt3': fields.char('resvamnt3'),
        'resvamnt4': fields.char('resvamnt4'),
        'resvdate1': fields.char('resvdate1'),
        'docustatus': fields.char('docustatus'),
        'sotitle': fields.char('sotitle'),
        'shiptocode': fields.char('shiptocode'),
        'quotstatus': fields.char('quotstatus'),
        'introduceid': fields.char('introduceid'),
        'appvflag': fields.char('appvflag'),
        'contactnameship': fields.char('contactnameship'),
        'pkgstatus': fields.char('pkgstatus'),
        'jobid': fields.char('jobid'),
        'refeflag': fields.char('refeflag'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_sohd as (
            select so.id, so.date_order as date,
                '00000' as brchcode,
                so.name as DocuNo,
                to_char(so.date_order, 'dd/mm/yyyy') as DocuDate,
                rp.search_key as custcode,
                rp.name as CustName,
                null as ContactName,
                sol.delay as ValidDays,
                null as ExpireDate,
                to_char(so.date_order, 'dd/mm/yyyy') as ShipDate, -- Use same as docudate
                aptl.days as CreditDays,
                null as transpcode,
                ru.search_key as empcode,
                so.amount_untaxed as SumGoodAmnt,
                so.add_disc_amt as BillDiscFormula,  -- What is this?
                so.add_disc_amt as BillDiscAmnt,
                so.amount_net as BillAftrDiscAmnt,
                so.amount_net as TotaBaseAmnt,
                case when so.amount_tax > 0 then 1 else 3 end  as VATType,  -- Has tax = 1, no tax = 3
                case when
                (case when coalesce(nullif(so.amount_net, 0.0), 0.0) = 0 then 0
                else round((so.amount_total - so.amount_net)
                / so.amount_net * 100, 0) end) = 0 then -0.01
                else (case when coalesce(nullif(so.amount_net, 0.0), 0.0) = 0 then 0
                else round((so.amount_total - so.amount_net)
                / so.amount_net * 100, 0) end) end as VATRate,
                case when (so.amount_total - so.amount_net) = 0 then -0.01 else (so.amount_total - so.amount_net) end as VatAmnt,
                so.amount_total as Netamnt,
                -- case when pt.type = 'service' then 2 else 1 end as GoodType, -- In order_line, can mixed.
                1 as GoodType, -- In order_line, can mixed.
                null as Commission,
                null as CommissionAmnt,
                null as saleareacode,
                null as deptcode,
                null as jobcode,
                case when rc.name = 'THB' then 'N' else 'Y' end as MultiCurrency,
                case when rc.name != 'THB' then to_char(so.date_order, 'dd/mm/yyyy') else null end as ExchDate,
                case when rc.name != 'THB' then rc.name else null end as Currcode,
                case when rc.name != 'THB' then rc.name else null end as CurrTypecode,
                round(cr.rate, 4) as Exchrate,
                '104' as DocuType,
                case when coalesce(nullif(so.amount_net, 0.0), 0.0) = 0 then ''
                    else (
                    case when round((so.amount_total - so.amount_net)
                    / so.amount_net * 100, 2) = 7
                    then 'SO-EX7' else 'NO' end) end as VatGroupCode,
                null as SOID,
                null as CurrID,
                null as CurrTypeID,
                null as EmpID,
                null as CreditID,
                null as BrchID,
                null as TranspAreaID,
                null as TranspID,
                null as CustID,
                null as DeptID,
                null as OrganName,
                null as SaleAreaID,
                null as VATGroupID,
                null as OnHold,
                null as ShipToAddr1,
                null as ShipToAddr2,
                null as District,
                null as Amphur,
                null as Province,
                null as PostCode,
                null as Tel,
                null as Fax,
                null as Condition,
                null as ShipDays,
                null as CreditTermType,
                null as FixedRate,
                null as PrintTime,
                null as SumIncludeAmnt,
                null as SumExcludeAmnt,
                null as BaseDiscAmnt,
                null as TotaExcludeAmnt,
                null as Attach,
                null as Remark,
                null as CustPODate,
                null as StatusRemark,
                null as CustPONo,
                null as VATEffc,
                null as RefSOID,
                null as RefNo,
                null as RefDate,
                null as ClearSO,
                null as FOB,
                null as DiscVATEffc,
                null as EndCreditDate,
                null as MiscChargFormula,
                0.0 as MiscChargAmnt,
                null as MiscChargRemark,
                null as ExchType,
                null as FromFlag,
                null as ResvStr1,
                null as ResvStr2,
                null as ResvStr3,
                null as ResvStr4,
                null as ResvStr5,
                null as ResvStr6,
                null as ResvStr7,
                null as ResvAmnt1,
                null as ResvAmnt2,
                null as ResvAmnt3,
                null as ResvAmnt4,
                null as ResvDate1,
                null as DocuStatus,
                null as SOTitle,
                null as ShipToCode,
                null as QuotStatus,
                null as IntroduceID,
                null as AppvFlag,
                null as ContactnameShip,
                null as PkgStatus,
                null as JobID,
                null as Refeflag

            from sale_order so
            join sale_order_line sol on sol.id =
            (
                select max(id) from sale_order_line
                where order_id = so.id
            )
            left outer join product_product pp on pp.id = sol.product_id
                join product_template pt on pt.id = pp.product_tmpl_id
            left outer join res_partner rp on rp.id = so.partner_id
            left outer join account_payment_term apt on apt.id = so.payment_term
            left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
            left outer join res_users ru on ru.id = so.user_id
            left outer join product_pricelist ppl on ppl.id = so.pricelist_id
            left outer join res_currency rc on rc.id = ppl.currency_id
            JOIN res_currency_rate cr ON (cr.currency_id = ppl.currency_id)
                AND
                cr.id IN (SELECT id
                  FROM res_currency_rate cr2
                  WHERE (cr2.currency_id = ppl.currency_id)
                      AND ((so.date_order IS NOT NULL AND cr2.name <= so.date_order)
                    OR (so.date_order IS NULL AND cr2.name <= NOW()))
                  ORDER BY name DESC LIMIT 1)
            where so.state in ('progress', 'manual', 'done')
            order by so.id desc
        )""")

ws_sohd()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
