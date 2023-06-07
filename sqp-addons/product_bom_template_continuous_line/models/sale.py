# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import osv

header_msg = "<div>" + \
                "<b>Heat Insulation Sandwich Panel</b><br>" + \
                "<b>Product of Square Panel System Co., Ltd.</b><br>" + \
                "<b><u>Specification :</u></b>" + \
                "<ul>" + \
                    "<li>Density : 40~45 kg/m3</li>" + \
                    "<li>Core material &nbsp;: Polyisocyanorate Foam ( PIR )</li>" + \
                    "<li>Surface material : Color steel sheet (T) 0.50 mm.</li>" + \
                    "<li>Color Steel Sheet - Outside : Off white</li>" + \
                    "<li>Color Steel Sheet - Inside : Off white</li>" + \
                    "<li>Panel Thickness : ______ mm. (External)</li>" + \
                    "<li>Joint : </li>" + \
                "</ul>" + \
             "</div>"


class sale_order(osv.osv):
    _inherit = "sale.order"

    def onchange_product_tag_id(self, cr, uid, ids, product_tag_id, context=None):
        res = super(sale_order, self).onchange_product_tag_id(cr, uid, ids, product_tag_id, context=context)
        # Overwrite header text for quotation type of continuous
        if product_tag_id:
            tag = self.pool.get("product.tag").browse(cr, uid, product_tag_id, context=context)
            if tag.name.upper() == "CONTINUOUS":
                res["header_msg"] = header_msg
        return res
