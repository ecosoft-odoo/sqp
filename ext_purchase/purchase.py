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

import types
import netsvc
from osv import osv, fields
import openerp.addons.decimal_precision as dp

class purchase_order(osv.osv):

    _inherit = "purchase.order"
    _columns = {
        'ref_attention_id': fields.many2one('res.partner', 'Attention',  domain="[('parent_id','=', partner_id)]", readonly=False),
        'ref_order_id': fields.many2one('sale.order', 'Ref Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", readonly=False),
        'ref_project_name': fields.char('Ref Project Name', size=128, readonly=False),
        'ref_purchase_id': fields.many2one('purchase.order', 'Ref Purchase Order', domain="[('state','not in',('draft','sent','confirmed'))]", readonly=False),
    }
    
    def onchange_ref_order_id(self, cr, uid, ids, ref_order_id, context=None):
        v = {}
        if ref_order_id:
            order = self.pool.get('sale.order').browse(cr, uid, ref_order_id, context=context)
            if order.ref_project_name:
                v['ref_project_name'] = order.ref_project_name
        return {'value': v}
    
    #   Enhancement issue #1006 
    def create(self, cr, uid, vals, context=None):        
        order =  super(purchase_order, self).create(cr, uid, vals, context=context)
        if vals.get('requisition_id', False):
            self.update_ref_purchase_order(cr, uid, [vals['requisition_id']], context) 
            #     Enhancement  issue #1005
            pr_obj = self.pool.get('purchase.requisition')
            po_ids = pr_obj.search(cr,uid,[('id','=',vals['requisition_id']),('state','=','draft')])
            if po_ids:
                pr_obj.tender_in_purchase(cr, uid, [vals['requisition_id']], context)
            #     Enhancement  issue #1005 
        return order
    
    def update_ref_purchase_order(self, cr, uid, requisition_ids, context=None):
        res = {}
        pr_obj = self.pool.get('purchase.requisition')
        for pr in pr_obj.browse(cr, uid, requisition_ids, context=context):
            res = {
                'ref_order_id': pr.id and pr.ref_order_id.id or False,
                'ref_project_name': pr.id and pr.ref_project_name or False
            }
            prids=self.search(cr,uid,[('requisition_id','in',requisition_ids)])
            self.write(cr, uid, prids, res, context=context)
            
    def update_ref_incoming_shipment(self, cr, uid, purchase_ids, context=None):
        res = {}
        sk_obj = self.pool.get('stock.picking.in')
        stock_ids = sk_obj.search(cr,uid,[('purchase_id','in',purchase_ids)])
        for po_rec in self.browse(cr, uid, purchase_ids, context=context):
            res = {
                'ref_order_id': po_rec.ref_order_id and po_rec.ref_order_id.id or False,
                'ref_project_name': po_rec.ref_project_name or False,
            }
            stock_ids = sk_obj.search(cr,uid,[('purchase_id','=',po_rec.id)])
            sk_obj.write(cr, uid, stock_ids, res, context=context)        

#     Enhancement  issue #1005            
    def print_quotation(self, cr, uid, ids, context=None):       
        res =  super(purchase_order, self).print_quotation(cr, uid, ids, context=context)
        pr_obj = self.pool.get('purchase.requisition')
        for po in self.browse(cr, uid, ids, context=context):
            if po.requisition_id and po.requisition_id.id!="" and po.requisition_id.state in ['draft','in_purchase']:
                pr_obj.tender_in_progress(cr, uid, [po.requisition_id.id],context=context)
        return res

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        if super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context=context):
            pr_obj = self.pool.get('purchase.requisition')
            for po in self.browse(cr, uid, ids, context=context):
                if po.requisition_id and po.requisition_id.id!="" and po.requisition_id.state in ['draft','in_purchase','in_progress']:
                    pr_obj.tender_done(cr, uid, [po.requisition_id.id],context=context)
        return True

purchase_order()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
