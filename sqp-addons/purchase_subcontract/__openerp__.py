# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Ecosoft Co., Ltd. (http://ecosoft.co.th).
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
    'name' : 'PO Sub Contractor (SQP)',
    'version' : '1.0',
    'author' : 'Ecosoft',
    'summary': 'PO Sub Contractor (SQP)',
    'description': """
This module reuse Purchase Order for PO Sub Contractor. Internally it is PO, marked as "Sub Contractor".
* There will be new menu "PO Sub Contractor" just to separate these PO from normal PO.
* New field "Copy SO Lines", which copy lines.
* A new Document Sequence will be applied.
    """,
    'category': 'Purchase Management',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['purchase'],
    'demo' : [],
    'data' : ['purchase_subcon_sequence.xml',
              'purchase_view.xml'
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
