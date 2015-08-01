#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################
#
# ChriCar Beteiligungs- und Beratungs- GmbH
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
# created 2009-09-19 23:51:03+02
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from openerp.osv import fields, osv
from openerp.tools.sql import drop_view_if_exists
import openerp.addons.decimal_precision as dp


class mrp_production(osv.osv):
    
    _inherit = "mrp.production"
    
    def _total_qty_returned(self, cursor, user, ids, name, arg, context=None):
        res = dict.fromkeys(ids, False)
        tot = 0.0
        for production in self.browse(cursor, user, ids, context=context):
            for line in production.mrp_product_location_ids:
                tot += line.qty_available
                res[production.id] = tot
        return res
    
    _columns = {
        'mrp_product_location_ids': fields.one2many('mrp.product.location', 'production_id', 'Product by Stock'),
        'total_qty_returned': fields.function(_total_qty_returned, string='Quantity FG (returned)', type='float')
    }
    
mrp_production()

class mrp_product_location(osv.osv):
    _name = "mrp.product.location"
    _description = "Available Stock By Location"
    _auto = False
    _table = "mrp_product_location"

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        """ Finds the incoming and outgoing quantity of product.
        @return: Dictionary of values
        """
        if not field_names:
            field_names = []
        if context is None:
            context = {}
        res = {}
        
        for product_loc in self.browse(cr, uid, ids):
            c = context.copy()
            c.update({ 'states': ('done',), 'what': ('in', 'out'), 'location': product_loc.location_id.id})
            stock = self.pool.get('product.product').get_product_available(cr, uid, [product_loc.product_id.id], context=c)
            res[product_loc.id] = stock.get(product_loc.product_id.id, 0.0)
        return res
    
    _columns = {
           'location_id': fields.many2one('stock.location', 'Location', select=True, required=True, readonly=True),
           'production_id': fields.many2one('mrp.production', 'MO', select=True, required=True, readonly=True),
           'product_id': fields.many2one('product.product', 'Product', select=True, required=True, readonly=True),
           'company_id': fields.many2one('res.company', 'Company', readonly=True),
           'qty_available': fields.function(_product_available, string='Available Qty',
                type='float',  digits_compute=dp.get_precision('Product Unit of Measure')),           
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'mrp_product_location')
        location_id = self.pool.get('ir.model.data').get_object_reference(cr, None, 'stock', 'stock_location_locations_virtual')[1]
        cr.execute("""create or replace view mrp_product_location
                as
            SELECT ROW_NUMBER() OVER (ORDER BY location_id, production_id, product_id DESC) AS id, *
            FROM (
            SELECT location_id, b.production_id, a.product_id, a.company_id FROM
                (SELECT
                 l.id AS location_id,product_id,
                 l.company_id
                FROM stock_location l,
                     stock_move i
                WHERE l.usage='internal'
                  AND i.location_dest_id = l.id
                  AND state != 'cancel'
                  AND i.company_id = l.company_id
                  AND l.active = True
                  AND l.location_id <> %s
                  AND l.chained_location_type = 'none'
                  and l.posx = -1
                UNION
                SELECT
                    l.id AS location_id ,product_id,
                l.company_id
                FROM stock_location l,
                     stock_move o
                WHERE l.usage='internal'
                  AND o.location_id = l.id
                  AND state != 'cancel'
                  AND o.company_id = l.company_id
                  AND l.active = True
                  AND l.location_id <> %s
                  AND l.chained_location_type = 'none'
                  and l.posx = -1
                  ) a
                JOIN 
                (select mrp.id production_id, bom.product_id
                from mrp_production mrp 
                join mrp_bom bom
            on mrp.bom_id is not null and mrp.parent_id is null
            and bom.bom_id = mrp.bom_id
                       and mrp.state in ('draft')
                order by mrp.id, bom.product_id) b
                        ON a.product_id = b.product_id) AS mrp_product_location
                        ORDER BY location_id, production_id, product_id DESC
            ;""" % (str(location_id), str(location_id)))

mrp_product_location()
