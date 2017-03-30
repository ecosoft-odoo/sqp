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
        order_id = super(purchase_order, self).create(cr, uid, vals, context=context)
        if order_id:
            order = self.browse(cr, uid, order_id, context=context)

            # Update name
            if order.boi_type == 'BOI':
                boi_cert_name = order.boi_cert_id and order.boi_cert_id.name or 'BOI'
                name = '%s-%s'%(boi_cert_name, order.name[order.name.find('-') + 1:])
                self.write(cr, uid, [order_id], {'name': name}, context=context)
        return order_id

    def write(self, cr, uid, ids, vals, context=None):
        boi_type = vals.get('boi_type', False)
        boi_cert_id = vals.get('boi_cert_id', False)
        if boi_type or boi_cert_id:
            cert_obj = self.pool.get('boi.certificate')

            cert = cert_obj.browse(cr, uid, boi_cert_id, context=context)

            # Update name
            for order in self.browse(cr, uid, ids, context=context):
                vals['name'] = boi_type == 'BOI' and '%s-%s'%(cert.name, order.name[order.name.find('-') + 1:]) \
                                or boi_type == 'NONBOI' and order.name[order.name.find('-') + 1:] \
                                or (not boi_type and cert.id) and '%s-%s'%(cert.name, order.name[order.name.find('-') + 1:]) \
                                or order.name
        return super(purchase_order, self).write(cr, uid, ids, vals, context=context)

    def action_picking_create(self, cr, uid, ids, context=None):
        picking_id = super(purchase_order, self).action_picking_create(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        if picking_id:
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            name = picking.name

            for order in self.browse(cr, uid, ids, context=context):
                boi_cert_id = order.boi_cert_id and order.boi_cert_id.id or False

                # Update name
                if order.boi_type == 'BOI':
                    boi_cert_name = order.boi_cert_id and order.boi_cert_id.name or 'BOI'
                    name = '%s-%s'%(boi_cert_name, name[name.find('-') + 1:])
                picking_obj.write(cr, uid, [picking_id], {'name': name, 'boi_type': order.boi_type, 'boi_cert_id': boi_cert_id}, context=context)
        return picking_id

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        warehouse_name = boi_type == 'BOI' and 'FC_RM_BOI' or 'OF_RM'
        warehouse_ids = warehouse_obj.search(cr, uid, [('name','=',warehouse_name)], context=context)
        warehouse_id = len(warehouse_ids) > 0 and warehouse_ids[0] or False
        return {'value': {'boi_cert_id': False, 'warehouse_id': warehouse_id}}

purchase_order()
