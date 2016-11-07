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


class ws_sodt(osv.osv):

    _name = "ws.sodt"
    _auto = False

    _columns = {
        'date': fields.date('CompareDate'),
        'brchcode': fields.char('brchcode'),
        'docuno': fields.char('docuno'),
        'goodcode': fields.char('goodcode'),
        'goodname': fields.char('goodname'),
        'invecode': fields.char('invecode'),
        'locacode': fields.char('locacode'),
        'goodunitcode': fields.char('goodunitcode'),
        'maingoodunitcode': fields.char('maingoodunitcode'),
        'goodstockrate2': fields.char('goodstockrate2'),
        'goodqty2': fields.char('goodqty2'),
        'goodprice2': fields.char('goodprice2'),
        'gooddiscformula': fields.char('gooddiscformula'),
        'gooddiscamnt': fields.char('gooddiscamnt'),
        'goodamnt': fields.char('goodamnt'),
        'miscchargformula': fields.char('miscchargformula'),
        'miscchargamnt': fields.char('miscchargamnt'),
        'jobcode': fields.char('jobcode'),
        'goodcompareunitcode': fields.char('goodcompareunitcode'),
        'goodcompareqty': fields.char('goodcompareqty'),
        'vattype': fields.char('vattype'),
        'docutype': fields.char('docutype'),
        'soid': fields.char('soid'),
        'listno': fields.char('listno'),
        'refsoid': fields.char('refsoid'),
        'goodcompareunitid': fields.char('goodcompareunitid'),
        'jobid': fields.char('jobid'),
        'vatgroupid': fields.char('vatgroupid'),
        'goodid': fields.char('goodid'),
        'inveid': fields.char('inveid'),
        'locaid': fields.char('locaid'),
        'goodunitid1': fields.char('goodunitid1'),
        'goodprice1': fields.char('goodprice1'),
        'goodqty1': fields.char('goodqty1'),
        'goodunitid2': fields.char('goodunitid2'),
        'goodstockrate1': fields.char('goodstockrate1'),
        'gooddisctype': fields.char('gooddisctype'),
        'chargremark': fields.char('chargremark'),
        'sumexcludeamnt': fields.char('sumexcludeamnt'),
        'markup': fields.char('markup'),
        'contactname': fields.char('contactname'),
        'shiptoaddr1': fields.char('shiptoaddr1'),
        'shiptoaddr2': fields.char('shiptoaddr2'),
        'district': fields.char('district'),
        'amphur': fields.char('amphur'),
        'province': fields.char('province'),
        'postcode': fields.char('postcode'),
        'fax': fields.char('fax'),
        'tel': fields.char('tel'),
        'shipdue': fields.char('shipdue'),
        'shipdate': fields.char('shipdate'),
        'reflistno': fields.char('reflistno'),
        'remabefoqty': fields.char('remabefoqty'),
        'remark': fields.char('remark'),
        'lotno': fields.char('lotno'),
        'lotflag': fields.char('lotflag'),
        'goodtype': fields.char('goodtype'),
        'serialflag': fields.char('serialflag'),
        'goodstockunitid': fields.char('goodstockunitid'),
        'postflag': fields.char('postflag'),
        'goodstockqty': fields.char('goodstockqty'),
        'goodcost': fields.char('goodcost'),
        'vatrate': fields.char('vatrate'),
        'stockflag': fields.char('stockflag'),
        'goodflag': fields.char('goodflag'),
        'remaqty': fields.char('remaqty'),
        'reserveqty': fields.char('reserveqty'),
        'freeflag': fields.char('freeflag'),
        'resvstr1': fields.char('resvstr1'),
        'resvstr2': fields.char('resvstr2'),
        'resvstr3': fields.char('resvstr3'),
        'resvamnt1': fields.char('resvamnt1'),
        'resvamnt2': fields.char('resvamnt2'),
        'resvdate1': fields.char('resvdate1'),
        'goodremaqty1': fields.char('goodremaqty1'),
        'goodremaqty2': fields.char('goodremaqty2'),
        'shiptocode': fields.char('shiptocode'),
        'markupamnt': fields.char('markupamnt'),
        'commisformula': fields.char('commisformula'),
        'commisamnt': fields.char('commisamnt'),
        'refno': fields.char('refno'),
        'poqty': fields.char('poqty'),
        'remaqtypkg': fields.char('remaqtypkg'),
        'expireflag': fields.char('expireflag'),
        'poststock': fields.char('poststock'),
        'aftermarkupamnt': fields.char('aftermarkupamnt'),
        'remagoodstockqty': fields.char('remagoodstockqty'),
        'brchid': fields.char('brchid'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_sodt as (
    select sol.id, so.date_order as date,
    '00000' as brchcode,
    so.name as DocuNo,
    pp.search_key as goodcode,
    left(replace(pp.name_template, '"', ''''), 255) as GoodName,
    sw.name as invecode,
    sl.name as locacode,  -- Can we use shop in ERP?
    pu.name as goodunitcode,
    -- mainggoodunitcode is from a specific requirement that non-standard must alwasy be 'cm'
    case when pt.type != 'service' then pu.name else 'cm' end as maingoodunitcode,  -- Same as goodunitcode ???
    case when pt.type != 'service' then 1 else null end as GoodStockRate2,
    round(sol.product_uom_qty, 4) as GoodQty2,  -- What is "2" means?
    round(sol.price_unit, 4) as GoodPrice2,
    round(sol.discount/100 * sol.product_uom_qty * sol.price_unit, 4) as GoodDiscFormula,
    round(sol.discount/100 * sol.product_uom_qty * sol.price_unit, 4) as GoodDiscAmnt, -- Saem as GoodDiscFormula?
    round((sol.product_uom_qty * sol.price_unit) - (sol.discount/100 * sol.product_uom_qty * sol.price_unit), 4) as GoodAmnt,
    null as MiscChargFormula,
    0 as MiscChargAmnt,
    null as jobcode,
    null as goodcompareunitcode,
    null as GoodCompareQty,
    null as VatType,  -- Has tax = 1, no tax = 3
    null as DocuType,
    null as SOID,
    row_number() over(partition by so.id order by sol.id) as ListNo,
    null as RefSOID,
    null as GoodCompareUnitID,
    null as JobID,
    null as VATGroupID,
    null as GoodID,
    null as InveID,
    null as LocaID,
    null as GoodUnitID1,
    null as GoodPrice1,  -- What about GoodPrice2?
    null as GoodQty1,
    null as GoodUnitID2,
    0 as GoodStockRate1,
    null as GoodDiscType,
    null as ChargRemark,
    null as SumExcludeAmnt,
    null as MarkUp,
    null as ContactName,
    null as ShipToAddr1,
    null as ShipToAddr2,
    null as District,
    null as Amphur,
    null as Province,
    null as PostCode,
    null as Fax,
    null as Tel,
    null as ShipDue,
    to_char(so.date_order + cast('1 day' as interval) * sol.delay, 'dd/mm/yyyy') as ShipDate,
    null as RefListNo,
    null as RemaBefoQty,
    null as Remark,
    null as LotNo,
    null as LotFlag,
    case when pt.type != 'service' then 1 else 2 end as GoodType,
    null as SerialFlag,
    null as GoodStockUnitID,
    null as PostFlag,
    sol.product_uom_qty as GoodStockQty,
    null as GoodCost,
    case when coalesce(nullif(so.amount_net, 0.0), 0.0) = 0 then 0
        else round((so.amount_total - so.amount_net)
        / so.amount_net * 100, 2) end as VatRate,
    null as StockFlag,
    case when pt.type != 'service' then 'G' else 'S' end as GoodFlag,
    sol.product_uom_qty as RemaQty,
    null as ReserveQty,  -- Should be computed field, isn't it?
    null as FreeFlag,
    null as ResvStr1,
    null as ResvStr2,
    null as ResvStr3,
    0 as ResvAmnt1,
    0 as ResvAmnt2,
    null as ResvDate1,
    sol.product_uom_qty as GoodRemaQty1,
    sol.product_uom_qty as GoodRemaQty2,
    null as ShipToCode,
    null as MarkUpAmnt,
    null as CommisFormula,
    null as CommisAmnt,
    null as Refno,
    sol.product_uom_qty as POQty,
    sol.product_uom_qty as RemaQtyPkg,
    null as Expireflag,
    null as Poststock,
    null as AfterMarkupamnt,
    sol.product_uom_qty RemaGoodStockQty,
    null brchid

from sale_order so
join sale_order_line sol on so.id = sol.order_id
left outer join product_product pp on pp.id = sol.product_id
left outer join product_template pt on pt.id = pp.product_tmpl_id
left outer join product_uom pu on pu.id = sol.product_uom
left outer join res_partner rp on rp.id = so.partner_id
left outer join account_payment_term apt on apt.id = so.payment_term
left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
left outer join res_users ru on ru.id = so.user_id
left outer join product_pricelist ppl on ppl.id = so.pricelist_id
left outer join res_currency rc on rc.id = ppl.currency_id
left outer join sale_shop ss on ss.id = so.shop_id
left outer join stock_warehouse sw on sw.id = ss.warehouse_id
left outer join stock_location sl on sl.id = sw.lot_stock_id
JOIN res_currency_rate cr ON (cr.currency_id = ppl.currency_id)
    AND
    cr.id IN (SELECT id
      FROM res_currency_rate cr2
      WHERE (cr2.currency_id = ppl.currency_id)
          AND ((so.date_order IS NOT NULL AND cr2.name <= so.date_order)
        OR (so.date_order IS NULL AND cr2.name <= NOW()))
      ORDER BY name DESC LIMIT 1)
where so.state in ('progress', 'manual', 'done')
order by so.id desc, sol.id
        )""")

ws_sodt()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
