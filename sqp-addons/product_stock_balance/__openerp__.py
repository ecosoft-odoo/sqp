# -*- coding: utf-8 -*-
{
    'name': 'SQP :: Product Stock Balance',
    'version': '7.0.1.0.0',
    'author': 'Tharathip C.',
    'summary': 'Stock Balance Report',
    'description': """
    """,
    'category': 'Warehouse',
    'website': 'http://www.ecosoft.co.th',
    'images': [],
    'depends': [
        'stock',
        'account',
    ],
    'demo': [],
    'data': [
        'wizards/product_stock_balance_wizard.xml',
        'views/product_stock_balance_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [],
    'auto_install': False,
    'application': False,
    'installable': True,
}
