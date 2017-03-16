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
from osv import osv, fields

class mrp_production(osv.osv):
    
    _inherit = 'mrp.production'

    _columns = {
        'tmp_partner_id': fields.many2one('res.partner', 'Customer (temp)', required=False, help='Only used for old MO without SO in new system'),
        'tmp_ref_order': fields.char('Sales Order (temp)', size=64, required=False, help='Only used for old MO without SO in new system'),
    }    
    
    def action_confirm(self, cr, uid, ids, context=None):
        # For case, no order_id and no target_picking_idbut user type in SO number manually
        for production in self.browse(cr, uid, ids):
            picking_id = False
            if not production.order_id and not production.target_picking_id \
                    and production.tmp_ref_order:
                picking_id = self._create_picking(cr, uid, production, production.product_lines, None, context=context)
            if picking_id:
                self.write(cr, uid, [production.id], {'target_picking_id': picking_id})                     
        res = super(mrp_production, self).action_confirm(cr, uid, ids, context=context)
        return res 
    
    # Assign partner_id
    def _prepare_production_picking(self, cr, uid, production, context=None):
        res = super(mrp_production, self)._prepare_production_picking(cr, uid, production, context=context)
        if not res.get('partner_id', False):
            res['partner_id'] = production.tmp_partner_id and production.tmp_partner_id.id or False
        return res    
    
    # Assign partner_id and location
    def _prepare_production_line_move(self, cr, uid, production, line, picking_id, date_planned, context=None):
        res = super(mrp_production, self)._prepare_production_line_move(cr, uid, production, line, picking_id, date_planned, context=context)
        default_shop = self.pool.get('sale.shop').browse(cr, uid, 1) # Default to Square Panel shop
        if not res.get('location_id', False):
            res['location_id'] = default_shop and default_shop.warehouse_id.lot_stock_id.id or False
        if not res.get('location_dest_id', False):
            res['location_dest_id'] = default_shop and default_shop.warehouse_id.lot_output_id.id or False
        if not res.get('partner_id', False):
            res['partner_id'] = production.tmp_partner_id and production.tmp_partner_id.id or False
        return res
        
mrp_production()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
