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
    'name': 'BOI (SQP)',
    'version': '1.0',
    'author': 'Ecosoft',
    'summary': 'BOI (SQP)',
    'description': """""",
    'category': 'BOI',
    'website': 'http://www.ecosoft.co.th',
    'images': [],
    'depends': [
        'account_debitnote',
        'create_invoice_line_percentage',
        'ext_purchase',
        'product_tag',
        'product_bom_template',
        'ext_mrp',
        'bom_move',
        'ext_sale',
        'split_quotation_ab',
    ],
    'demo': [],
    'data': [
        'view/boi_view.xml',
        'view/sale_view.xml',
        'view/account_invoice_view.xml',
        'view/stock_view.xml',
        'view/purchase_requisition_view.xml',
        'view/purchase_view.xml',
        'view/product_view.xml',
        'view/product_rapid_create_view.xml',
        'report/boi_report_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
