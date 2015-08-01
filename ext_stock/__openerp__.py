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
    'name' : "Extensions for Stock Module (SQP)",
    'author' : 'Ecosoft',
    'summary': '',
    'description': """
Features
========

* Adding new "Purchase Order Ref." in Simplified Internal Move Line window. 
* Adding new "Sales Order Ref." in header.
* If schedule date is updated by user, make sure it will change all the move line's schedule date.
* Simplified Internal Move, do not show recorded auto generated from MO.

""",
    'category': 'Stock',
    'sequence': 8,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['stock','stock_simplified_move','sale_stock','hr','web_m2o_enhanced'],
    'demo' : [],
    'data' : [
               'stock_view.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
