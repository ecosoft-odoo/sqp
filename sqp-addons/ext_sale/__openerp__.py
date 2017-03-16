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
    'name' : "Extensions for Sales Module",
    'author' : 'Kitti U.',
    'summary': '',
    'description': """
Features
========

* Adding new version field in Sales Order
* When print Quotation / Sales Order --> create attachment with version number
* 4 Document Sequence,
* * Quotation / Quotation International (QD/QI)
* * Sales Order / Sales Order International (SD/SI)
* Number of Sets (X Units)
* New Project Reference field
* New Additional Discount Amt to be used to calculate %
* If SO mark as International, only list product marked as international.

* ***For SO for Standard AHU products only***, although it is make to order, do not generate MO from SO. It will be generated manually later on.

""",
    'category': 'Sales',
    'sequence': 8,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['document',
                 'sale',
                 'advance_and_additional_discount','product_tag'],
    'demo' : [],
    'data' : [
        'sale_report.xml',
        'sale_view.xml',
        'product_view.xml',
        #'sale_sequence.xml',
        'data/ir.values.csv',
        
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
