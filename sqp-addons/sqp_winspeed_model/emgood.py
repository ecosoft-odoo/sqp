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


class ws_emgood(osv.osv):

    _name = "ws.emgood"
    _auto = False

    _columns = {
        'goodcode': fields.char('goodcode'),
        'maingoodunitcode': fields.char('maingoodunitcode'),
        'goodname1': fields.char('goodname1'),
        'goodname2': fields.char('goodname2'),
        'goodnameeng1': fields.char('goodnameeng1'),
        'goodnameeng2': fields.char('goodnameeng2'),
        'goodmarketname': fields.char('goodmarketname'),
        'goodbillname': fields.char('goodbillname'),
        'goodtypecode': fields.char('goodtypecode'),
        'goodcatecode': fields.char('goodcatecode'),
        'goodgroupcode': fields.char('goodgroupcode'),
        'goodbrandcode': fields.char('goodbrandcode'),
        'goodpattncode': fields.char('goodpattncode'),
        'gooddesigncode': fields.char('gooddesigncode'),
        'goodgradecode': fields.char('goodgradecode'),
        'goodclasscode': fields.char('goodclasscode'),
        'goodsizecode': fields.char('goodsizecode'),
        'goodcolorcode': fields.char('goodcolorcode'),
        'multiunitflag': fields.char('multiunitflag'),
        'goodpackflag': fields.char('goodpackflag'),
        'costestimate': fields.char('costestimate'),
        'lotserialexpireflag': fields.char('lotserialexpireflag'),
        'vattype': fields.char('vattype'),
        'goodqtydefault': fields.char('goodqtydefault'),
        'gooddisc': fields.char('gooddisc'),
        'barcodeflag': fields.char('barcodeflag'),
        'goodcompareunitcode': fields.char('goodcompareunitcode'),
        'goodid': fields.char('goodid'),
        'maingoodunitid': fields.char('maingoodunitid'),
        'goodtypeid': fields.char('goodtypeid'),
        'goodcateid': fields.char('goodcateid'),
        'goodgroupid': fields.char('goodgroupid'),
        'goodbrandid': fields.char('goodbrandid'),
        'goodpattnid': fields.char('goodpattnid'),
        'gooddesignid': fields.char('gooddesignid'),
        'goodgradeid': fields.char('goodgradeid'),
        'goodclassid': fields.char('goodclassid'),
        'goodsizeid': fields.char('goodsizeid'),
        'goodcolorid': fields.char('goodcolorid'),
        'salegoodunitid': fields.char('salegoodunitid'),
        'subgoodunitid': fields.char('subgoodunitid'),
        'buygoodunitid': fields.char('buygoodunitid'),
        'freeflag': fields.char('freeflag'),
        'stockflag': fields.char('stockflag'),
        'vatrate': fields.char('vatrate'),
        'serialrunningflag': fields.char('serialrunningflag'),
        'serialrunningno': fields.char('serialrunningno'),
        'goodwide': fields.char('goodwide'),
        'goodlong': fields.char('goodlong'),
        'goodhigh': fields.char('goodhigh'),
        'measureunitid': fields.char('measureunitid'),
        'goodweightflag': fields.char('goodweightflag'),
        'goodweight': fields.char('goodweight'),
        'weightunitid': fields.char('weightunitid'),
        'standardcost': fields.char('standardcost'),
        'standardsaleprce': fields.char('standardsaleprce'),
        'standardbuyprce': fields.char('standardbuyprce'),
        'standardkeepcost': fields.char('standardkeepcost'),
        'standardtransfercost': fields.char('standardtransfercost'),
        'gooddisccondition': fields.char('gooddisccondition'),
        'returngooddisc': fields.char('returngooddisc'),
        'goodpoint': fields.char('goodpoint'),
        'goodsegcode': fields.char('goodsegcode'),
        'goodcompareunitid': fields.char('goodcompareunitid'),
        'goodunitid1': fields.char('goodunitid1'),
        'goodunitid2': fields.char('goodunitid2'),
        'commission': fields.char('commission'),
        'goodtypeflag': fields.char('goodtypeflag'),
        'checkdeficit': fields.char('checkdeficit'),
        'checkdeficitoption': fields.char('checkdeficitoption'),
        'stockmanagement': fields.char('stockmanagement'),
        'goodproduceflag': fields.char('goodproduceflag'),
        'paygooddisc': fields.char('paygooddisc'),
        'paygooddisccondition': fields.char('paygooddisccondition'),
        'inactive': fields.char('inactive'),
    }

    def init(self, cr):
        # self._table = so_inv_pay_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW ws_emgood as (
