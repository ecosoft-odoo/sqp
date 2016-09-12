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


class ws_soinvoice(osv.osv):

    _name = "ws.soinvoice"
    _auto = False

    _columns = {
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'invno': fields.char('invno'),
        'invdate': fields.char('invdate'),
        'custcode': fields.char('custcode'),
        'custname': fields.char('custname'),
        'sono': fields.char('sono'),
        'custpono': fields.char('custpono'),
        'creditstartdate': fields.char('creditstartdate'),
        'creditdays': fields.char('creditdays'),
        'creditenddate': fields.char('creditenddate'),
        'duedate': fields.char('duedate'),
        'senddate': fields.char('senddate'),
        'transpcode': fields.char('transpcode'),
        'empcode': fields.char('empcode'),
        'empname': fields.char('empname'),
        'goodcode': fields.char('goodcode'),
        'goodname': fields.char('goodname'),
        'invecode': fields.char('invecode'),
        'locacode': fields.char('locacode'),
        'goodunitcode': fields.char('goodunitcode'),
        'goodqty2': fields.char('goodqty2'),
        'goodprice2': fields.char('goodprice2'),
        'gooddiscamnt': fields.char('gooddiscamnt'),
        'goodamount': fields.char('goodamount'),
        'jobcodedt': fields.char('jobcodedt'),
        'jobnamedt': fields.char('jobnamedt'),
        'goodunitrate': fields.char('goodunitrate'),
        'vattype': fields.char('vattype'),
        'goodcompareunitcode': fields.char('goodcompareunitcode'),
        'goodcompareqty': fields.char('goodcompareqty'),
        'sumgoodamnt': fields.char('sumgoodamnt'),
        'billdiscformula': fields.char('billdiscformula'),
        'billaftrdiscamnt': fields.char('billaftrdiscamnt'),
        'advnamnt': fields.char('advnamnt'),
        'totalbaseamnt': fields.char('totalbaseamnt'),
        'aftradvnaamnt': fields.char('aftradvnaamnt'),
        'vatrate': fields.char('vatrate'),
        'vatamnt': fields.char('vatamnt'),
        'netamnt': fields.char('netamnt'),
        'vatgroupcode': fields.char('vatgroupcode'),
        'departmentcode': fields.char('departmentcode'),
        'departmentname': fields.char('departmentname'),
        'jobcode': fields.char('jobcode'),
        'jobname': fields.char('jobname'),
        'saleareacode': fields.char('saleareacode'),
        'saleareaname': fields.char('saleareaname'),
        'goodtype': fields.char('goodtype'),
        'stockeffc': fields.char('stockeffc'),
        'fob': fields.char('fob'),
        'arcode': fields.char('arcode'),
        'exchdate': fields.char('exchdate'),
        'currcode': fields.char('currcode'),
        'currname': fields.char('currname'),
        'currtypecode': fields.char('currtypecode'),
        'currtypename': fields.char('currtypename'),
        'exchrate': fields.char('exchrate'),
        'no': fields.char('no'),
        'desciption': fields.char('desciption'),
        'advnno': fields.char('advnno'),
        # 'invno': fields.char('invno'),
        'advndate': fields.char('advndate'),
        'advntotaamnt': fields.char('advntotaamnt'),
        'lastremaamnt': fields.char('lastremaamnt'),
        'cutadvnamnt': fields.char('cutadvnamnt'),
        'invoiceno': fields.char('invoiceno'),
        'invoicedate': fields.char('invoicedate'),
        'vatremark': fields.char('vatremark'),
        'taxid': fields.char('taxid'),
        'brchname': fields.char('brchname'),
        'brchnameeng': fields.char('brchnameeng'),
        'basevat': fields.char('basevat'),
        # 'vatrate': fields.char('vatrate'),
        'vatamount': fields.char('vatamount'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_soinvoice as (
select ail.id, ai.number as Docuno,
to_char(ai.date_invoice + interval '543 years', 'dd/mm/yyyy') as DocuDate,
ai.number as InvNo,
to_char(ai.date_invoice + interval '543 years', 'dd/mm/yyyy') as InvDate,
rp.search_key as CustCode,
rp.name as CustName,
so.name as SONo,
null as CustPONo,
null as CreditStartDate,
aptl.days as CreditDays,
null as CreditEndDate,
to_char(ai.date_due + interval '543 years', 'dd/mm/yyyy') as DueDate,
null as SendDate,
null as TranspCode,
ru.search_key as EmpCode,
ru.login as EmpName,
pp.search_key as GoodCode,
replace(pp.name_template, '"', '''') as GoodName,
sw.name as InveCode,
sl.name as LocaCode,
pu.name as GoodUnitCode,
ail.quantity as GoodQty2,
round(ail.price_unit, 4) as GoodPrice2,
round((ail.quantity * ail.price_unit) - ail.price_subtotal, 4) as GoodDiscAmnt,
round(ail.price_subtotal, 4) as GoodAmount,
null as JobCodeDT,
null as JobNameDT,
    case when pu.uom_type = 'bigger' then round(1/factor, 2)
    when pu.uom_type = 'smaller' then round(factor, 2)
    else 1 end as GoodUnitRate,
    case when ai.amount_tax > 0 then 1 else 3 end  as VatType,
null as GoodCompareUnitCode,
null as GoodCompareqty,
so.name RefeNo,
ai.amount_beforetax as Sumgoodamnt,
    ai.add_disc_amt as Billdiscformula,
    ai.amount_net as Billaftrdiscamnt,
    coalesce(nullif(ai.amount_advance, 0.0), ai.amount_deposit) as advnamnt,
    ai.amount_beforetax as Totalbaseamnt,
    ai.amount_beforetax as aftradvnaamnt,
    case when ai.amount_beforetax = 0 then 0 else
        round((ai.amount_total - ai.amount_beforetax)
            / ai.amount_beforetax * 100, 2) end as VatRate,
    ai.amount_tax as VatAmnt,
    ai.amount_total as Netamnt,
    case when (case when ai.amount_beforetax = 0 then 0 else
        round((ai.amount_total - ai.amount_beforetax)
            / ai.amount_beforetax * 100, 2) end) = 7 then 'SO-EX7' else 'NO' end as VatGroupCode,
null as DepartmentCode,
null as DepartmentName,
null as JobCode,
null as JobName,
null as SaleAreaCode,
null as SaleAreaName,
case when pt.type != 'service' then 1 else 2 end as GoodType,
case when pt.type != 'service' then 'Y' else 'N' end as StockEffc,
null as FOB,
rp.search_key as ARCode,
to_char(ai.date_invoice + interval '543 years', 'dd/mm/yyyy') as ExchDate,
case when rc.name = 'THB' then null else rc.name end as Currcode,
case when rc.name = 'THB' then null else rc.name end as CurrName,
case when rc.name = 'THB' then null else rc.name end as CurrTypecode,
case when rc.name = 'THB' then null else rc.name end as CurrTypeName,
round(cr.rate, 4) as Exchrate,
null as No,
null as Desciption,
null as AdvnNo,
-- null as InvNo,
null as AdvnDate,
null as AdvnTotaAmnt,
null as LastRemaAmnt,
coalesce(nullif(ai.amount_advance, 0.0), ai.amount_deposit) as CutAdvnAmnt,
ai.number as InvoiceNo,
to_char(ai.date_invoice + interval '543 years', 'dd/mm/yyyy') as InvoiceDate,
'ขายเชื่อ' || rp.name as VATRemark,
rp.vat as taxid,
rp.branch as Brchname,
rp.branch as Brchnameeng,
ai.amount_beforetax as BaseVat,
-- case when ai.amount_beforetax = 0 then 0 else
--        round((ai.amount_total - ai.amount_beforetax)
--            / ai.amount_beforetax * 100, 2) end as VatRate,
ai.amount_tax as VatAmount

from account_invoice ai
    join account_invoice_line ail on ail.invoice_id = ai.id
    left outer join res_partner rp on rp.id = ai.partner_id
    left outer join product_product pp on pp.id = ail.product_id
    left outer join product_template pt on pt.id = pp.product_tmpl_id
    left outer join (select invoice_id, max(picking_id) picking_id
        from picking_invoice_rel
        group by invoice_id) p on p.invoice_id = ai.id
    left outer join stock_picking sp on sp.id = p.picking_id
    left outer join res_currency rc on rc.id = ai.currency_id
    left outer join account_payment_term apt on apt.id = ai.payment_term
    left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
    left outer join sale_order_invoice_rel sir on sir.invoice_id = ai.id
    left outer join sale_order so on so.id = sir.order_id
    left outer join res_users ru on ru.id = so.user_id
    left outer join product_uom pu on pu.id = ail.uos_id
    left outer join sale_shop ss on ss.id = so.shop_id
    left outer join stock_warehouse sw on sw.id = ss.warehouse_id
    left outer join stock_location sl on sl.id = sw.lot_stock_id

    JOIN res_currency_rate cr ON (cr.currency_id = ai.currency_id)
            AND
            cr.id IN (SELECT id
                  FROM res_currency_rate cr2
                  WHERE (cr2.currency_id = ai.currency_id)
                      AND ((ai.date_invoice IS NOT NULL AND cr2.name <= ai.date_invoice)
                        OR (ai.date_invoice IS NULL AND cr2.name <= NOW()))
                  ORDER BY name DESC LIMIT 1)

where ai.type in ('out_invoice', 'out_refund') and (ail.is_deposit = false and ail.is_advance = false)
    and ai.state not in ('draft', 'cancel')
    and ai.date_invoice >= '2016-09-01'
order by ai.id desc
        )""")

ws_soinvoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
