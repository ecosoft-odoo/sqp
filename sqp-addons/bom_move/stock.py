# -*- coding: utf-8 -*-
from osv import osv, fields
from openerp.tools.translate import _


class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
        'is_bom_move': fields.boolean('BOM Move', readonly=False),
        'ref_mo_id': fields.many2one('mrp.production', 'Ref MO',
                                     domain=[('parent_id', '=', False)]),
        'ref_sub_mo_ids': fields.related('ref_mo_id', 'child_ids',
                                         type='one2many',
                                         relation='mrp.production',
                                         string='Ref Sub-MOs', readonly=True),
        'department_id': fields.many2one('hr.department', 'Department',
                                         readonly=False),
    }

    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        if len(ids) > 1:
            raise osv.except_osv(_('Error!'), _('Not multiple value!!!'))
        res = super(stock_picking, self).do_partial(cr, uid, ids, partial_datas, context)
        if len(ids) > 0:
            pickings = self.browse(cr, uid, ids)
            if pickings[0].is_bom_move and pickings[0].state != 'done':
                name = self.pool.get('ir.sequence').get(cr, uid, 'bom.move')
                self.write(cr, uid, ids, {'name': name})
        return res

stock_picking()


class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    _columns = {
        'is_bom_move': fields.boolean('BOM Move', readonly=False),
        'ref_mo_id': fields.many2one('mrp.production', 'Ref MO',
                                     domain=[('parent_id', '=', False)]),
        'ref_sub_mo_ids': fields.related('ref_mo_id', 'child_ids',
                                         type='one2many',
                                         relation='mrp.production',
                                         string='Ref Sub-MOs',
                                         readonly=True),
        'department_id': fields.many2one('hr.department', 'Department',
                                         readonly=False),
    }
    _defaults = {
        'is_bom_move': lambda s, cr, uid, c: c.get('is_bom_move', False),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default.get('name', '/') == '/':
            picking_obj = self.pool.get('stock.picking')
            picking = picking_obj.browse(cr, uid, id, context=context)
            if picking.id and picking.is_bom_move:
                name = self.pool.get('ir.sequence').get(cr, uid, 'bom.move')
                default.update(name=name)
        return super(stock_picking_out, self).copy(cr, uid, id, default=default, context=context)

    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name') == '/'):
            # For BOM Move
            seq_obj_name = \
                vals.get('is_bom_move', False) and 'bom.move' or False
            if seq_obj_name:
                vals['name'] = \
                    self.pool.get('ir.sequence').get(cr, user, seq_obj_name)
        new_id = super(stock_picking_out, self).create(cr, user, vals, context)
        return new_id

stock_picking_out


class stock_move(osv.osv):
    _inherit = 'stock.move'

    _order = 'default_code, name_template, date_expected desc, id'

    _columns = {
        'default_code': fields.related('product_id', 'default_code',
                                       type='char',
                                       string='Internal Reference',
                                       readonly=False,
                                       store=True, ),
        'name_template': fields.related('product_id', 'name_template',
                                        type='char',
                                        string='Template Name',
                                        readonly=False,
                                        store=True, ),
    }

stock_move()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
