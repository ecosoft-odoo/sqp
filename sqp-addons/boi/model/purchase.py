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
        'boi_number_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order') or '/'
        if vals.get('boi_type', False) and vals.get('name', False):
            vals.update({'name': '%s-%s'%(vals.get('boi_type'),vals.get('name'))})
        return super(purchase_order, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            if vals.get('boi_type', False):
                if order.name.find(vals.get('boi_type')) < 0:
                    if order.name.find('BOI') >= 0 and vals.get('boi_type') == 'NONBOI':
                        name = order.name.replace('BOI', 'NONBOI')
                    else:
                        name = '%s-%s'%(vals.get('boi_type'),order.name)
                else:
                    if order.name.find('NONBOI') >= 0 and vals.get('boi_type') == 'BOI':
                        name = order.name.replace('NONBOI', 'BOI')
                    else:
                        name = order.name
                vals.update({'name': name})
        return super(purchase_order, self).write(cr, uid, ids, vals, context=context)

    def action_picking_create(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).action_picking_create(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        if res:
            picking = picking_obj.browse(cr, uid, res, context=context)
            for order in self.browse(cr, uid, ids, context=context):
                name = '%s-%s'%(order.boi_type,picking.name)
                boi_number_id = order.boi_number_id and order.boi_number_id.id or False
                picking_obj.write(cr, uid, res, {'boi_type': order.boi_type, 'boi_number_id': boi_number_id, 'name': name})
        return res

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        name = boi_type == 'BOI' and 'FC_RM_BOI' or 'OF_RM'
        warehouse_ids = warehouse_obj.search(cr, uid, [('name','=',name)], context=context)
        res = warehouse_ids and {'boi_number_id': False, 'warehouse_id': warehouse_ids[0]} or {'boi_number_id': False}
        return {'value': res}

purchase_order()
