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
    'name': "Sales Commission Calculations Extension for SQP",
    'author': 'Ecosoft',
    'summary': '',
    'description': """

Release Commission only when payment reach "Final Amount" in Sales Order
------------------------------------------------------------------------

New field "Final Amount" in Sales Order, will be used as trigger that, the SO give the green light for commission.

""",
    'category': 'Sales',
    'sequence': 20,
    'website': 'http://www.ecosoft.co.th',
    'images': [],
    'depends': ['sale',
                'sale_commission_calc',
                'sale_commission_calc_extension'],
    'demo': [
    ],
    'data': [
          'sale_view.xml',
          'commission_rule_view.xml',
          'commission_calc_view.xml',
    ],
    'test': [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
