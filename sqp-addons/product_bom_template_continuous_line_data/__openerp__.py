# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name" : "BOM Template For Continuous Line (Data)",
    "version" : "7.0.1.0.0",
    "author" : "Tharathip C.",
    "category": "Warehouse",
    "sequence": 4,
    "website" : "http://www.ecosoft.co.th",
    "depends" : [
        "tmp_product_bom_template",
    ],
    "data" : [
        "data/bom.choice.skin.csv",
        "data/bom.choice.width.csv",
        "data/bom.choice.surface.csv",
        "data/product.product.csv",
        "data/mrp.bom.csv",
        "data/00_slipjoint/mrp.bom.csv",
        "data/01_secretjoint/mrp.bom.csv",
        "data/02_roofjoint/mrp.bom.csv",
        "data/03_board/mrp.bom.csv",
        "data/mrp.machine.setup.master.csv",
        "data/mrp.machine.setup.master.line.csv",
        "data/pallet.config.csv",
        "data/pallet.config.line.csv",
    ],
    "auto_install": False,
    "application": True,
    "installable": True,
}
