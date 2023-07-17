# -*- coding: utf-8 -*-
# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import xlwt
import logging
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import _render

_logger = logging.getLogger(__name__)


class sqp_sampling_in_process_continuous_xls_parser(report_sxw.rml_parse):

    def _get_wanted_list(self):
        wanted_list = [
            "item", "panel_code", "panel_size", "color", "surface", "qty_pcs", "qty_sampling", "date",
            "mark", "edge", "plate", "width", "length", "thick", "checker", "remark",
        ]
        return wanted_list

    def __init__(self, cr, uid, name, context):
        super(sqp_sampling_in_process_continuous_xls_parser, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            "wanted_list": self._get_wanted_list(),
        })


class sqp_sampling_in_process_continuous_xls(report_xls):

    def __init__(self, name, table, rml=False, parser=False, header=True,
                 store=False):
        super(sqp_sampling_in_process_continuous_xls, self).__init__(
            name, table, rml, parser, header, store)

        self.col_specs_lines_template = {
            "item": {
                "header": [1, 20, "text", "Item"],
                "lines": [1, 0, "number", _render("item")],
            },
            "panel_code": {
                "header": [1, 20, "text", "Panel Code"],
                "lines": [1, 0, "text", _render("panel_code")],
            },
            "panel_size": {
                "header": [1, 20, "text", "PANEL SIZE\nW x L x T"],
                "lines": [1, 0, "text", _render("panel_size")],
            },
            "color": {
                "header": [1, 20, "text", "COLOR\n(UPPER/LOWER)"],
                "lines": [1, 0, "text", _render("color")],
            },
            "surface": {
                "header": [1, 20, "text", "SURFACE\n(UPPER/LOWER)"],
                "lines": [1, 0, "text", _render("surface")],
            },
            "qty_pcs": {
                "header": [1, 15, "text", "QTY\npcs"],
                "lines": [1, 0, "number", _render("qty_pcs")],
            },
            "qty_sampling": {
                "header": [1, 15, "text", "QTY\nsampling"],
                "lines": [1, 0, "text", ""],
            },
            "date": {
                "header": [1, 15, "text", "Date"],
                "lines": [1, 0, "text", ""],
            },
            "mark": {
                "header": [1, 15, "text", "รอย"],
                "lines": [1, 0, "text", ""],
            },
            "edge": {
                "header": [1, 15, "text", "สภาพขอบ"],
                "lines": [1, 0, "text", ""],
            },
            "plate": {
                "header": [1, 15, "text", "สภาพแผ่น"],
                "lines": [1, 0, "text", ""],
            },
            "width": {
                "header": [1, 15, "text", "กว้าง"],
                "lines": [1, 0, "text", ""],
            },
            "length": {
                "header": [1, 15, "text", "ยาว"],
                "lines": [1, 0, "text", ""],
            },
            "thick": {
                "header": [1, 15, "text", "หนา"],
                "lines": [1, 0, "text", ""],
            },
            "checker": {
                "header": [1, 20, "text", "ผู้สุ่มตรวจ"],
                "lines": [1, 0, "text", ""],
            },
            "remark": {
                "header": [1, 20, "text", "Remark"],
                "lines": [1, 0, "text", ""],
            },
        }

    def _write_header(self, o, ws, _p, row_pos, _xs):
        # Logo
        parent_path = os.path.dirname(os.path.abspath(__file__))
        ws.insert_bitmap("{}/sqp_small_logo.bmp".format(parent_path), 0, 0, scale_x=0.4, scale_y=0.27)
        # Company Name
        cell_format = "font: height 350;align: vert center;"
        left_top_border_format = "borders: left_color black, top_color black, left thin, top thin;"
        right_top_border_format = "borders: right_color black, top_color black, right thin, top thin;"
        left_bottom_border_format = "borders: left_color black, bottom_color black, left thin, bottom thin;"
        right_bottom_border_format = "borders: right_color black, bottom_color black, right thin, bottom thin;"
        left_right_bottom_border_format = "borders: left_color black, right_color black, bottom_color black, left thin, right thin, bottom thin;"
        bottom_border_format = "borders: bottom_color black, bottom thin;"
        c_specs = [
            ("header_1", 1, 0, "text", "", None, xlwt.easyxf(cell_format + left_top_border_format)),
            ("header_2", 12, 0, "text", "บริษัท สแควร์ พาแนล ซิสเต็ม จำกัด", None, xlwt.easyxf(cell_format + right_top_border_format)),
            ("header_3", 3, 0, "text", "CO-F-02 Rev.0", None, xlwt.easyxf(cell_format + right_top_border_format)),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("header_1", 1, 0, "text", "", None, xlwt.easyxf(cell_format + left_bottom_border_format)),
            ("header_2", 12, 0, "text", "Square Panel System Co., Ltd.", None, xlwt.easyxf(cell_format + right_bottom_border_format)),
            ("header_3", 3, 0, "text", "วันที่บังคับใช้: 22/06/66", None, xlwt.easyxf(cell_format + right_bottom_border_format)),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        # Title
        c_specs = [
            ("header_1", 16, 0, "text", "ใบสุ่มตรวจ (Sampling in Process)", None, xlwt.easyxf(cell_format + _xs["center"] + left_right_bottom_border_format)),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        cell_format = "font: height 240;align: vert center;"
        c_specs = [
            ("header_1", 3, 0, "text", "หน่วยงาน: Continuous Line", None, xlwt.easyxf(cell_format + left_bottom_border_format)),
            ("header_2", 5, 0, "text", "ชื่อลูกค้า: {}".format(((o.order_id and o.order_id.partner_id.name or "") or (o.tmp_partner_id and o.tmp_partner_id.name or "") or "").encode("UTF-8")), None, xlwt.easyxf(cell_format + bottom_border_format)),
            ("header_3", 4, 0, "text", "ORDER NO: {}".format((o.order_id and o.order_id.name or "") or o.tmp_ref_order or ""), None, xlwt.easyxf(cell_format + bottom_border_format)),
            ("header_4", 4, 0, "text", "PROJECT: {}".format(((o.order_id and o.order_id.ref_project_name or "") or (o.product_id and o.product_id.name or "") or "").encode("UTF-8")), None, xlwt.easyxf(cell_format + right_bottom_border_format)),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        # Column Headers
        head_col_style = xlwt.easyxf("font: bold true, height 200;align: vert center, horz center;borders: left_color black, top_color black, right_color black, bottom_color black, left thin, top thin, right thin, bottom thin;")
        c_specs = map(lambda x: self.render(
            x, self.col_specs_lines_template, "header"), _p.wanted_list)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=head_col_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)
        # Height Row
        for i in range(5):
            ws.row(i).height = 600
        return row_pos

    def _write_lines(self, o, ws, _p, row_pos, _xs):
        detail_col_style = xlwt.easyxf("align: horz center;font: height 200;borders: left_color black, top_color black, right_color black, bottom_color black, left thin, top thin, right thin, bottom thin;")
        item = 0
        panel_code = ""
        panel_size = ""
        color = ""
        surface = ""
        qty_pcs = ""
        for line in o.product_lines:
            item += 1
            # Panel code
            product_name = line.product_id.name
            if product_name:
                panel_code = product_name
                if "|" in product_name and product_name.rindex("|") > 0:
                    panel_code = product_name[:product_name.rindex("|")]
            # Panel size
            W = str(int(line.W)) if line.W == int(line.W) else "{:,.2f}".format(line.W)
            L = str(int(line.L)) if line.L == int(line.L) else "{:,.2f}".format(line.L)
            T = str(int(line.T)) if line.T == int(line.T) else "{:,.2f}".format(line.T)
            panel_size = "{} x {} x {}".format(W, L, T)
            color = "{}/{}".format(line.product_id.mat_inside_skin_choices.code or "", line.product_id.mat_outside_skin_choices.code or "")
            surface = "{}/{}".format(line.product_id.mat_in_surface_choices.name or "", line.product_id.mat_out_surface_choices.name or "")
            qty_pcs = str(int(line.product_qty)) if line.product_qty == int(line.product_qty) else "{:,.2f}".format(line.product_qty)
            _logger.info("item => {}, panel code => {}, panel size => {}, color => {}, surface => {}, qty(pcs) => {}".format(
                item, panel_code, panel_size, color, surface, qty_pcs))
            c_specs = map(lambda x: self.render(
                x, self.col_specs_lines_template, "lines"), _p.wanted_list)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=detail_col_style)
        return row_pos

    def _write_footer(self, o, ws, _p, row_pos, _xs):
        cell_format = "font: height 200;"
        left_border_style = xlwt.easyxf(cell_format + "borders: left_color black, left thin;")
        right_border_style = xlwt.easyxf(cell_format + "borders: right_color black, right thin;")
        bottom_border_style = xlwt.easyxf(cell_format + "borders: bottom_color black, bottom thin;")
        left_bottom_border_style = xlwt.easyxf(cell_format + "borders: left_color black, bottom_color black, left thin, bottom thin;")
        right_bottom_border_style = xlwt.easyxf(cell_format + "borders: right_color black, bottom_color black, right thin, bottom thin;")
        c_specs = [
            ("footer_1", 1, 0, "text", "", None, left_border_style),
            ("footer_2", 1, 0, "text", ""),
            ("footer_3", 1, 0, "text", ""),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", ""),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", ""),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "หมายเหตุ 1", None, left_border_style),
            ("footer_2", 1, 0, "text", ""),
            ("footer_3", 1, 0, "text", "รอย = รอยขีดข่วน รอยเปื้อนน้ำยาโฟม"),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", "สภาพขอบ = การรีดJoint การพับJoint หรือลอนหลังคา สภาพ Sidetape"),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", "สภาพแผ่น = แผ่นเยื้อง การซอยแผ่น"),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "หมายเหตุ 2", None, left_border_style),
            ("footer_2", 1, 0, "text", ""),
            ("footer_3", 1, 0, "text", "P = ผ่าน"),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", "F = ไม่ผ่าน"),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", ""),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "หมายเหตุ 3", None, left_border_style),
            ("footer_2", 1, 0, "text", ""),
            ("footer_3", 1, 0, "text", "ตรวจทุกแผ่นแรกของแต่ละ Item ตามเกณฑ์ A"),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", "หาก Item ไหนมีความยาวรวมเกิน 500 m ให้ตรวจตามเกณฑ์ A ซ้ำทุก 500 m"),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", ""),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "", None, left_border_style),
            ("footer_2", 1, 0, "text", ""),
            ("footer_3", 1, 0, "text", ""),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", ""),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", ""),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "", None, left_border_style),
            ("footer_2", 1, 0, "text", "*เมื่อพบชิ้นงานไม่ได้คุณภาพให้ทำการแจ้งQC"),
            ("footer_3", 1, 0, "text", ""),
            ("footer_4", 1, 0, "text", ""),
            ("footer_5", 1, 0, "text", ""),
            ("footer_6", 1, 0, "text", ""),
            ("footer_7", 1, 0, "text", ""),
            ("footer_8", 1, 0, "text", ""),
            ("footer_9", 1, 0, "text", ""),
            ("footer_10", 1, 0, "text", ""),
            ("footer_11", 1, 0, "text", ""),
            ("footer_12", 1, 0, "text", ""),
            ("footer_13", 1, 0, "text", ""),
            ("footer_14", 1, 0, "text", ""),
            ("footer_15", 1, 0, "text", ""),
            ("footer_16", 1, 0, "text", "", None, right_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        c_specs = [
            ("footer_1", 1, 0, "text", "", None, left_bottom_border_style),
            ("footer_2", 1, 0, "text", "", None, bottom_border_style),
            ("footer_3", 1, 0, "text", "", None, bottom_border_style),
            ("footer_4", 1, 0, "text", "", None, bottom_border_style),
            ("footer_5", 1, 0, "text", "", None, bottom_border_style),
            ("footer_6", 1, 0, "text", "", None, bottom_border_style),
            ("footer_7", 1, 0, "text", "", None, bottom_border_style),
            ("footer_8", 1, 0, "text", "", None, bottom_border_style),
            ("footer_9", 1, 0, "text", "", None, bottom_border_style),
            ("footer_10", 1, 0, "text", "", None, bottom_border_style),
            ("footer_11", 1, 0, "text", "", None, bottom_border_style),
            ("footer_12", 1, 0, "text", "", None, bottom_border_style),
            ("footer_13", 1, 0, "text", "", None, bottom_border_style),
            ("footer_14", 1, 0, "text", "", None, bottom_border_style),
            ("footer_15", 1, 0, "text", "", None, bottom_border_style),
            ("footer_16", 1, 0, "text", "", None, right_bottom_border_style),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data)
        return row_pos

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        for o in objects:
            sheet_name = o.name.replace("/", "_")
            ws = wb.add_sheet(sheet_name)
            ws.panes_frozen = True
            ws.remove_splits = True
            ws.portrait = 0  # Landscape
            ws.fit_width_to_pages = 1
            row_pos = 0

            # Set print header/footer
            ws.header_str = self.xls_headers["standard"]
            ws.footer_str = self.xls_footers["standard"]

            # Data
            row_pos = self._write_header(o, ws, _p, row_pos, _xs)
            row_pos = self._write_lines(o, ws, _p, row_pos, _xs)
            row_pos = self._write_footer(o, ws, _p, row_pos, _xs)


sqp_sampling_in_process_continuous_xls(
    "report.sqp_sampling_in_process_continuous.xls",
    "mrp.production",
    parser=sqp_sampling_in_process_continuous_xls_parser)
