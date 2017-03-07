# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class res_company(osv.osv):

    _inherit = 'res.company'
    _columns = {
        'sale_percent_overhead': fields.float('Job Cost Overhead (%)'),
    }
