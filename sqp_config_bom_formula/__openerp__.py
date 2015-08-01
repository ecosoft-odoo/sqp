# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Configuration - BOM Formulas',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
    """,
    'author': 'Ecosoft',
    'website': 'http://www.ecosoft.co.th/',
    'depends': [
        'mrp',
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
