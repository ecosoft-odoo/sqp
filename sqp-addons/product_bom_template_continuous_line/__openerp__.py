# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name" : "BOM Template For Continuous Line",
    "version" : "7.0.1.0.0",
    "author" : "Tharathip C.",
    "summary": "Create part based on BOM Template for continuous line",
    "category": "Warehouse",
    "sequence": 4,
    "website" : "http://www.ecosoft.co.th",
    "depends" : [
        "boi",
        "bom_move",
        "mrp_production_status",
        "product_bom_template",
        "report_xls",
    ],
    "data" : [
        "security/ir.model.access.csv",
        "wizards/product_make_bom_views.xml",
        "views/mrp_views.xml",
        "views/product_rapid_create_views.xml",
        "views/product_views.xml",
        "views/pallet_config_views.xml",
        "report/report_data.xml",
    ],
    "auto_install": False,
    "application": True,
    "installable": True,
}
