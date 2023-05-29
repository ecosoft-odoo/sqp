# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from osv import fields, osv
from openerp.tools.translate import _


# Bill of Material
class mrp_bom(osv.osv):
    _inherit = "mrp.bom"

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
        "mat_width_choices": fields.many2many(
            "bom.choice.width",
            string="Width Choices",
        ),
        "mat_in_surface_choices": fields.many2many(
            "bom.choice.surface",
            string="Surface (In) Choices",
        ),
        "mat_out_surface_choices": fields.many2many(
            "bom.choice.surface",
            string="Surface (Out) Choices",
        ),
    }

    _defaults = {
        "is_continuous_line": False,
    }

    def update_is_continuous_line(self, cr, uid, id, context=None):
        bom = self.browse(cr, uid, id, context=context)
        for bom_line in bom.bom_lines:
            # Continuous Line on BOM Line must equal to BOM
            if bom_line.is_continuous_line != bom.is_continuous_line:
                self.write(
                    cr, uid, bom_line.id,
                    {"is_continuous_line": bom.is_continuous_line}, context=context)
        return True

    def create(self, cr, uid, vals, context=None):
        bom_id = super(mrp_bom, self).create(cr, uid, vals, context=context)
        self.update_is_continuous_line(cr, uid, bom_id, context=context)
        return bom_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(mrp_bom, self).write(cr, uid, ids, vals, context=context)
        if "is_continuous_line" in vals:
            ids = not isinstance(ids, list) and [ids] or ids
            for id in ids:
                self.update_is_continuous_line(cr, uid, id, context=context)
        return res

    def action_product_bom_create(self, cr, uid, product_ids, data, context=None):
        product_id, bom_id = super(mrp_bom, self).action_product_bom_create(
            cr, uid, product_ids, data, context=context
        )
        # Update product
        self.pool.get("product.product").write(cr, uid, product_id, {
            "is_continuous_line": data["is_continuous_line"],
        }, context=context)
        # Update BOM
        self.write(cr, uid, bom_id, {
            "is_continuous_line": data["is_continuous_line"],
        }, context=context)
        # Update BOM Lines
        bom = self.browse(cr, uid, bom_id, context=context)
        for bom_line in bom.bom_lines:
            self.write(cr, uid, bom_line.id, {
                "is_continuous_line": bom.is_continuous_line,
            }, context=context)
        return product_id, bom_id


