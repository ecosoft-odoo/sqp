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
    'name' : "Product Tags",
    'author' : 'Kitti U.',
    'summary': '',
    'description': """
    
New Product Tags as many2many relationship with Product.
* Product Tag on Sales Order page, ensure that product listed by selected tag.
* Customer Product on Product, if specified, this product listed for only this customer.
* One-Time Use checkbox on Product. Product created from BOM Template will be marked as One-Time Use.

""",
    'category': 'Sales',
    'sequence': 8,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['base','product','sale','sale_stock','web_m2o_enhanced'],
    'demo' : [],
    'data' : [
        'sale_view.xml',
        'product_view.xml',
        'security/ir.model.access.csv'
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
