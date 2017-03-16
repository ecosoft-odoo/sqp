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
from openerp.tools.translate import _

class product_make_bom(osv.osv_memory):
    _inherit = "product.make.bom"
    
    def _get_ref_order_id(self, cr, uid, context=None):
        if context == None:
            context = {}
        # If ref_order_id is in context, simply use it.
        if context.get('ref_order_id', False):
            return context.get('ref_order_id')
        
        ids = context.get('active_ids', [0])
        cr.execute('select ref_order_id, count from \
                        (select ref_order_id, count(*) as count \
                        from product_product where ref_order_id > 0 \
                        and id in %s \
                        group by ref_order_id) a order by count desc',(tuple(ids),))
        res = cr.fetchall()
        if len(res):
            if len(res) == 1:
                return res[0][0]
            else:
                raise osv.except_osv(_('Warning!'), _('You cannot create BOM from products of different "Ref Sales Order"'))
        else:
            return False         
    
    _columns = {
        'is_one_time_use': fields.boolean('One-Time'),
        'ref_order_id': fields.many2one('sale.order','Ref Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", readonly=False, help='This product is created for this Sales Order'),
    }
    _defaults = {
        'is_one_time_use': True,
        'ref_order_id': _get_ref_order_id,
    }
    
    def onchange_ref_order_id(self, cr, uid, ids, ref_order_id, context=None):
        v = {}
        if ref_order_id:
            order = self.pool.get('sale.order').browse(cr, uid, ref_order_id, context=context)
            if order.ref_project_name:
                v['product_name'] = order.ref_project_name
        return {'value': v}

product_make_bom()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
