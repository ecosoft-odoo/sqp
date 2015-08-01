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
import openerp.addons.decimal_precision as dp
from lxml import etree

class product_product(osv.osv):
    
    # Overwrite method
    def get_product_safety(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        location_obj = self.pool.get('stock.location')
        warehouse_obj = self.pool.get('stock.warehouse')
        shop_obj = self.pool.get('sale.shop')
        
        states = context.get('states',[])
        what = context.get('what',())
        if not ids:
            ids = self.search(cr, uid, [])
        res = {}.fromkeys(ids, 0.0)
        if not ids:
            return res

        if context.get('shop', False):
            warehouse_id = shop_obj.read(cr, uid, int(context['shop']), ['warehouse_id'])['warehouse_id'][0]
            if warehouse_id:
                context['warehouse'] = warehouse_id

        if context.get('warehouse', False):
            lot_id = warehouse_obj.read(cr, uid, int(context['warehouse']), ['lot_stock_id'])['lot_stock_id'][0]
            if lot_id:
                context['location'] = lot_id

        if context.get('location', False):
            if type(context['location']) == type(1):
                location_ids = [context['location']]
            elif type(context['location']) in (type(''), type(u'')):
                location_ids = location_obj.search(cr, uid, [('name','ilike',context['location'])], context=context)
            else:
                location_ids = context['location']
        else:
            location_ids = []
            wids = warehouse_obj.search(cr, uid, [], context=context)
            if not wids:
                return res
            for w in warehouse_obj.browse(cr, uid, wids, context=context):
                location_ids.append(w.lot_stock_id.id)

        # build the list of ids of children of the location given by id
        if context.get('compute_child',True):
            child_location_ids = location_obj.search(cr, uid, [('location_id', 'child_of', location_ids)])
            location_ids = child_location_ids or location_ids
        
        # this will be a dictionary of the product UoM by product id
        product2uom = {}
        uom_ids = []
        for product in self.read(cr, uid, ids, ['uom_id'], context=context):
            product2uom[product['id']] = product['uom_id'][0]
            uom_ids.append(product['uom_id'][0])
        # this will be a dictionary of the UoM resources we need for conversion purposes, by UoM id
        uoms_o = {}
        for uom in self.pool.get('product.uom').browse(cr, uid, uom_ids, context=context):
            uoms_o[uom.id] = uom

        results_safety = []
        results_in = []
        results_out = []
        results_mo_resv = []

        from_date = context.get('from_date',False)
        to_date = context.get('to_date',False)
        date_str = False
        date_values = False
        where = [tuple(location_ids),tuple(location_ids),tuple(ids),tuple(states)]
        if from_date and to_date:
            date_str = "date>=%s and date<=%s"
            where.append(tuple([from_date]))
            where.append(tuple([to_date]))
        elif from_date:
            date_str = "date>=%s"
            date_values = [from_date]
        elif to_date:
            date_str = "date<=%s"
            date_values = [to_date]
        if date_values:
            where.append(tuple(date_values))

        prodlot_id = context.get('prodlot_id', False)
        prodlot_clause = ''
        if prodlot_id:
            prodlot_clause = ' and prodlot_id = %s '
            where += [prodlot_id]
            
        # Calculate Safety
        if 'safety' in what:
            cr.execute(
                'select sum(product_min_qty), product_id, product_uom '\
                'from stock_warehouse_orderpoint '\
                'where location_id IN %s '\
                'and product_id IN %s '\
                'and active = True '\
                'group by product_id, product_uom ', tuple([tuple(location_ids), tuple(ids)]))
            results_safety = cr.fetchall()
        if 'in' in what:
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id NOT IN %s '\
                'and location_dest_id IN %s '\
                'and product_id IN %s '\
                "and state in %s " + (date_str and "and "+date_str+" " or '') + " "\
                + prodlot_clause + 
                'group by product_id,product_uom',tuple(where))
            results_in = cr.fetchall()
        if 'out' in what:
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id IN %s '\
                'and location_dest_id NOT IN %s '\
                'and product_id  IN %s '\
                "and state in %s " + (date_str and "and "+date_str+" " or '') + " "\
                + prodlot_clause + 
                'group by product_id,product_uom',tuple(where))
            results_out = cr.fetchall()
        # Additional Column
        if 'mo_resv' in what:
            cr.execute(
                'select sum(sm.product_qty), sm.product_id, sm.product_uom from stock_move sm '\
                    'join mrp_production mrp on sm.picking_id = mrp.picking_id '\
                    "where sm.state not in ('cancel','done') "\
                    "and mrp.state = 'confirmed' "\
                    'and sm.product_id IN %s '\
                    'group by sm.product_id, sm.product_uom', tuple([tuple(ids),]))
            results_mo_resv = cr.fetchall()            
            
        # Get the missing UoM resources
        uom_obj = self.pool.get('product.uom')
        uoms = map(lambda x: x[2], results_safety) + map(lambda x: x[2], results_in) + \
                map(lambda x: x[2], results_out) + map(lambda x: x[2], results_mo_resv)
        if context.get('uom', False):
            uoms += [context['uom']]
        uoms = filter(lambda x: x not in uoms_o.keys(), uoms)
        if uoms:
            uoms = uom_obj.browse(cr, uid, list(set(uoms)), context=context)
            for o in uoms:
                uoms_o[o.id] = o
                
        #TOCHECK: before change uom of product, stock move line are in old uom.
        context.update({'raise-exception': False})
        # Count the safety quantities
        for amount, prod_id, prod_uom in results_safety:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                    uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] -= amount
        # Count the incoming quantities
        for amount, prod_id, prod_uom in results_in:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                     uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] += amount
        # Count the outgoing quantities
        for amount, prod_id, prod_uom in results_out:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                    uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] -= amount
        # Count the MO Out
        for amount, prod_id, prod_uom in results_mo_resv:
            amount = uom_obj._compute_qty_obj(cr, uid, uoms_o[prod_uom], amount,
                    uoms_o[context.get('uom', False) or product2uom[prod_id]], context=context)
            res[prod_id] -= amount
                          
        return res
    
    # Overwrite method
    def _product_safety(self, cr, uid, ids, field_names=None, arg=False, context=None):

        if not field_names:
            field_names = []
        if context is None:
            context = {}
        res = {}
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0.0)
        for f in field_names:
            c = context.copy()
            if f == 'qty_safety':
                c.update({ 'what': ('safety') })
            if f == 'qty_reorder':
                c.update({ 'states': ('confirmed','waiting','assigned','done'), 'what': ('in', 'out', 'safety', 'mo_resv') })
            # Additional Column
            if f == 'qty_mo_resv':
                c.update({ 'what': ('mo_resv') })
            # --
            safety_stock = self.get_product_safety(cr, uid, ids, context=c)
            for id in ids:
                if f == 'qty_safety':
                    res[id][f] = -safety_stock.get(id, 0.0) # show safety in positive value
                else:
                    res[id][f] = safety_stock.get(id, 0.0)
        return res
    
    def _search_product_reorder(self, cr, uid, obj, name, args, context=None):
        for arg in args:
            # domain = qty_reorder < 0
            if arg[0] == 'qty_reorder' and arg[1] == '<' and arg[2] == 0:
                c = context.copy()
                c.update({ 'states': ('confirmed','waiting','assigned','done'), 'what': ('in', 'out', 'safety', 'mo_resv') })
                safety_stock = self.get_product_safety(cr, uid, ids=None, context=c)
                res = []        
                for id in safety_stock:
                    if safety_stock.get(id, 0.0) < 0.0:
                        res.append(id)
                return [('id', 'in', res)]
    
    _inherit = "product.product"
    _columns = {
        'qty_safety': fields.function(_product_safety, multi='qty_safety',
            type='float',  digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Safety Stock',
            help="Quantity of Orderpoint of each product in given location."),
        'qty_reorder': fields.function(_product_safety, multi='qty_safety',
            type='float', fnct_search=_search_product_reorder, digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Reorder',
            help="Quantity of suggested reorder based on Future - Safety"),
        # Additional column
        'qty_mo_resv': fields.function(_product_safety, multi='qty_safety',
            type='float',  digits_compute=dp.get_precision('Product Unit of Measure'),
            string='MO Out',
            help="Quantity of product to be reserved for production (regardless of location)"),                   
    }

product_product()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
