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
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from dateutil.relativedelta import relativedelta
import netsvc
from osv import osv, fields
from tools.translate import _

class stock_move_add(osv.osv_memory):

    _inherit = 'stock.move.add'

    _columns = {
        'product_categ_id': fields.many2one('product.category', 'Product Category'),
    }
    
stock_move_add()


class stock_move(osv.osv):
    _inherit = "stock.move"
    #
    # Cancel move => cancel others move and pickings
    #
    def action_consume_cancel(self, cr, uid, ids, context=None):
        """ Cancels the moves and if all moves are cancelled it cancels the picking.
        @return: True
        """
        if not ids:
            return True
        
        new_move = self.browse(cr, uid, ids, context)[0]
        
        sm_ids = self.search(cr, uid, [('move_dest_id','=', new_move.id)], context=context)
        sp_picking = False
        if sm_ids:
            for move in self.browse(cr, uid, sm_ids):
                sp_picking = move.picking_id
                if move.state == 'done':
                    self.write(cr, uid, [move.id], {'state': 'cancel'})
                else:
                    self.action_cancel(cr, uid, [move.id], context=context)
        # kittiu -- do not remove scheduled product
#         if sp_picking:            
#             mrp_obj = self.pool.get('mrp.production')
#             mo_ids = mrp_obj.search(cr, uid, [('picking_id','=', sp_picking.id)], context=context)
#             if mo_ids:
#                 prod_line_obj = self.pool.get('mrp.production.product.line')
#                 ml_ids = prod_line_obj.search(cr, uid, [('production_id','=', mo_ids[0]),('product_id','=', new_move.product_id.id)], context=context)
#                 if ml_ids:
#                     prod_line = prod_line_obj.browse(cr, uid, ml_ids)[0]
#                     compare = float_compare(prod_line.product_qty, new_move.product_qty, precision_rounding=4)
#                     if compare == 0:
#                         prod_line_obj.unlink(cr, uid, [prod_line.id], context=context)
#                     elif compare > 0:
#                         prod_line_obj.write(cr, uid, [prod_line.id], {'product_qty': prod_line.product_qty - new_move.product_qty})
                    
        self.action_cancel(cr, uid, [new_move.id], context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
