# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import fields, osv
from lxml import etree


class product_rapid_create(osv.osv):
    _inherit = "product.rapid.create"

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
        "product_customer": fields.many2one('res.partner', 'Product Customer'),
    }

    _defaults = {
        "is_continuous_line": False,
    }

    def _prepare_product(self, cr, uid, ids, new_product_name, line, object, context=None):
        prepare_product = super(product_rapid_create, self)._prepare_product(
            cr, uid, ids, new_product_name, line, object, context=context)
        prepare_product.update({
            "is_continuous_line": object.is_continuous_line,
            "partner_id": object.product_customer.id,
            "mat_in_surface_choices": line.mat_in_surface_choices.id,
            "mat_out_surface_choices": line.mat_out_surface_choices.id,
            "bom_template_id": line.bom_template_id.id,
        })
        return prepare_product

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = super(product_rapid_create, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if context is None:
            context = {}
        # Change string Panel to Continuous
        if context.get("default_is_continuous_line", False):
            if view_type == "form":
                doc = etree.XML(res["arch"])
                for node in doc.xpath("//group[@string='Panel']"):
                    node.set("string", "Continuous")
                res["arch"] = etree.tostring(doc)
        return res


class product_rapid_create_line(osv.osv):
    _inherit = "product.rapid.create.line"

    _columns = {
        "mat_width_choices": fields.many2one(
            "bom.choice.width",
            string="Width (W)",
            domain="[('bom_ids','in',[bom_template_id or 0])]",
            required=False,
            ondelete="CASCADE",
            select=True,
        ),
        "mat_in_surface_choices": fields.many2one(
            "bom.choice.surface",
            string="Surface (In)",
            domain="[('bom_ids','in',[bom_template_id or 0])]",
            required=False,
            ondelete="CASCADE",
            select=True,
        ),
        "mat_out_surface_choices": fields.many2one(
            "bom.choice.surface",
            string="Surface (Out)",
            domain="[('bom_ids','in',[bom_template_id or 0])]",
            required=False,
            ondelete="CASCADE",
            select=True,
        ),
        "is_mat_in_surface_choices_required": fields.boolean(
            string="Surface (In) Required",
            ondelete="CASCADE",
            select=True,
        ),
        "is_mat_out_surface_choices_required": fields.boolean(
            string="Surface (Out) Required",
            ondelete="CASCADE",
            select=True,
        ),
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
    }

    def onchange_mat_width_choices(self, cr, uid, ids, mat_width_choices, context=None):
        width = 0.0
        if mat_width_choices:
            width_choice_obj = self.pool.get("bom.choice.width")
            width_choice = width_choice_obj.browse(cr, uid, mat_width_choices, context=context)
            width = width_choice.value or 0.0
        return {"value": {"W": width}}

    def onchange_bom_template_id(self, cr, uid, ids, bom_template_id, context=None):
        res = super(product_rapid_create_line, self).onchange_bom_template_id(cr, uid, ids, bom_template_id, context=context)
        if bom_template_id:
            bom = self.pool.get("mrp.bom").browse(cr, uid, bom_template_id, context=context)
            res["value"].update({
                "is_mat_in_surface_choices_required": len(bom.mat_in_surface_choices) > 0,
                "is_mat_out_surface_choices_required": len(bom.mat_out_surface_choices) > 0,
            })
        return res

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        res = super(product_rapid_create_line, self).onchange_product_id(cr, uid, ids, product_id, context=context)
        if context.get("default_is_continuous_line") and product_id:
            product = self.pool.get("product.product").browse(cr, uid, product_id, context=context)
            # Thick
            thick = product.T and product.T.id or False
            # Width
            width = False
            if product.W:
                width_ids = self.pool.get("bom.choice.width").search(cr, uid, [("value", "=", product.W)], context=context)
                if len(width_ids) == 1:
                    width = width_ids[0]
            # Insulation
            insulation = product.mat_insulation_choices and product.mat_insulation_choices.id or False
            res["value"].update({
                "mat_width_choices": width,
                "T": thick,
                "mat_insulation_choices": insulation,
            })
        return res