# MO
class mrp_production(osv.osv):
    _inherit = "mrp.production"

    def _get_is_continuous_line(self, cr, uid, context=None):
        if context is None:
            context = {}
        # Default Continuous Line from product page
        active_model = context.get("active_model")
        active_ids = context.get("active_ids")
        if active_model == "product.product" and active_ids:
            products = self.pool.get(active_model).browse(cr, uid, active_ids, context=context)
            is_continuous_lines = list(set([product.is_continuous_line for product in products]))
            if is_continuous_lines:
                if len(is_continuous_lines) > 1:
                    raise osv.except_osv(_("User Error"), _("No manufacturing orders are allowed to be created with a mixture of 'continuous lines'."))
                return is_continuous_lines[0]
        return False

    def _progress_rate(self, cr, uid, ids, names, arg, context=None):
        res = super(mrp_production, self)._progress_rate(cr, uid, ids, names, arg, context=context)
        # --
        production_status_obj = self.pool.get("mrp.production.status")
        stages = ["sc"]

        for id in ids:
            mrp_prod = self.browse(cr, uid, id, context=context)
            if not mrp_prod.is_continuous_line:
                continue
            # compute progress rates for continuous line
            line_ids = production_status_obj.search(cr, uid, [("production_id", "=", id)])
            results = production_status_obj.read(cr, uid, line_ids, ["product_qty"] + stages)
            num_products = len(results) # I.e., 5 product lines
            actual_total = 0.0
            for result in results:
                actual_line_total = 0.0
                planned_line = result["product_qty"]
                if planned_line:
                    for stage in stages:
                        actual_line = result[stage]
                        actual_line_total += actual_line

                    ratio_completion = (actual_line_total/planned_line)
                    actual_total += ratio_completion > 1 and 1 or ratio_completion
                    res[id]["progress_rate"] = 100 * (actual_total/num_products)
                else:
                    res[id]["progress_rate"] = 0.0
        return res

    def _get_mrp_production(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('mrp.production.status').browse(cr, uid, ids, context=context):
            result[line.production_id.id] = True
        return result.keys()

    _columns = {
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
        "line_number_sc": fields.selection(
            selection=[
                ("L1", "Line 1"),
                ("L2", "Line 2"),
                ("L3", "Line 3"),
                ("L4", "Line 4"),
                ("L5", "Line 5"),
                ("L6", "Line 6"),
                ("L7", "Line 7"),
            ],
            string="Line # sc",
        ),
        "progress_rate": fields.function(
            _progress_rate,
            multi="progress",
            string="Progress",
            type="float",
            group_operator="avg",
            help="Percent of tasks closed according to the total of tasks todo.",
            store = {
                "mrp.production": (lambda self, cr, uid, ids, c={}: ids, ["status_lines","num_stations"], 10),
                "mrp.production.status": (_get_mrp_production, ["s1", "s2", "s3", "s4", "s5", "sc", "num_stations"], 10),
            },
        ),
        "continuous_status_lines": fields.one2many(
            "mrp.production.status",
            "production_id",
            string="Status Tracking",
            readonly=False,
            states={"done": [("readonly", True)]},
        ),
        "continuous_product_lines": fields.one2many(
            "mrp.production.product.line",
            "production_id",
            string="Scheduled goods",
            readonly=True,
            states={"draft": [("readonly", False)]},
        ),
    }

    _defaults = {
        "is_continuous_line": _get_is_continuous_line,
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(mrp_production, self).write(cr, uid, ids, vals, context=context)
        if vals.get("line_number_sc", False):
            mo = self.browse(cr, uid, ids[0])
            if not mo.parent_id and mo.child_ids:  # For a parent,
                # update statue tracking line
                status_line_ids = [x.id for x in mo.status_lines]
                self.pool.get("mrp.production.status").write(cr, uid, status_line_ids,
                                                             {"sc_line": vals.get("line_number_sc")},
                                                             context=context)
        return res

    def _hook_create_post_procurement(self, cr, uid, production, procurement_id, context=None):
        self.pool.get("procurement.order").write(cr, uid, procurement_id, {"is_continuous_line": production.is_continuous_line}, context=context)
        return super(mrp_production, self)._hook_create_post_procurement(cr, uid, production, procurement_id, context=context)


# Width Choice
class bom_choice_width(osv.osv):
    _name = "bom.choice.width"
    _description = "Width Choice when create BOM"
    
    _columns = {
        "name": fields.char(
            string="Name",
            required=True,
        ),
        "value": fields.float(
            string="Value",
            required=True,
        ),
        "bom_ids": fields.many2many(
            "mrp.bom",
            string="BOMs",
        ),
    }


# Surface Choice
class bom_choice_surface(osv.osv):
    _name = "bom.choice.surface"
    _description = "Surface Choice when create BOM"

    _columns = {
        "name": fields.char(
            string="Name",
            required=True,
        ),
        "bom_ids": fields.many2many(
            "mrp.bom",
            string="BOMs",
        ),
    }


# MO Status Tracking
class mrp_production_status(osv.osv):
    _inherit = "mrp.production.status"

    _columns = {
        "sc": fields.float(
            string="SC",
        ),
        "sc_line": fields.selection(
            selection=[
                ("L1", "Line 1"),
                ("L2", "Line 2"),
                ("L3", "Line 3"),
                ("L4", "Line 4"),
                ("L5", "Line 5"),
                ("L6", "Line 6"),
                ("L7", "Line 7"),
            ],
            string="SCL#",
        )
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(mrp_production_status, self).write(cr, uid, ids, vals, context=context)
        if not isinstance(ids, list):
            ids = [ids]
        for mp_status in self.pool.get("mrp.production.status").browse(cr, uid, ids):
            if mp_status.sc > mp_status.product_qty:
                raise osv.except_osv(_("Can not save change!"),
                                 _("Some subsequence value in Status Tracking still greater than product quantity"))
        return res


# Machine Setup Master
class mrp_machine_setup_master(osv.osv):
    _inherit = "mrp.machine.setup.master"

    _columns = {
        "name": fields.selection([
            ("line1", "Line 1"),
            ("line2", "Line 2"),
            ("line3", "Line 3"),
            ("line4", "Line 4"),
            ("line5", "Line 5"),
            ("line_pir1_pir", "Line PIR1 (PIR)"),
            ("line_pir1_pu", "Line PIR1 (PU)"),
            ("line_pir2_pir", "Line PIR2 (PIR)"),
            ("line_pir2_pu", "Line PIR2 (PU)"),
            ("line_pir3_pir", "Line PIR3 (PIR)"),
            ("line_pir3_pu", "Line PIR3 (PU)"),
            ("line_slipjoint_pir", "Line Slip Joint (PIR)"),
            ("line_slipjoint_pu", "Line Slip Joint (PU)"),
            ("line_secretjoint_pir", "Line Secret Joint (PIR)"),
            ("line_secretjoint_pu", "Line Secret Joint (PU)"),
            ("line_roofjoint_pir", "Line Roof Joint (PIR)"),
            ("line_roofjoint_pu", "Line Roof Joint (PU)"),
            ("line_board_pir", "Line Board (PIR)"),
            ("line_board_pu", "Line Board (PU)")],
            string="Machine",
        ),
        "is_continuous_line": fields.boolean(
            string="Continuous Line",
        ),
        "bom_template_id": fields.many2one(
            "mrp.bom",
            string="BOM Template Ref",
        )
    }


# MO Scheduled Products
class mrp_production_product_line(osv.osv):
    _inherit = "mrp.production.product.line"

    def _get_product_line(self, cr, uid, ids, context=None):
        """ return all product_line for the same updated product """
        product_line_ids = []
        for product in self.browse(cr, uid, ids, context=context):
            product_line_ids += self.pool.get("mrp.production.product.line").search(cr, uid, [("product_id", "=", product.id)], context=context)
        return product_line_ids

    def _get_machine_setup_params(self, cr, uid, ids, field_name, arg, context=None):
        setup_detail_obj = self.pool.get("mrp.machine.setup.master.line")
        res = {}
        for product_line in self.browse(cr, uid, ids, context=context):
            res[product_line.id] = {}
            # Default value
            masters = ["line_slipjoint", "line_secretjoint", "line_roofjoint", "line_board"]
            for master in masters:
                res[product_line.id].update({
                    "%s_pir" % master: False,
                    "%s_pu" % master: False,
                    "%s_pir_settime" % master: False,
                    "%s_pu_settime" % master: False,
                })
            product = product_line.product_id
            master_ids = setup_detail_obj.search(cr, uid, [("thickness", "=", product.T.id)])
            if master_ids:
                W = product.W or 0.0
                T = product.T.value or 0.0
                sets = setup_detail_obj.browse(cr, uid, master_ids)
                for set in sets:
                    if any([m in set.machine_id.name for m in masters]):
                        if product.bom_template_id == set.machine_id.bom_template_id and product.mat_insulation_choices.code.lower() in set.machine_id.name:
                            density = self._get_val(cr, uid, product_line.id, set.str_density, W, L, context=context)
                            settime = self._get_val(cr, uid, product_line.id, set.str_settime, W, L, context=context)
                            res[product_line.id].update({
                                set.machine_id.name: round(W * T * density * settime / 1000000, 2),
                                set.machine_id.name + "_settime": settime,
                            })
        return res

    def _compute_total_panel(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        ConfigLine = self.pool.get("pallet.config.line")
        for product_line in self.browse(cr, uid, ids, context=context):
            product = product_line.product_id
            config_line_ids = ConfigLine.search(cr, uid, [
                ("config_id.bom_template_id", "=", product.bom_template_id.id),
                ("config_id.is_international", "=", product.ref_order_id.is_international),
                ("thickness", "=", product.T.id),
            ], context=context, limit=1)
            config_lines = ConfigLine.browse(cr, uid, config_line_ids, context=context)
            res[product_line.id] = config_lines[0].total_panel if config_lines else False
        return res

    _columns = {
        "line_slipjoint_pir": fields.function(
            _get_machine_setup_params,
            string="Slip Joint (PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_slipjoint_pu": fields.function(
            _get_machine_setup_params,
            string="Slip Joint (PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_secretjoint_pir": fields.function(
            _get_machine_setup_params,
            string="Secret Joint (PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_secretjoint_pu": fields.function(
            _get_machine_setup_params,
            string="Secret Joint (PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_roofjoint_pir": fields.function(
            _get_machine_setup_params,
            string="Roof Joint (PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_roofjoint_pu": fields.function(
            _get_machine_setup_params,
            string="Roof Joint (PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_board_pir": fields.function(
            _get_machine_setup_params,
            string="Board (PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_board_pu": fields.function(
            _get_machine_setup_params,
            string="Board (PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_slipjoint_pir_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Slip Joint PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_slipjoint_pu_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Slip Joint PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_secretjoint_pir_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Secret Joint PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_secretjoint_pu_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Secret Joint PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_roofjoint_pir_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Roof Joint PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_roofjoint_pu_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Roof Joint PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_board_pir_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Board PIR)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "line_board_pu_settime": fields.function(
            _get_machine_setup_params,
            string="Set Time (Board PU)",
            type="float",
            multi="all",
            store={
                "mrp.production.product.line": (lambda self, cr, uid, ids, c={}: ids, None, 10),
                "product.product": (_get_product_line, ["W", "L", "T", "bom_product_type", "cut_area", "remark"], 10),
            }
        ),
        "total_panel": fields.function(
            _compute_total_panel,
            type="integer",
            string="Full Panel Per Stack",
        ),
    }

    def hide_field(self, cr, uid, node, view_type, context=None):
        modifiers = eval(node.get("modifiers", "{}").replace("true", "True").replace("false", "False"))
        if view_type == "tree":
            modifiers["tree_invisible"] = True
        if view_type == "form":
            modifiers["invisible"] = True
        modifiers = str(modifiers).replace("'", '"').replace("True", "true").replace("False", "false")
        node.set("invisible", "1")
        node.set("modifiers", modifiers)

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = super(mrp_production_product_line, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if context is None:
            context = {}
        if "is_continuous_line" in context:
            Master = self.pool.get("mrp.machine.setup.master")
            # Find all machine setup master
            all_master_ids = Master.search(cr, uid, [], context=context)
            all_masters = Master.browse(cr, uid, all_master_ids, context=context)
            all_master_names = [m.name for m in all_masters]
            # Find some machine setup master which match with continuous line
            master_ids = Master.search(cr, uid, [("is_continuous_line", "=", context["is_continuous_line"])], context=context)
            masters = Master.browse(cr, uid, master_ids, context=context)
            master_names = [m.name for m in masters]
            # --
            doc = etree.XML(res["arch"])
            for node in doc.iter():
                field_name = node.attrib.get("name")
                # Continue for loop when not found attribute name
                if not field_name:
                    continue
                # Hide some field
                hide_field_for_continuous_line = ["cut_area"]
                if context["is_continuous_line"] and field_name in hide_field_for_continuous_line:
                    self.hide_field(cr, uid, node, view_type, context=context)
                hide_field_for_not_continuous_line = []
                if not context["is_continuous_line"] and field_name in hide_field_for_not_continuous_line:
                    self.hide_field(cr, uid, node, view_type, context=context)
                # Continue for loop when field name not match with master name
                if not any([m in field_name for m in all_master_names]):
                    continue
                # Hide field (Condition by 'continueous line')
                if not any([m in field_name for m in master_names]):
                    self.hide_field(cr, uid, node, view_type, context=context)
            res["arch"] = etree.tostring(doc)
        return res
