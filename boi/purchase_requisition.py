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
        'boi_number_id': fields.many2one('boi.certificate', 'BOI Number'),
    }

    _defaults = {
        'boi_type': 'NONBOI',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.requisition')
        vals.update({'name': vals.get('boi_type', '') + '-' + vals.get('name', '')})
        return super(purchase_requisition, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        for requisition in self.browse(cr, uid, ids, context=context):
            if 'boi_type' in vals:
                if requisition.name.find(vals['boi_type']) < 0:
                    if requisition.name.find('BOI') >= 0 and vals['boi_type'] == 'NONBOI':
                        name = requisition.name.replace('BOI', 'NONBOI')
                    else:
                        name = vals['boi_type'] + '-' + requisition.name
                else:
                    if requisition.name.find('NONBOI') >=0 and vals['boi_type'] == 'BOI':
                        name = requisition.name.replace('NONBOI', 'BOI')
                    else:
                        name = requisition.name
                vals.update({'name': name})
        return super(purchase_requisition, self).write(cr, uid, ids, vals, context=context)

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        res = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)
        order_obj = self.pool.get('purchase.order')
        for requisition in self.browse(cr, uid, ids, context=context):
            if not isinstance(res.get(requisition.id, False), list):
                order_ids = [res.get(requisition.id, False)]
            if order_ids:
                order = order_obj.browse(cr, uid, order_ids, context=context)[0]
                name = requisition.boi_type + '-' + order.name
                order_obj.write(cr, uid, order_ids, {'boi_type': requisition.boi_type, 'boi_number_id': requisition.boi_number_id.id, 'name': name}, context=context)
        return res

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_number_id': False}}

purchase_requisition()
