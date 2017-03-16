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


class ws_sodeposit(osv.osv):

    _name = "ws.sodeposit"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'invno': fields.char('invno'),
        'invdate': fields.char('invdate'),
        'custcode': fields.char('custcode'),
        'custname': fields.char('custname'),
        'jobcode': fields.char('jobcode'),
        'jobname': fields.char('jobname'),
        'sono': fields.char('sono'),
        'creditstartdate': fields.char('creditstartdate'),
        'creditdays': fields.char('creditdays'),
        'duedate': fields.char('duedate'),
        'empcode': fields.char('empcode'),
        'empname': fields.char('empname'),
        'custpono': fields.char('custpono'),
        'custpodate': fields.char('custpodate'),
        'refeno': fields.char('refeno'),
        'goodremark': fields.char('goodremark'),
        'goodamount': fields.char('goodamount'),
        'sumgoodamnt': fields.char('sumgoodamnt'),
        'totalbaseamnt': fields.char('totalbaseamnt'),
        'vatrate': fields.char('vatrate'),
        'vatamnt': fields.char('vatamnt'),
        'netamnt': fields.char('netamnt'),
        'vatgroupcode': fields.char('vatgroupcode'),
        'saleareacode': fields.char('saleareacode'),
        'saleareaname': fields.char('saleareaname'),
        'departmentcode': fields.char('departmentcode'),
        'departmentname': fields.char('departmentname'),
        'contactname': fields.char('contactname'),
        'exchdate': fields.char('exchdate'),
        'currcode': fields.char('currcode'),
        'currname': fields.char('currname'),
        'currtypecode': fields.char('currtypecode'),
        'currtypename': fields.char('currtypename'),
        'exchrate': fields.char('exchrate'),
        'no': fields.char('no'),
        'desciption': fields.char('desciption'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_sodeposit as (
select ail.id, ai.date_invoice as date,
    ai.number as DocuNo,
    to_char(ai.date_invoice, 'dd/mm/yyyy') as DocuDate,
    ai.number as InvNo,
    to_char(ai.date_invoice, 'dd/mm/yyyy') as InvDate,
    rp.search_key as CustCode,
    rp.name as CustName,
    null as JobCode,
    null as JobName,
    so.name as SONo,
    null as CreditStartDate,
    aptl.days as CreditDays,
    to_char(ai.date_due, 'dd/mm/yyyy') as DueDate,
    ru.search_key as EmpCode,
    ru.login as EmpName,
    null as CustPONo, -- In ERP, it is just a Description
    null as CustPODate,
    so.name RefeNo,
    case when ai.note is null then '-' else ai.note end as Goodremark,
    ail.price_subtotal as GoodAmount,
    ai.amount_beforetax as Sumgoodamnt,
    ai.amount_beforetax as TotalBaseAmnt,
    case when coalesce(nullif(ai.amount_beforetax, 0.0), 0.0) = 0 then 0
    else round((ai.amount_total - ai.amount_beforetax)
        / ai.amount_beforetax * 100, 0) end as VatRate,
    (ai.amount_total - ai.amount_beforetax) as VatAmnt,
    ai.amount_total as Netamnt,
    case when round((ai.amount_total - ai.amount_beforetax)
        / ai.amount_beforetax * 100, 0) = 7
        then 'SO-EX7' else 'NO' end as VatGroupCode,
    null as SaleAreaCode,
    null as SaleAreaName,
    null as DepartmentCode,
    null as DepartmentName,
    null as ContactName,
    to_char(ai.date_invoice, 'dd/mm/yyyy') as ExchDate,
    case when rc.name = 'THB' then null else rc.name end as Currcode,
    case when rc.name = 'THB' then null else rc.name end as CurrName,
    case when rc.name = 'THB' then null else rc.name end as CurrTypecode,
    case when rc.name = 'THB' then null else rc.name end as CurrTypeName,
    round(cr.rate, 4) as Exchrate,
    1 as No,
    ail.name as Desciption

from account_invoice ai
    join account_invoice_line ail on ail.invoice_id = ai.id
    join res_partner rp on rp.id = ai.partner_id
    left outer join res_currency rc on rc.id = ai.currency_id
    left outer join account_payment_term apt on apt.id = ai.payment_term
    left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
    left outer join sale_order_invoice_rel sir on sir.invoice_id = ai.id
    left outer join sale_order so on so.id = sir.order_id
    left outer join res_users ru on ru.id = so.user_id

    JOIN res_currency_rate cr ON (cr.currency_id = ai.currency_id)
            AND
            cr.id IN (SELECT id
                  FROM res_currency_rate cr2
                  WHERE (cr2.currency_id = ai.currency_id)
                      AND ((ai.date_invoice IS NOT NULL AND cr2.name <= ai.date_invoice)
                        OR (ai.date_invoice IS NULL AND cr2.name <= NOW()))
                  ORDER BY name DESC LIMIT 1)

where ai.type in ('out_invoice') and (ail.is_deposit = true or ail.is_advance = true)
    and ai.state not in ('draft', 'cancel')
    and ail.price_subtotal > 0
order by ai.id desc
        )""")

ws_sodeposit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
