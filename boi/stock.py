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

class stock_picking(osv.osv):

    _inherit = 'stock.picking'

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

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        picking_obj = self.browse(cr, uid, id, context=context)
        seq_obj_name = 'stock.picking' + ('.' + picking_obj.type if picking_obj.type != 'internal' else '')
        default['name'] = picking_obj.boi_type + '-' + self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
        default.setdefault('origin', False)
        default.setdefault('backorder_id', False)
        return super(stock_picking, self).copy(cr, uid, id, default, context)

stock_picking()


class stock_picking_out(osv.osv):

    _inherit = 'stock.picking.out'

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

    def create(self, cr, user, vals, context=None):
        seq_obj_name =  self._name
        old_name = self.pool.get('ir.sequence').get(cr, user, seq_obj_name)
        vals['name'] = vals['boi_type'] + '-' + old_name
        return super(stock_picking_out, self).create(cr, user, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        for picking in self.browse(cr, uid, ids, context=context):
            if 'boi_type' in vals:
                if picking.name.find(vals['boi_type']) < 0:
                    if picking.name.find('BOI') >= 0 and vals['boi_type'] == 'NONBOI':
                        name = picking.name.replace('BOI', 'NONBOI')
                    else:
                        name = vals['boi_type'] + '-' + picking.name
                else:
                    if picking.name.find('NONBOI') >= 0 and vals['boi_type'] == 'BOI':
                        name = picking.name.replace('NONBOI', 'BOI')
                    else:
                        name = picking.name
                vals.update({'name': name})
        return super(stock_picking_out, self).write(cr, uid, ids, vals, context=context)

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_number_id': False}}

stock_picking_out()


class stock_picking_in(osv.osv):

    _inherit = 'stock.picking.in'

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

    def create(self, cr, user, vals, context=None):
        seq_obj_name =  self._name
        vals['name'] = self.pool.get('ir.sequence').get(cr, user, seq_obj_name)
        vals['name'] = vals['boi_type'] + '-' + vals['name']
        return super(stock_picking_in, self).create(cr, user, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        for picking in self.browse(cr, uid, ids, context=context):
            if vals.get('boi_type', False):
                if picking.name.find(vals.get('boi_type')) < 0:
                    if picking.name.find('BOI') >= 0 and vals.get('boi_type') == 'NONBOI':
                        name = picking.name.replace('BOI', 'NONBOI')
                    else:
                        name = vals.get('boi_type') + '-' + picking.name
                else:
                    if picking.name.find('NONBOI') >= 0 and vals.get('boi_type') == 'BOI':
                        name = picking.name.replace('NONBOI', 'BOI')
                    else:
                        name = picking.name
                vals.update({'name': name})
        return super(stock_picking_in, self).write(cr, uid, ids, vals, context=context)

    def onchange_boi_type(self, cr, uid, ids, boi_type, context=None):
        return {'value': {'boi_number_id': False}}
