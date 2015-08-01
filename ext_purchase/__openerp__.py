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

{
    'name' : "Extensions for Purchase",
    'author' : 'Kitti U.',
    'summary': '',
    'description': """
Features
========
* In Purchase Requisition, remove Send to Suppliers button and states.
* In Purchase Order, new Attention, Ref Sales Order, Ref Project Name field.
* * Reference these 2 fields to Incoming Shipment and Supplier Invoice.
* 2 Document Sequence,
* * Purchase Order (SP)
* * Purchase Requisition (PR)
* In Purchase Requisition, field Date Start and Date End to be date, not datetime.
* Enhancement issue #1006 
* * Purchase Requisition
* * * new Attention, Ref Sales Order, Ref Project Name field
* * * Overloading write method for call "update_ref_purchase_order" method in PO.
* * Purchase Order 
* * * New "update_ref_purchase_order" method for copy Ref Sales Order and Ref Project Name  from PR to PO.
* * * Overloading create method for call "update_ref_purchase_order" method.
* Enhancement issue #1005
* * Purchase Order
* * * Overriding print_quotation method for change state in PR is in_progress(Sent to Suppliers)
* * * Overriding wkf_confirm_order method for change state in PR is done(Purchase Done)
* * * Modification create method for change state in PR is in_purchase(Sent to Purchase) when has been create first new quotation.
* Fix issue #1007
* * sqp-addons/Purchase Requisition
* * * Overriding _seller_details method, replace partner_id parameter with supplier id  on call price_get function
* * * Overriding make_purchase_order method    
* Ensure that Purchase Requisition Line, only Product for Purchase will be selectable.
* Enhancement #1052
* * Supplier Field in PO to show only Company (no contact).
* * Attention to be contact according to selected Supplier
* Feature #1050,#1051, Add permission of PR group to access the Purchases root menu, purchase requisition and purchase order module. 
* Purchase Requisition's Description
* Add new Ref Purchase Order field in PO, for manual input.

""",
    'category': 'Purchase Management',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['web_m2o_enhanced','stock','purchase','purchase_requisition','picking_invoice_relation',
                 'purchase_requisition_double_validation'],
    'demo' : [],
    'data' : [
        'purchase_view.xml',
        'stock_view.xml',
        'account_invoice_view.xml',
        'purchase_requisition_view.xml',
        #'purchase_requisition_sequence.xml',
        #'purchase_sequence.xml'
         'security/ir.model.access.csv',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
