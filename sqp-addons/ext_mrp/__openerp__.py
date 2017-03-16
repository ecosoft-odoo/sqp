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
    'name' : "Extensions for MRP Module",
    'author' : 'Kitti U.',
    'summary': '',
    'description': """
New Windows
===========

Sales Order menu for manufacturing people (readonly and no price related information)

* Add Create Product/BOM from SO Line

Change menu name for Super MO (MO with no parents)

* A button to view all Child MOs
* Menu Super MO -> MO
* Menu Manufacturing Order -> Sub-MO

Create DO from MO
=================
* New "Create Delivery Order" button for Super MO when -- 1) SO exits, 2) State in (Confirmed, Ready) 3) Target DO not exist
* Once DO is created, Target Delivery Order will be filled with new DO
* Once MO is done, should trigger DO to state Ready to Deliver

MO Form
=======

For SQP Only, in order to manage its stock movement

* Super MO (product Project) --> Always set Source Location / Destination Location = Production / Production
* Sub MO (produce W1, W2) --> Always set Source Location / Destination Location = Production / Factory FG

Allow adding RM in confirmed MO

* Only available for Super MO
* Default Location --> Always set Source Location / Destination Location = Production / Production
* Only Parts listed for product selection.

MO
==

* Use Product's sequence as ordering sequence in Status Tracking tab.
* When remove Product to Consume, do not remove it from Scheduled Product
* When create DO from MO, use MO's schedule date for DO.
* Allow cancel MO and all its Sub MOs (only when all Sub-MO are not produced
* Validation, Super MO must have 1 level of Sub-MO only.

""",
    'category': 'Manufacturing',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['mrp','mrp_sale_rel','ext_sale','mrp_change_rm','mrp_quick_bom'],
    'demo' : [],
    'data' : [
        'sale_view.xml',
        'mrp_view.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
