# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv


class ws_podeposit(osv.osv):

    _name = "ws.podeposit"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'docuno': fields.char('docuno'),
        'docudate': fields.char('docudate'),
        'invno': fields.char('invno'),
        'invdate': fields.char('invdate'),
        'vendercode': fields.char('vendercode'),
        'vendername': fields.char('vendername'),
        'contact': fields.char('contact'),
        'creditstartdate': fields.char('creditstartdate'),
        'creditdays': fields.char('creditdays'),
        'paydate': fields.char('paydate'),
        'jobcode': fields.char('jobcode'),
        'jobname': fields.char('jobname'),
        'pono': fields.char('pono'),
        'ponodt': fields.char('ponodt'),
        'goodremark': fields.char('goodremark'),
        'goodamount': fields.char('goodamount'),
        'sumgoodamnt': fields.char('sumgoodamnt'),
        'totalbaseamnt': fields.char('totalbaseamnt'),
        'vatrate': fields.char('vatrate'),
        'vatamnt': fields.char('vatamnt'),
        'netamnt': fields.char('netamnt'),
        'vatgroupcode': fields.char('vatgroupcode'),
        'departmentcode': fields.char('departmentcode'),
        'departmentname': fields.char('departmentname'),
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
        cr.execute("""CREATE or REPLACE VIEW ws_podeposit as (
select ail.id, ai.date_invoice as date,
    ai.number as Docuno,
    to_char(ai.date_invoice, 'dd/mm/yyyy') as Docudate,
    ai.number as InvNo,
    to_char(ai.date_invoice, 'dd/mm/yyyy') as InvDate,
    rp.search_key as VenderCode,
    rp.name as VenderName,
    null as Contact,
    null as Creditstartdate,
    aptl.days as CreditDays,
    to_char(ai.date_due, 'dd/mm/yyyy') as Paydate,
    null as JobCode,
    null as JobName,
    po.name as PoNo,
    po.name as PoNoDT,
    ail.name as Goodremark,
    ail.price_subtotal as GoodAmount,
    ai.amount_beforetax as Sumgoodamnt,
    ai.amount_beforetax as TotalBaseAmnt,
    round((ai.amount_total - ai.amount_beforetax)
        / ai.amount_beforetax * 100, 2) as VatRate,
    (ai.amount_total - ai.amount_beforetax) as VatAmnt,
    ai.amount_total as Netamnt,
    case when round((ai.amount_total - ai.amount_beforetax)
        / ai.amount_beforetax * 100, 2) = 7
        then 'PO-EX7' else 'NO' end as VatGroupCode,
    null as DepartmentCode,
    null as DepartmentName,
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
    left outer join purchase_invoice_rel pir on pir.invoice_id = ai.id
    left outer join purchase_order po on po.id = pir.purchase_id
    left outer join stock_warehouse sw on sw.id = po.warehouse_id
    left outer join stock_location sl on sl.id = sw.lot_stock_id

    JOIN res_currency_rate cr ON (cr.currency_id = ai.currency_id)
            AND
            cr.id IN (SELECT id
                  FROM res_currency_rate cr2
                  WHERE (cr2.currency_id = ai.currency_id)
                      AND ((ai.date_invoice IS NOT NULL AND cr2.name <= ai.date_invoice)
                        OR (ai.date_invoice IS NULL AND cr2.name <= NOW()))
                  ORDER BY name DESC LIMIT 1)

where ai.type = 'in_invoice' and (ail.is_deposit = true or ail.is_advance = true)
    and ai.state not in ('draft', 'cancel')
order by ai.id desc
        )""")

ws_podeposit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