select  pp.id, pp.search_key as GoodCode,
    pu.name as maingoodunitcode,
    left(replace(pt.name, '"', ''''), 245) as GoodName1,
    null as GoodName2,
    null as GoodNameEng1,
    null as GoodNameEng2,
    pp.default_code as GoodMarketName,
    null as GoodBillName,
    case when pt.type = 'service' then 1 else 2 end as GoodTypecode,
    pc.search_key as GoodCatecode,
    null as GoodGroupcode,
    null as GoodBrandcode,
    null as GoodPattncode,
    null as GoodDesigncode,
    null as GoodGradecode,
    null as GoodClasscode,
    null as GoodSizecode,
    null as GoodColorcode,
    3 as MultiUnitFlag,
    case when pt.type = 'service' then 'S' else 'G' end as GoodPackFlag,
    1 as CostEstimate,
    0 as LotSerialExpireFlag,
    case when pt.id in (select distinct prod_id from product_taxes_rel) then 1 else 3 end  as VatType,
    0 as GoodQtyDefault,
    null as GoodDisc,
    'N' as BarCodeFlag,
    null as goodcompareunitcode,
    null as GoodID,
    null as MainGoodUnitID,
    null as GoodTypeID,
    null as GoodCateID,
    null as GoodGroupID,
    null as GoodBrandID,
    null as GoodPattnID,
    null as GoodDesignID,
    null as GoodGradeID,
    null as GoodClassID,
    null as GoodSizeID,
    null as GoodColorID,
    null as SaleGoodUnitID,
    null as SubGoodUnitID,
    null as BuyGoodUnitID,
    'N' as FreeFlag,
    case when pt.type = 'product' then 'Y' else 'N' end as StockFlag,
    0 as VatRate,
    'N' as SerialRunningFlag,
    null as SerialRunningNo,
    0 as GoodWide,
    0 as GoodLong,
    0 as GoodHigh,
    null as MeasureUnitID,
    1 as GoodWeightFlag,
    0 as GoodWeight,
    null as WeightUnitID,
    0 as StandardCost,
    0 as StandardSalePrce,
    0 as StandardBuyPrce,
    0 as StandardKeepCost,
    0 as StandardTransferCost,
    null as GoodDiscCondition,
    null as ReturnGoodDisc,
    0 as GoodPoint,
    null as GoodSegCode,
    null as GoodCompareUnitID,
    null as GoodUnitID1,
    null as GoodUnitID2,
    null as Commission,
    case when pt.type != 'service' then 'G' else 'S' end as GoodTypeFlag,
    0 as CheckDeficit,
    0 as CheckDeficitOption,
    null as StockManagement,
    0 as GoodProduceFlag,
    null as PayGoodDisc,
    null as PayGoodDiscCondition,
    case when pp.active = true then 'A' else 'I' end  as Inactive

from product_product pp join product_template pt on pt.id = pp.product_tmpl_id
left outer join product_uom pu on pu.id = pt.uom_id
left outer join product_category pc on pc.id = pt.categ_id
where is_one_time_use = false
or pp.id in (select product_id from purchase_order_line)
        )""")

ws_emgood()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
