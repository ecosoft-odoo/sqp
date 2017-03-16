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

import netsvc
from osv import osv, fields
import decimal_precision as dp
from tools.translate import _

class product_product(osv.osv):
    
    _inherit = "product.product"    
    
    def _check_product_name(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        for record in self.browse(cr, uid, ids, context=context):
            if record.ref_order_id: # Only for ref_order case.
                ids = product_obj.search(cr, uid, [('name','=',record.name),('ref_order_id','=',record.ref_order_id.id)])
                if len(ids) > 1:
                    raise osv.except_osv(_('Error'), _('You cannot create product with name %s')% (record.name,))
        return True
    
    _columns = {
        'sequence': fields.integer('Sequence'),
        'is_one_time_use': fields.boolean('One-Time Use', required=False, help="One time used product are those product created from Rapid Product Creation wizard as they are linked to specific SO"),
        'ref_order_id':fields.many2one('sale.order','Ref Sales Order', readonly=False, domain="[('state','not in',('draft','sent','cancel'))]", help='This product is created from this Sales Order'),
        'W':fields.float('Width (W)', readonly=False),
        'L':fields.float('Length (L)', readonly=False),
        'T':fields.many2one('bom.choice.thick', 'Thick (T)', readonly=False),
        'mat_inside_skin_choices':fields.many2one('bom.choice.skin', 'Inside Skin', readonly=False),
        'mat_outside_skin_choices':fields.many2one('bom.choice.skin', 'Outside Skin', readonly=False),
        'mat_insulation_choices':fields.many2one('bom.choice.insulation', 'Insulation', readonly=False),
        'cut_area':fields.float('Cut Area (sqm)'),
        'bom_product_type':fields.selection([('panel','Panel'),
                                             ('door','Door'),
                                             ('window','Window'),],'BOM Product Type', readonly=False),
        'remark':fields.char('Remarks', size=128),    
    }
    _defaults = {
        'is_one_time_use' : False,
    }
    _constraints = [
        (_check_product_name, 'Name must be unique for the same Sales Order',
            ['name','ref_order_id'])]
    
    def unlink(self, cr, uid, ids, context=None):
        # Delete BOM before delete product
        bom_obj = self.pool.get('mrp.bom')
        bom_ids = bom_obj.search(cr, uid, [('product_id', 'in', ids)], context=context)
        bom_obj.unlink(cr, uid, bom_ids, context=context)        
        return super(product_product, self).unlink(cr, uid, ids, context=context)
    
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
