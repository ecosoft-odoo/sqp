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

import netsvc
from osv import osv, fields
from tools.translate import _


class product_template(osv.osv):
    
    _inherit = "product.template"
    _columns = {
        # Do not translate
        'name': fields.char('Name', size=256, required=True, translate=False, select=True),
    }    
    
product_template()

class product_product(osv.osv):
    
    _inherit = "product.product"
    
    def _get_search_key(self, cr, uid, ids, name, args, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            res[product.id] = '%0*d' % (6, product.id)
        return res

    _columns = {
        # Do not translate
        'name_template': fields.related('product_tmpl_id', 'name', string="Template Name", type='char', size=256, store=True, select=True),
        'search_key': fields.function(_get_search_key, method=True, type='char', string='Search Key', store=True),
    }

product_product()


class product_category(osv.osv):
    
    _inherit = "product.category"
    
    def _get_search_key(self, cr, uid, ids, name, args, context=None):
        res = {}
        for categ in self.browse(cr, uid, ids, context=context):
            res[categ.id] = '%0*d' % (6, categ.id)
        return res

    _columns = {
        'search_key': fields.function(_get_search_key, method=True, type='char', string='Search Key', store=True),
    }

product_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
