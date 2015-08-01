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
import time

import types
import netsvc
from osv import osv, fields
import openerp.addons.decimal_precision as dp

class sale_order(osv.osv):

    def _amount_untaxed_pset(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for order in self.browse(cr, uid, ids, context=context):
            amount = order.amount_untaxed / (order.number_of_set == 0 and 1 or order.number_of_set)
            res[order.id] = amount
        return res
    
    def _search_mrp_created(self, cr, uid, obj, name, args, domain=None, context=None):
        if not len(args):
            return []
        for arg in args:
            if arg[1] == '=':
                if not arg[2]:
                    ids = self.search(cr, uid,[('ref_mo_ids','=',False)], context=context)
                else:
                    ids = self.search(cr, uid,[('ref_mo_ids','<>',False)], context=context)
            else:
                return []
        return [('id', 'in', [id for id in ids])]
    
    def _mrp_created(self, cr, uid, ids, name, arg, context=None):
        res = dict.fromkeys(ids,False)
        for order in self.browse(cr, uid, ids, context=context):
            if order.ref_mo_ids:
                res[order.id] =True
        return res
    
    _inherit = "sale.order"
    _columns = {
        'header_msg': fields.html('Header Message', readonly=False),
        'doc_version': fields.integer('Version', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'ref_quote_no': fields.char('Ref Quotate Number', size=64, readonly=True),
        'number_of_set': fields.integer('Number of Sets', readonly=True, states={'draft': [('readonly', False)]}), 
        'amount_untaxed_pset': fields.function(_amount_untaxed_pset, digits_compute=dp.get_precision('Account'), string='Untaxed Amount/Set'),
        'ref_attention_name': fields.char('Attention', size=128, readonly=False),
        'ref_project_name': fields.char('Ref Project Name', size=128, readonly=False),
        'is_international': fields.boolean('International', change_default=True, help='This check book will have affect on Document Sequence Number'),
        'add_disc_amt_ex':fields.float('Additional Discount Amt (Ex)',digits=(4,2), readonly=True, states={'draft': [('readonly', False)]}),
        'note2': fields.text('Note'),
        'ref_mo_ids':fields.one2many('mrp.production', 'order_id', 'Reference MO', readonly=True),
        'mrp_created': fields.function(_mrp_created, string='MO Created', 
            type='boolean',fnct_search=_search_mrp_created, help="It indicates that sale order has at least one MO."),
        'tag_no': fields.text('TAG No.'),
    }
    _defaults = {
        'doc_version' : 1,
        'number_of_set' : 1,
    }
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'ref_quote_no': self.browse(cr, uid, ids[0]).name,
                                  'date_order': time.strftime("%Y-%m-%d")})
        order = self.browse(cr, uid, ids[0])
        if order.is_international:
            new_name = self.pool.get('ir.sequence').get(cr, uid, 'confirmed.sale.order.inter')
        else:
            new_name = self.pool.get('ir.sequence').get(cr, uid, 'confirmed.sale.order')
        self.write(cr, uid, ids, {'name': new_name})        
        super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default.update({'ref_mo_ids':[]})
        context.update({'is_copied': True})
        return super(sale_order, self).copy(cr, uid, id, default, context)

    def create(self, cr, uid, vals, context=None):
        # On creation, set number_of_set to 1. This will set number_of_set field visible.
        if not context.get('is_copied', False):
            vals.update({'number_of_set': 1})
        is_international = vals.get('is_international', False)
        if is_international:
            new_name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order.inter')
            vals['name'] = new_name
        return super(sale_order, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(sale_order, self).write(cr, uid, ids, vals, context=context)
        # if % = 0 and add_disc_amt_ex > 0, recalculate using add_disc_amt_ex
        if not isinstance(ids, types.ListType): # Make it a list
            ids = [ids]
        if not vals.get('add_disc') and vals.get('add_disc_amt_ex'):
            amount_untaxed = self.read(cr, uid, ids, ['amount_untaxed'])[0]['amount_untaxed']
            if amount_untaxed:
                add_disc = (vals.get('add_disc_amt_ex') / amount_untaxed) * 100
                vals['add_disc'] = add_disc
                res = super(sale_order, self).write(cr, uid, ids, vals, context=context)
        # else just set add_disc_amt_ex = add_disc_amt
        else:
            for id in ids:
                value = self.read(cr, uid, [id], ['add_disc_amt'])
                super(sale_order, self).write(cr, uid, [value[0]['id']], {'add_disc_amt_ex': value[0]['add_disc_amt']})
        return res
    
    def onchange_number_of_set(self, cr, uid, ids, number_of_set, context=None):
        if context is None:
            context = {}
        number_of_set = number_of_set < 1 and 1 or number_of_set
        self.recompute_order_lines(cr, uid, ids, number_of_set, context=context)
        return {'value': {'number_of_set': number_of_set}}   
    
    def recompute_order_lines(self, cr, uid, ids, number_of_set, context=None):
        if context is None:
            context = {}
#        res = {
#            'value': {'order_line': [] },
#        }
        if len(ids) > 0:
            line_pool = self.pool.get('sale.order.line')
            order = self.browse(cr, uid, ids[0], context=context)
            for line in order.order_line:
                line_pool.write(cr, uid, [line.id], {'product_uom_qty': line.product_uom_qty_pset * number_of_set,
                                                     'number_of_set': number_of_set })
        return True    
    
    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        res.update({'ref_order_id': order.id,
                    'ref_project_name': order.ref_project_name})
        return res
            
sale_order()

class sale_order_line(osv.osv):
    
    def _amount_line_per_set(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        number_of_set = 0
        for line in self.browse(cr, uid, ids, context=context):
            number_of_set = number_of_set == 0 and line.order_id.number_of_set or number_of_set
            price = line.price_subtotal / (number_of_set == 0 and 1 or number_of_set)
            res[line.id] = price
        return res
       
    _inherit = "sale.order.line"
    _columns = {
        'product_uom_qty_pset': fields.float('Quantity/Set', digits_compute= dp.get_precision('Product UoS'), required=True, readonly=True),
        'price_subtotal_pset': fields.function(_amount_line_per_set, string='Subtotal/Set', digits_compute= dp.get_precision('Account')),
    }
    _defaults = {
        'product_uom_qty_pset' : 1,
    }    
    def create(self, cr, uid, vals, context=None):
        order_obj = self.pool.get('sale.order')
        order = order_obj.browse(cr, uid, vals['order_id'])
        vals.update({'product_uom_qty_pset': vals['product_uom_qty'] / order.number_of_set})
        return super(sale_order_line, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if ids:
            number_of_set = vals.get('number_of_set', False) or \
                                self.pool.get('sale.order.line').browse(cr, uid, ids[0]).order_id.number_of_set or 1.0
            if vals.get('product_uom_qty_pset', False) and not vals.get('product_uom_qty', False):
                vals.update({'product_uom_qty': vals['product_uom_qty_pset'] * number_of_set})
            if vals.get('product_uom_qty', False) and not vals.get('product_uom_qty_pset', False):
                vals.update({'product_uom_qty_pset': vals['product_uom_qty'] / number_of_set})
        return super(sale_order_line, self).write(cr, uid, ids, vals, context=context)    
    
sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
