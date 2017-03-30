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
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict", domain="[('start_date','!=',False),('active','!=',False)]"),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        requisition_id = super(purchase_requisition, self).create(cr, uid, vals, context=context)
        if requisition_id:
            requisition = self.browse(cr, uid, requisition_id, context=context)

            # Update name
            if requisition.boi_type == 'BOI':
                boi_cert_name = requisition.boi_cert_id and requisition.boi_cert_id.name or 'BOI'
                name = '%s-%s'%(boi_cert_name, requisition.name[requisition.name.find('-') + 1:])
                self.write(cr, uid, [requisition_id], {'name': name}, context=context)
        return requisition_id

    def write(self, cr, uid, ids, vals, context=None):
        boi_type = vals.get('boi_type', False)
        boi_cert_id = vals.get('boi_cert_id', False)
        if boi_type or boi_cert_id:
            cert_obj = self.pool.get('boi.certificate')

            cert = cert_obj.browse(cr, uid, boi_cert_id, context=context)

            # Update name
            for requisition in self.browse(cr, uid, ids, context=context):
                vals['name'] = boi_type == 'BOI' and '%s-%s'%(cert.name, requisition.name[requisition.name.find('-') + 1:]) \
                                or boi_type == 'NONBOI' and requisition.name[requisition.name.find('-') + 1:] \
                                or (not boi_type and cert.id) and '%s-%s'%(cert.name, requisition.name[requisition.name.find('-') + 1:]) \
                                or requisition.name
        return super(purchase_requisition, self).write(cr, uid, ids, vals, context=context)

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        result = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)
        order_obj = self.pool.get('purchase.order')
        for requisition in self.browse(cr, uid, ids, context=context):
            order_id = result.get(requisition.id, False)
            if order_id:
                order = order_obj.browse(cr, uid, order_id, context=context)
                name = order.name
                boi_cert_id = requisition.boi_cert_id and requisition.boi_cert_id.id or False

                # Update name
                if requisition.boi_type == 'BOI':
                    boi_cert_name = requisition.boi_cert_id and requisition.boi_cert_id.name or 'BOI'
                    name = '%s-%s'%(boi_cert_name, name[name.find('-') + 1:])
                order_obj.write(cr, uid, [order_id], {'name': name, 'boi_type': requisition.boi_type, 'boi_cert_id': boi_cert_id}, context=context)
        return result

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        warehouse_obj = self.pool.get('stock.warehouse')
        warehouse_name = boi_type == 'BOI' and 'FC_RM_BOI' or 'OF_RM'
        warehouse_ids = warehouse_obj.search(cr, uid, [('name','=',warehouse_name)], context=context)
        warehouse_id = len(warehouse_ids) > 0 and warehouse_ids[0] or False
        return {'value': {'boi_cert_id': False, 'warehouse_id': warehouse_id}}

purchase_requisition()
