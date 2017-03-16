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
    'name': 'Configuration for SQP',
    'version': '1.0',
    'category': 'Hidden',
    'description': '',
    'author': 'Ecosoft',
    'website': 'http://www.ecosoft.co.th/',
    'depends': [#'account','product_tag'
                ],
     'data': [
#         # Configuration, i.e., users, companies, etc.
#         'data/res.company.csv', # Company Info
#         'data/res.lang.csv', # Language Info
#         'data/account_data.xml', # Payment Term
#         'data/product_data.xml', # Product Category, Product Tags
#         'data/product.uom.csv', # UOMs
#         'data/ir.values.csv', # Default Values in SO form.
#         'data/mrp_data.xml', # Machine Setup Config
#         'data/res.partner.category.csv', # Machine Setup Config
#         #'master/sales_person_user_data.xml',
#         'data/ir_sequence.xml',
#         # AHU Price List
#         'master/product/ahu_with_3pricelist/product.pricelist.csv', # Price list version
#         'master/product/ahu_with_3pricelist/product.pricelist.version.csv', # Price list version  
#         'master/product/ahu_with_3pricelist/product.product.csv',
#         'master/product/ahu_with_3pricelist/product.pricelist.item.csv',        
        ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
