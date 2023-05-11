# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import fields, osv


class product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
        "mat_in_surface_choices": fields.many2one(
            "bom.choice.surface",
            string="Surface (In)",
        ),
        "mat_out_surface_choices": fields.many2one(
            "bom.choice.surface",
            string="Surface (Out)",
        ),
        "bom_template_id": fields.many2one(
            "mrp.bom",
            string="BOM Template",
        )
    }

    _defaults = {
        "is_continuous_line": False,
    }
