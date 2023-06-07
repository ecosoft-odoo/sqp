# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import fields, osv
from openerp.tools.translate import _


class product_make_bom(osv.osv_memory):
    _inherit = "product.make.bom"

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(product_make_bom, self).default_get(cr, uid, fields, context=context)
        # If context is none, let return res
        if context is None:
            return res
        # Default Continuous Line from product page
        active_model = context.get("active_model")
        active_ids = context.get("active_ids")
        if active_model == "product.product" and active_ids:
            products = self.pool.get(active_model).browse(cr, uid, active_ids, context=context)
            is_continuous_lines = list(set([product.is_continuous_line for product in products]))
            if is_continuous_lines:
                if len(is_continuous_lines) > 1:
                    raise osv.except_osv(_("User Error"), _("No products or bills of materials are allowed to be created with a mixture of 'continuous lines'."))
                res["is_continuous_line"] = is_continuous_lines[0]
        return res
