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
    'name' : 'BOM Template',
    'version' : '1.0',
    'author' : 'Kitti U.',
    'summary': 'Create part based on BOM Template',
    'description': """
    
1) Create Product & BOM from BOM Template with Formula

* BOM to be able to use as BOM Template with flexible formula
* Create One-Time Product window for Panel/Door/Window, with Size and Choices as parameters
* Ability to create new Product & BOM from the above.

2) Calculate machine setup parameters for product created by Create One-Time Product window.

* Machine Setup Formula window
* For products created from One-Time Product window, also pass W/T/L parameters
* When Product is Created, calculate machine setup parameters for each product
    
    """,
    'category': 'Warehouse',
    'sequence': 4,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['web_m2o_enhanced','product','mrp','mrp_quick_bom','mrp_sale_rel'],
    'demo' : [],
    'data' : [
        'wizard/product_rapid_create_view.xml',
        'wizard/product_make_bom_view.xml',
        'product_view.xml',
        'mrp_view.xml',
        'sale_view.xml',
        'data/bom.choice.thick.csv',
        'data/bom.choice.model.csv',
        'data/bom.choice.joint.csv',
        'data/bom.choice.skin.csv',
        'data/bom.choice.insulation.csv',
        'data/bom.choice.camlock.csv',
        'data/bom.choice.window.csv',
        'security/ir.model.access.csv',
        'data/default_data.xml',
        #'bom_data/mrp.bom.csv',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
