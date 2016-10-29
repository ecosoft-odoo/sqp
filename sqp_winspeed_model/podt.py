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


class ws_podt(osv.osv):

    _name = "ws.podt"
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
        'jobcode': fields.char('jobcode'),
        'goodcompareunitcode': fields.char('goodcompareunitcode'),
        'goodcompareqty': fields.char('goodcompareqty'),
        'vattype': fields.char('vattype'),
        'docutype': fields.char('docutype'),
        'poid': fields.char('poid'),
        'listno': fields.char('listno'),
        'inveid': fields.char('inveid'),
        'dropshipid': fields.char('dropshipid'),
        'goodid': fields.char('goodid'),
        'vendorid': fields.char('vendorid'),
        'vatgroupid': fields.char('vatgroupid'),
        'locaid': fields.char('locaid'),
        'jobid': fields.char('jobid'),
        'goodunitid1': fields.char('goodunitid1'),
        'goodqty1': fields.char('goodqty1'),
        'goodprice1': fields.char('goodprice1'),
        'goodunitid2': fields.char('goodunitid2'),
        'goodstockrate1': fields.char('goodstockrate1'),
        'appvqty1': fields.char('appvqty1'),
        'goodremaqty1': fields.char('goodremaqty1'),
        'goodcompareunitid': fields.char('goodcompareunitid'),
        'appvgoodamnt': fields.char('appvgoodamnt'),
        'appvqty2': fields.char('appvqty2'),
        'goodremaqty2': fields.char('goodremaqty2'),
        'goodstockunitid': fields.char('goodstockunitid'),
        'goodstockqty': fields.char('goodstockqty'),
        'goodcost': fields.char('goodcost'),
        'goodtype': fields.char('goodtype'),
        'goodremark': fields.char('goodremark'),
        'stockflag': fields.char('stockflag'),
        'vatrate': fields.char('vatrate'),
        'quotselected': fields.char('quotselected'),
        'lotflag': fields.char('lotflag'),
        'lotno': fields.char('lotno'),
        'serialflag': fields.char('serialflag'),
        'totaaddcost': fields.char('totaaddcost'),
        'poststock': fields.char('poststock'),
        'receplace1': fields.char('receplace1'),
        'receplace2': fields.char('receplace2'),
        'district': fields.char('district'),
        'amphur': fields.char('amphur'),
        'provice': fields.char('provice'),
        'postcode': fields.char('postcode'),
        'tel': fields.char('tel'),
        'fax': fields.char('fax'),
        'vendorlotno': fields.char('vendorlotno'),
        'fromdocutype': fields.char('fromdocutype'),
        'misccharg': fields.char('misccharg'),
        'miscchargamnt': fields.char('miscchargamnt'),
        'appvflag': fields.char('appvflag'),
        'refpoid': fields.char('refpoid'),
        'reflistno': fields.char('reflistno'),
        'cancelflag': fields.char('cancelflag'),
        'canceldate': fields.char('canceldate'),
        'cancelcause': fields.char('cancelcause'),
        'freeflag': fields.char('freeflag'),
        'appvremark': fields.char('appvremark'),
        'completeflag': fields.char('completeflag'),
        'goodflag': fields.char('goodflag'),
        'refvendorid': fields.char('refvendorid'),
        'refqutpoid': fields.char('refqutpoid'),
        'refqutlistno': fields.char('refqutlistno'),
        'expireflag': fields.char('expireflag'),
        'refsolistno': fields.char('refsolistno'),
        'refsoid': fields.char('refsoid'),
        'remagoodstockqty': fields.char('remagoodstockqty'),
        'brchid': fields.char('brchid'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_podt as (
select pol.id, po.date_order as date,
    '00000' as brchcode,
    replace(po.name, '"', '''') as DocuNo,
    pp.search_key as goodcode,
    left(replace(pt.name, '"', ''''), 255) as GoodName,
    sw.name as invecode,
    sl.name as locacode,
    pu.name as goodunitcode,
    case when pt.categ_id not in (6, 36) then pu.name else 'cm' end as maingoodunitcode,  -- Same as goodunitcode ???
    case when pt.categ_id not in (6, 36) then 1 else null end as GoodStockRate2,
    round(pol.product_qty, 4) as GoodQty2,
    round(pol.price_unit, 2) as GoodPrice2,
    round(pol.discount/100 * pol.product_qty * pol.price_unit, 2) as GoodDiscFormula,
    round(pol.discount/100 * pol.product_qty * pol.price_unit, 2) as GoodDiscAmnt,
    round((pol.product_qty * pol.price_unit) - (pol.discount/100 * pol.product_qty * pol.price_unit), 2) as GoodAmnt,
    null as jobcode,
    null as goodcompareunitcode,
    null as GoodCompareQty,
    case when po.amount_tax > 0 then 1 else 3 end  as VatType,
    '305' as DocuType,
    null as POID,
    row_number() over(partition by po.id order by pol.id) as ListNo,
    null as InveID,
    null as DropShipID,
    null as GoodID,
    null as VendorID,
    null as VATGroupID,
    null as LocaID,
    null as JobID,
    null as GoodUnitID1,
    null as GoodQty1,
    null as GoodPrice1,
    null as GoodUnitID2,
    null as GoodStockRate1,
    null as AppvQty1,
    round(pol.product_qty, 4) as GoodRemaQty1,
    null as GoodCompareUnitID,
    round((pol.product_qty * pol.price_unit) - (pol.discount/100 * pol.product_qty * pol.price_unit), 2) as AppvGoodAmnt,
    round(pol.product_qty, 4) as AppvQty2,
    round(pol.product_qty, 4) as GoodRemaQty2,
    null as GoodStockUnitID,
    null as GoodStockQty,
    null as GoodCost,
    case when pt.type = 'service' then 2 else 1 end as GoodType,
    null as GoodRemark,
    null as StockFlag,
    round(case when coalesce(nullif(po.amount_net, 0.0), 0.0) = 0 then 0
    else round((po.amount_total - po.amount_net)
    / po.amount_net * 100, 2) end, 2) as VATRate,
    null as QuotSelected,
    null as LotFlag,
    null as LotNo,
    null as SerialFlag,
    null as TotaAddCost,
    null as PostStock,
    null as RecePlace1,
    null as RecePlace2,
    null as District,
    null as Amphur,
    null as Provice,
    null as PostCode,
    null as Tel,
    null as Fax,
    null as VendorLotNo,
    null as FromDocuType,
    null as MiscCharg,
    null as MiscChargAmnt,
    null as AppvFlag,
    null as RefPOID,
    null as RefListNo,
    null as CancelFlag,
    null as CancelDate,
    null as CancelCause,
    null as FreeFlag,
    null as AppvRemark,
    null as CompleteFlag,
    case when pt.type = 'service' then 'S' else 'G' end as GoodFlag,
    null as RefVenDorID,
    null as RefQutPOID,
    null as RefQutListNo,
    null as expireflag,
    null as RefSolistNo,
    null as RefSOID,
    round(pol.product_qty, 4) as RemaGoodStockQty,
    null as brchid
from purchase_order po
join purchase_order_line pol on po.id = pol.order_id
left outer join product_product pp on pp.id = pol.product_id
left outer join product_template pt on pt.id = pp.product_tmpl_id
left outer join product_uom pu on pu.id = pol.product_uom
left outer join res_partner rp on rp.id = po.partner_id
left outer join account_payment_term apt on apt.id = po.payment_term_id
left outer join account_payment_term_line aptl on aptl.payment_id = apt.id
left outer join purchase_requisition pr on pr.id = po.requisition_id
left outer join res_users ru on ru.id = pr.user_id
left outer join product_pricelist ppl on ppl.id = po.pricelist_id
left outer join res_currency rc on rc.id = ppl.currency_id
left outer join stock_warehouse sw on sw.id = po.warehouse_id
left outer join stock_location sl on sl.id = sw.lot_stock_id
JOIN res_currency_rate cr ON (cr.currency_id = ppl.currency_id)
    AND
    cr.id IN (SELECT id
      FROM res_currency_rate cr2
      WHERE (cr2.currency_id = ppl.currency_id)
          AND ((po.date_order IS NOT NULL AND cr2.name <= po.date_order)
        OR (po.date_order IS NULL AND cr2.name <= NOW()))
      ORDER BY name DESC LIMIT 1)
where po.state in ('confirmed', 'approved', 'done')
order by po.id desc, pol.id
        )""")

ws_podt()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
