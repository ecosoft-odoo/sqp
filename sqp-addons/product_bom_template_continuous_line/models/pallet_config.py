# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import fields, osv


class pallet_config(osv.osv):
    _name = "pallet.config"

    _columns = {
        "bom_template_id": fields.many2one(
            "mrp.bom",
            string="BOM Template",
            domain="[('is_bom_template', '=', True), ('is_continuous_line', '=', True)]",
            required=True,
        ),
        "is_international": fields.boolean(
            string="International",
        ),
        "line_ids": fields.one2many(
            "pallet.config.line",
            "config_id",
            string="Lines",
        )
    }


class pallet_config_line(osv.osv):
    _name = "pallet.config.line"

    _columns = {
        "config_id": fields.many2one(
            "pallet.config",
            string="Config",
        ),
        "thickness": fields.many2one(
            "bom.choice.thick",
            string="Thickness",
            required=True,
        ),
        "total_panel": fields.integer(
            string="Full Panel Per Stack",
            required=True,
        )
    }
