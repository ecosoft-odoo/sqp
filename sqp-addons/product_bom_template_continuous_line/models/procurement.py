# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import fields, osv


class procurement_order(osv.osv):
    _inherit = "procurement.order"

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
    }

    _defaults = {
        "is_continuous_line": False,
    }

    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context=context)
        res["is_continuous_line"] = procurement.is_continuous_line
        return res
