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
    'name' : "Temp Fix for MO with no SO ref",
    'author' : 'Ecosoft',
    'summary': '',
    'description': """

* As MO will be created without SO ref, no SO will be required to create ont-time product.
* User will have to manually key in SO ref (temp) and Customer (temp)
* For DO created after confirm MO, use the temp values

    
""",
    'category': 'Manufacturing',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['product_bom_template','mrp_sale_rel','ext_mrp'],
    'demo' : [],
    'data' : [
        'product_rapid_create_view.xml',
        'mrp_view.xml'
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
