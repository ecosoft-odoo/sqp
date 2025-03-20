# -*- coding: utf-8 -*-
from osv import osv, fields
from openerp.tools.translate import _

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'

    def _prepare_batch_move_vals(self, cr, uid, department, context=None):
        return{
            'date': fields.date.context_today(self, cr, uid, context=context),
            'department_id': next(iter(department)),
            'ref_bom_ids': [(6, 0, context.get('active_ids', []))],
        }
    
    def _create_bom_move_batch(self, cr, uid, ids, context=None):
        ''' Create a new batch of moves based on the selected moves.'''
        if context is None:
            context = {}

        picking_ids = context.get('active_ids', [])
        if not picking_ids:
            raise osv.except_osv(_('Error!'), _('No Bom moves selected.'))
        
        picks = self.read(cr, uid, picking_ids, ['department_id', 'state'], context=context)

        if any(x['state'] != 'done' for x in picks):
            raise osv.except_osv(_('Error!'), _('All selected BOM moves must be in "Transferred" state.'))
        
        department_ids = set([x['department_id'][0] for x in picks])
        if len(department_ids) != 1:
            raise osv.except_osv(_('Error!'), _('All selected Bom moves must belong to the same department.'))
        
        vals = self._prepare_batch_move_vals(cr, uid, department_ids, context=context)
        
        move_obj = self.pool.get('bom.move.batch')
        move_id = move_obj.create(cr, uid, vals, context)
        move = move_obj.browse(cr, uid, move_id, context)
        view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'bom_move_batch', 'view_bom_move_batch_form')
    
        result = {
            'name': _('Bom Move Batch'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'bom.move.batch',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id,
        }
        return result
        
stock_picking_out
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
