# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from openerp import netsvc

from openerp.osv import fields,osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class purchase_requisition(osv.osv):
    
    _inherit = 'purchase.requisition'
    
    _columns = {
        'ref_order_id': fields.many2one('sale.order', 'Ref Sales Order', domain="[('state','not in',('draft','sent','cancel'))]"),
        'ref_project_name': fields.char('Ref Project Name', size=64, readonly=False),
    }
    
    def onchange_ref_order_id(self, cr, uid, ids, ref_order_id, context=None):
        v = {}
        if ref_order_id:
            order = self.pool.get('sale.order').browse(cr, uid, ref_order_id, context=context)
            if order.ref_project_name:
                v['ref_project_name'] = order.ref_project_name
        return {'value': v}
        
    def write(self,cr, uid, ids, vals, context=None):
        res = super(purchase_requisition, self).write(cr, uid, ids, vals, context=context)                    
        purchase_order = self.pool.get('purchase.order')
        purchase_order.update_ref_purchase_order(cr, uid, ids, context=context)
        return res
    #Fix issue #1007   
    #Override _seller_details from  purchase.requisition class
    def _seller_details(self, cr, uid, requisition_line, supplier, context=None):
        # Call super class
        seller_price, qty, default_uom_po_id, date_planned = super(purchase_requisition, self)._seller_details(cr, uid, requisition_line, supplier, context=context)
        # Recalculate seller_price
        pricelist = self.pool.get('product.pricelist')
        product = requisition_line.product_id
        supplier_pricelist = supplier.property_product_pricelist_purchase or False
        seller_price = pricelist.price_get(cr, uid, [supplier_pricelist.id], product.id, qty, supplier.id, {'uom': default_uom_po_id})[supplier_pricelist.id]
        return seller_price, qty, default_uom_po_id, date_planned
    
    # kittiu: This interited method will make description and name swapped. So, don't use it and overwrite it.
#     def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
#         res = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=context)
#         purchase_obj = self.pool.get('purchase.order')
#         purchase_line_obj = self.pool.get('purchase.order.line')
#         for id in ids:
#             # Prepare PR Line's Desc
#             pr_line_desc = set()
#             for pr_line in self.browse(cr, uid, id).line_ids:
#                 pr_line_desc.add(pr_line.name)
#             # Write Description
#             i = 0
#             order = purchase_obj.browse(cr, uid, res[id])
#             for line in order.order_line:
#                 purchase_line_obj.write(cr, uid, [line.id], {'name': list(pr_line_desc)[i]})
#                 i += 1
#         return res
    
    # Complete overwrite method from purchase_requisition.make_purchase_rder
    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        """
        Create New RFQ for Supplier
        """
        if context is None:
            context = {}
        assert partner_id, 'Supplier should be specified'
        purchase_order = self.pool.get('purchase.order')
        purchase_order_line = self.pool.get('purchase.order.line')
        res_partner = self.pool.get('res.partner')
        fiscal_position = self.pool.get('account.fiscal.position')
        supplier = res_partner.browse(cr, uid, partner_id, context=context)
        supplier_pricelist = supplier.property_product_pricelist_purchase or False
        res = {}
        for requisition in self.browse(cr, uid, ids, context=context):
            if supplier.id in filter(lambda x: x, [rfq.state <> 'cancel' and rfq.partner_id.id or None for rfq in requisition.purchase_ids]):
                raise osv.except_osv(_('Warning!'), _('You have already one %s purchase order for this partner, you must cancel this purchase order to create a new quotation.') % rfq.state)
            location_id = requisition.warehouse_id.lot_input_id.id
            purchase_id = purchase_order.create(cr, uid, {
                        'origin': requisition.name,
                        'partner_id': supplier.id,
                        'pricelist_id': supplier_pricelist.id,
                        'location_id': location_id,
                        'company_id': requisition.company_id.id,
                        'fiscal_position': supplier.property_account_position and supplier.property_account_position.id or False,
                        'requisition_id':requisition.id,
                        'notes':requisition.description,
                        'warehouse_id':requisition.warehouse_id.id ,
            })
            res[requisition.id] = purchase_id
            for line in requisition.line_ids:
                product = line.product_id
                seller_price, qty, default_uom_po_id, date_planned = self._seller_details(cr, uid, line, supplier, context=context)
                taxes_ids = product.supplier_taxes_id
                taxes = fiscal_position.map_tax(cr, uid, supplier.property_account_position, taxes_ids)
                purchase_order_line.create(cr, uid, {
                    'order_id': purchase_id,
                    # kittiu: Force use PR Line's Desc, instead of product.partner_ref
                    #'name': product.partner_ref,
                    'name': line.name,
                    # --
                    'product_qty': qty,
                    'product_id': product.id,
                    'product_uom': default_uom_po_id,
                    'price_unit': seller_price,
                    'date_planned': date_planned,
                    'taxes_id': [(6, 0, taxes)],
                }, context=context)
                
        return res
        
purchase_requisition()

class purchase_requisition_line(osv.osv):

    _inherit = "purchase.requisition.line"

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True, domain=[('purchase_ok', '=', True)]),
        'name': fields.text('Description', required=True),
    }
    
    def onchange_product_id(self, cr, uid, ids, product_id, product_uom_id, context=None):
        res = super(purchase_requisition_line, self).onchange_product_id(cr, uid, ids, product_id, product_uom_id, context=context)
        product_product = self.pool.get('product.product')
        product = product_product.browse(cr, uid, product_id, context=context)
        dummy, name = product_product.name_get(cr, uid, product_id, context=context)[0]
        if product.description_purchase:
            name += '\n' + product.description_purchase
        res['value'].update({'name': name})
        
        return res

purchase_requisition_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
