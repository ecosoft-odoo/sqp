# -*- coding: utf-8 -*-
{
    'name': 'Configuration - BOM Formulas',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
    """,
    'author': 'Ecosoft',
    'website': 'http://www.ecosoft.co.th/',
    'depends': [
        'mrp', 'product_bom_template'
                ],
    'data': [
        'product.product.csv',
        'mrp.bom.csv',
        '00_slipjoint_ahu/mrp.bom.csv',
        '01_slipjoint_cr_ahu/mrp.bom.csv',
        '02_slipjoint_std_ahu/mrp.bom.csv',
        '03_slipjoint_rockwool/mrp.bom.csv',
        '04_firejoint_rockwool/mrp.bom.csv',
        '05_nonprogressive_joint/mrp.bom.csv',
        '06_foamslab/mrp.bom.csv',
        '07_single_door_flat/mrp.bom.csv',
        '08_double_door_unseq/mrp.bom.csv',
        '09_double_door_seq/mrp.bom.csv',
        '10_single_sliding_door/mrp.bom.csv',
        '11_swing_door_cold/mrp.bom.csv',
        '12_single_door_cold/mrp.bom.csv',
        '13_window/mrp.bom.csv',
        '14_sinko_ab/mrp.bom.csv',
            ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
