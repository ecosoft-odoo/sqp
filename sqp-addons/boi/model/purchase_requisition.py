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

class purchase_requisition(osv.osv):

    _inherit = 'purchase.requisition'

    _columns = {
        'boi_type': fields.selection([
            ('NONBOI', 'NONBOI'),
            ('BOI', 'BOI'),
            ], 'BOI Type', required=True, select=True,
        ),
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.requisition') or '/'
            boi_type = vals.get('boi_type','') == 'BOI' and 'BOI' or 'NONBOI'
            vals.update({'name': '%s-%s'%(boi_type, vals.get('name', '/'))})
        return super(purchase_requisition, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        requisition_id = super(purchase_requisition, self).copy(cr, uid, id, default=default, context=context)
        if requisition_id:
            requisition = self.browse(cr, uid, requisition_id, context=context)
            boi_type = requisition.boi_type == 'BOI' and 'BOI' or 'NONBOI'
            name = '%s-%s'%(boi_type,requisition.name)
            self.write(cr, uid, [requisition_id], {'name': name}, context=context)
        return requisition_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        boi_type = vals.get('boi_type', False)
        if boi_type:
            boi_type = boi_type == 'BOI' and 'BOI' or 'NONBOI'
            for requisition in self.browse(cr, uid, ids, context=context):
                vals['name'] = requisition.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(purchase_requisition, self).write(cr, uid, ids, vals, context=context)

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        result = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)
        order_obj = self.pool.get('purchase.order')
        for requisition in self.browse(cr, uid, ids, context=context):
            order_id = result.get(requisition.id, False)
            if order_id:
                order = order_obj.browse(cr, uid, order_id, context=context)
                boi_type = requisition.boi_type
                boi_cert_id = requisition.boi_cert_id and requisition.boi_cert_id.id \
                                or False
                name = '%s-%s'%(boi_type,order.name)
                order_obj.write(cr, uid, [order_id], {'name': name, 'boi_type': boi_type, 'boi_cert_id': boi_cert_id}, context=context)
        return result

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        warehouse_name = boi_type == 'BOI' and 'FC_RM_BOI' or 'OF_RM'
        warehouse_ids = warehouse_obj.search(cr, uid, [('name','=',warehouse_name)], context=context)
        warehouse_id = len(warehouse_ids) > 0 and warehouse_ids[0] or False
        return {'value': {'boi_cert_id': False, 'warehouse_id': warehouse_id}}

purchase_requisition()
