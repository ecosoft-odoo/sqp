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
    'name' : 'FIX Invoice Due Date',
    'version' : '1.0',
    'author' : 'Kitti U.',
    'summary': 'if Due Date exists, do not overwrite with Payment Term',
    'description': """

In Supplier Invoice, according to existing logic,
* When Validate, system will always use Payment Term + Invoice Date = Due Date
* No matter what is specified on screen, account_move_line's due date (date_maturity) will be calculated from Payment Term

We want to change it such that,
* If user already assign Due Date, just use it and do not recalc.
* Always and Always use Due Date on screen to set the account_move_line's due date (date_maturity)

    """,
    'category': 'Accounting & Finance',
    'sequence': 4,
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['account'],
    'demo' : [],
    'data' : [
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
