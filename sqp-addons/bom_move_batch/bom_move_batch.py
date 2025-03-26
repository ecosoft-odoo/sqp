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

import time
from osv import osv, fields
from openerp.tools.translate import _

class bom_move_batch(osv.osv):
    _name = 'bom.move.batch'
    _inherit = ['mail.thread']
    _description = "Bom Move Batch"
    _order = "id desc"
    _columns = {
        'name': fields.char('Name', size=64, required=True, readonly=True),
        'date': fields.date('Date', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'department_id': fields.many2one('hr.department', 'Department', readonly=True, states={'draft': [('readonly', False)]}),
        'ref_bom': fields.char('Reference', readonly=True),
        'ref_mo': fields.char('Reference MO', readonly=True),
        'ref_bom_ids': fields.many2many(
            'stock.picking.out',
            'bom_move_batch_bom_rel',
            'bom_move_batch_id',
            'bom_move_id',
            'Reference BOMs', readonly=True, states={'draft': [('readonly', False)]}
        ),
        'ref_mo_ids': fields.many2many(
            'mrp.production',
            'bom_move_batch_mo_rel',
            'bom_move_batch_id',
            'mo_id',
            'Reference MOs', required=True, readonly=True, states={'draft': [('readonly', False)]}
        ),
        'state':fields.selection(
            [
                ('draft','Draft'),
                ('done','Done'),
                ('cancel','Cancelled'),
            ], 'Status', readonly=True, track_visibility='onchange', size=32),
        'move_lines': fields.one2many('bom.move.batch.line', 'bom_move_batch_id', 'Internal Moves', readonly=True),
        'note': fields.text('Note'),
    }
    _defaults = {
        'state': 'draft',
        'name': '/',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    def copy(self, cr, uid, id, defaults, context=None):
        defaults['name'] = self.pool.get('ir.sequence').get(cr, uid, 'bom.move.batch')
        defaults['state'] = 'draft'
        return super(bom_move_batch, self).copy(cr, uid, id, defaults, context=context)
    
    def create_send_note(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            message = "Bom Move Batch Document <b>created</b>."
            self.message_post(cr, uid, [obj.id], body=message, context=context)
        
    def _get_batch_bom(self, cr, uid, batch_data, context=None):
        return ' ,'.join(sorted(batch_data['name']))

    def _get_batch_mo(self, cr, uid, batch_data, context=None):
        return ' ,'.join(sorted(batch_data['ref_mo']))
    
    def _prepare_batch_move_line_vals(self, cr, uid, batch_data, context=None):
        move_lines = []
        product_obj = self.pool.get('product.product')
        for product_id, data in batch_data['move_lines'].items():
            product = product_obj.browse(cr, uid, product_id)
            move_line = (
                    0, 
                    0,
                {
                    'name': product.name,
                    'product_id': product.id,
                    'product_qty': data['product_qty'],
                    'product_uom': product.uom_id.id,
                    'order_qty': data['order_qty'],
                    'product_uos': data
                }
            )
            move_lines.append(move_line)
        return move_lines

    def _get_batch(self, cr, uid, picking_ids, context=None):
        pick_obj = self.pool.get('stock.picking.out')
        move_obj = self.pool.get('stock.move')
        picks = pick_obj.read(cr, uid, picking_ids, ['department_id', 'name', 'ref_mo_id', 'move_lines'], context=context)
        batch_data = {
            'department_id': set(),
            'name': set(),
            'ref_mo': set(),
            'move_lines': {},
        }

        for pick in picks:
            if pick.get('department_id'):
                batch_data['department_id'].add(pick['department_id'][0])
            if pick.get('name'):
                batch_data['name'].add(pick['name'])
            if pick.get('ref_mo_id'):
                batch_data['ref_mo'].add(pick['ref_mo_id'][1])
            move_lines = pick.get('move_lines', False)
            if not move_lines:
                continue
            data_list = ['product_id', 'product_qty', 'order_qty']
            moves = move_obj.read(cr, uid, move_lines, data_list, context=context)

            for move in moves:
                product_id = move['product_id'][0]
                product_qty = move['product_qty']
                order_qty = move['order_qty']

                if product_id in batch_data['move_lines']:
                    batch_data['move_lines'][product_id]['product_qty'] += product_qty
                    batch_data['move_lines'][product_id]['order_qty'] += order_qty
                else:
                    batch_data['move_lines'][product_id] = {
                    'product_qty': product_qty,
                    'order_qty': order_qty,
                }  
            
        return batch_data
    
    def create(self, cr, uid, vals, context=None):
        picking_ids = vals.get('ref_bom_ids', False)
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'bom.move.batch') or '/'
        context.update({'mail_create_nolog': True})
        res = super(bom_move_batch, self).create(cr, uid, vals, context=context)
        self.create_send_note(cr, uid, [res], context=context)
        return res
        
    def write(self, cr, uid, ids, vals, context=None):
        mo_ids = vals.get('ref_mo_ids', False)
        pick_obj = self.pool.get('stock.picking.out')
        if mo_ids:
            picking_ids = pick_obj.search(
                cr, 
                uid, 
                [
                    ('ref_mo_id', 'in', mo_ids[0][2]),
                    ('type', '=', 'internal'),
                    ('is_bom_move', '=', True),
                    ('state', 'not in', ['cancel', 'done']),
                ],
                context=context)
            if picking_ids:
                vals['ref_bom_ids'] = [(6, 0, picking_ids)]        
        res = super(bom_move_batch, self).write(cr, uid, ids, vals, context=context)
        return res

    def action_done(self, cr, uid, ids, context=None):
        for batch in self.browse(cr, uid, ids, context=context):
            picking_ids = [rec.id for rec in batch.ref_bom_ids]
            if picking_ids:
                move_line_ids = self.pool.get('bom.move.batch.line').search(cr, uid, [('bom_move_batch_id', 'in', ids)], context=context)
                if move_line_ids:
                    self.pool.get('bom.move.batch.line').unlink(cr, uid, move_line_ids, context=context)
                batch_data = self._get_batch(cr, uid, picking_ids, context=context)
                if batch_data:
                    vals = {
                        'move_lines': self._prepare_batch_move_line_vals(cr, uid, batch_data, context=context),
                        'ref_bom': self._get_batch_bom(cr, uid, batch_data, context=context),
                        'ref_mo': self._get_batch_mo(cr, uid, batch_data, context=context),
                    }
                batch.write(vals)
                
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)
    
    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
    
    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

bom_move_batch()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: