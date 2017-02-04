# -*- coding: utf-8 -*-
from osv import osv, fields


class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
        'is_bom_move': fields.boolean('BOM Move', readonly=True),
        'ref_mo_id': fields.many2one('mrp.production', 'Ref MO', domain=[('parent_id', '=', False)]),
        'ref_sub_mo_ids': fields.related('ref_mo_id', 'child_ids', type='one2many', relation='mrp.production', string='Ref Sub-MOs', readonly=True),
        'department_id': fields.many2one('hr.department', 'Department', readonly=False),
    }

stock_picking()


class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    _columns = {
        'is_bom_move': fields.boolean('BOM Move', readonly=True),
        'ref_mo_id': fields.many2one('mrp.production', 'Ref MO', domain=[('parent_id', '=', False)]),
        'ref_sub_mo_ids': fields.related('ref_mo_id', 'child_ids', type='one2many', relation='mrp.production', string='Ref Sub-MOs', readonly=True),
        'department_id': fields.many2one('hr.department', 'Department', readonly=False),
    }
    _defaults = {
        'is_bom_move': lambda s, cr, uid, c: c.get('is_bom_move', False),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        picking_obj = self.browse(cr, uid, id, context=context)
        if ('name' not in default) or (picking_obj.name == '/'):
            # For BOM Move
            if picking_obj.is_bom_move:
                default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'bom.move')
        res = super(stock_picking_out, self).copy(cr, uid, id, default=default, context=context)
        return res

    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name') == '/'):
            # For BOM Move
            seq_obj_name = vals.get('is_bom_move', False) and 'bom.move' or False
            if seq_obj_name:
                vals['name'] = self.pool.get('ir.sequence').get(cr, user, seq_obj_name)
        new_id = super(stock_picking_out, self).create(cr, user, vals, context)
        return new_id


class stock_move(osv.osv):

    _inherit = 'stock.move'

stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
