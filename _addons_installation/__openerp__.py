# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 Gábor Dukai
#    Modified by Almacom (Thailand) Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "SQP Addons Installation",
    "version" : "1.0",
    "author" : "kittiu",
    "website" : "http://ecosoft.co.th",
    "description": """
Install all requried modules
""",
    "depends" : [               
                # ecosoft-addons
                'account_billing','account_thai_wht','account_debitnote',
                'advance_and_additional_discount','create_invoice_line_percentage',
                'doc_nodelete','line_sequence','mrp_sale_rel','payment_register',
                'product_flexible_search','product_pricelist_last_invoice',
                'product_uom_bycategory','purchase_requisition_double_validation',
                'report_menu_restriction','security_enhanced','split_quotation_ab',
                'stock_simplified_move','hide_print_button',
                # revised-addons
                'account_refund_original','jasper_reports','picking_invoice_rel',
                'web_m2o_enhanced','web_export_view',
                # sqp-addons
                'ac_report_font_thai','ext_account_voucher','ext_mrp','ext_product',
                'ext_purchase','ext_sale','fix_account_validate','fix_stock','jrxml_reports',
                'mrp_production_status','product_bom_template','product_tag','purchase_subcontract',
                'stock_supply_list'
                ],
                 
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

