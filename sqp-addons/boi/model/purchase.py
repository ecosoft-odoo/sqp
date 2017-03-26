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

from openerp.osv import fields, osv

class purchase_order(osv.osv):

    _inherit = 'purchase.order'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict", domain="[('start_date','!=',False),('active','!=',False)]"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            sequence_obj = self.pool.get('ir.sequence')
            if vals.get('is_subcontract', False):
                vals['name'] = sequence_obj.get(cr, uid, 'purchase.order.subcontract') or '/'
            else:
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order') or '/'
            boi_type = (vals.get('boi_type','') == 'BOI') and 'BOI' or 'NONBOI'
            vals.update({'name': '%s-%s'%(boi_type, vals.get('name', '/'))})
        return super(purchase_order, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        order_id = super(purchase_order, self).copy(cr, uid, id, default=default, context=context)
        if order_id:
            order = self.browse(cr, uid, order_id, context=context)
            boi_type = order.boi_type == 'BOI' and 'BOI' or 'NONBOI'
            name = '%s-%s'%(boi_type,order.name)
            self.write(cr, uid, [order_id], {'name': name}, context=context)
        return order_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        boi_type = vals.get('boi_type', False)
        if boi_type:
            for order in self.browse(cr, uid, ids, context=context):
                vals['name'] = order.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(purchase_order, self).write(cr, uid, ids, vals, context=context)

    def action_picking_create(self, cr, uid, ids, context=None):
        picking_id = super(purchase_order, self).action_picking_create(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        if picking_id:
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            for order in self.browse(cr, uid, ids, context=context):
                name = '%s-%s'%(order.boi_type,picking.name)
                boi_type = order.boi_type
                boi_cert_id = order.boi_cert_id and order.boi_cert_id.id or False
                picking_obj.write(cr, uid, picking_id, {'boi_type': boi_type, 'boi_cert_id': boi_cert_id, 'name': name})
        return picking_id

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        warehouse_name = boi_type == 'BOI' and 'FC_RM_BOI' or 'OF_RM'
        warehouse_ids = warehouse_obj.search(cr, uid, [('name','=',warehouse_name)], context=context)
        warehouse_id = len(warehouse_ids) > 0 and warehouse_ids[0] or False
        return {'value': {'boi_cert_id': False, 'warehouse_id': warehouse_id}}

purchase_order()
