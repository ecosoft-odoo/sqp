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

from openerp.osv import osv, fields


class stock_move(osv.osv):

    _inherit = "stock.move"
    _columns = {
        'purchase_id': fields.many2one('purchase.order', 'Purchase Order Ref.'),
        'note': fields.text('Remark'),
    }

stock_move()


class stock_picking(osv.osv):

    _inherit = "stock.picking"

    _columns = {
        'ref_order_id': fields.many2one('sale.order', 'Ref Sales Order', domain="[('state','not in',('draft','sent','cancel'))]", ondelete='set null', select=True),
        'ref_project_name': fields.char('Ref Project Name', size=64, readonly=False),
        'department_id': fields.many2one('hr.department', 'Department', readonly=False),
        'car_plate': fields.char('Car Plate', size=64, readonly=False),
        'ref_order_tag_no': fields.related('ref_order_id', 'tag_no', type='text', relation='sale.order', string='TAG No. from Order', store=False, readonly=True),
        'tag_no': fields.text('TAG No.'),
    }

    def onchange_ref_order_id(self, cr, uid, ids, ref_order_id, context=None):
        v = {}
        if ref_order_id:
            order = self.pool.get('sale.order').browse(cr, uid, ref_order_id, context=context)
            if order.ref_project_name:
                v['ref_project_name'] = order.ref_project_name
        return {'value': v}

stock_picking()


class stock_picking_out(osv.osv):

    _inherit = "stock.picking.out"

    def get_min_max_date(self, cr, uid, ids, field_name, arg, context=None):
        return super(stock_picking_out, self).get_min_max_date(cr, uid, ids, field_name, arg, context=context)

    # Override
    def _set_maximum_date(self, cr, uid, ids, name, value, arg, context=None):
        """ Calculates planned date if it is greater than 'value'.
        @param name: Name of field
        @param value: Value of field
        @param arg: User defined argument
        @return: True or False
        """
        if not value:
            return False
        if isinstance(ids, (int, long)):
            ids = [ids]
        for pick in self.browse(cr, uid, ids, context=context):
            sql_str = """update stock_move set
                    date_expected='%s'
                where
                    picking_id=%d """ % (value, pick.id)
            # Remove
#             if pick.max_date:
#                 sql_str += " and (date_expected='" + pick.max_date + "')"
            cr.execute(sql_str)
        return True

    # Override
    def _set_minimum_date(self, cr, uid, ids, name, value, arg, context=None):
        """ Calculates planned date if it is less than 'value'.
        @param name: Name of field
        @param value: Value of field
        @param arg: User defined argument
        @return: True or False
        """
        if not value:
            return False
        if isinstance(ids, (int, long)):
            ids = [ids]
        for pick in self.browse(cr, uid, ids, context=context):
            sql_str = """update stock_move set
                    date_expected='%s'
                where
                    picking_id=%s """ % (value, pick.id)
            # Remove
#             if pick.min_date:
#                 sql_str += " and (date_expected='" + pick.min_date + "')"
            cr.execute(sql_str)
        return True

    _columns = {
        'car_plate': fields.char('Car Plate', size=64, readonly=False),
        'min_date': fields.function(get_min_max_date, fnct_inv=_set_minimum_date, multi="min_max_date",
                 store=True, type='datetime', string='Scheduled Time', select=1, help="Scheduled time for the shipment to be processed"),
        'max_date': fields.function(get_min_max_date, fnct_inv=_set_maximum_date, multi="min_max_date",
                 store=True, type='datetime', string='Max. Expected Date', select=2),
        'ref_order_tag_no': fields.related('ref_order_id', 'tag_no', type='text', relation='sale.order', string='TAG No. from Order', store=False, readonly=True),
        'tag_no': fields.text('TAG No.'),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        picking_obj = self.browse(cr, uid, id, context=context)
        if ('name' not in default) or (picking_obj.name == '/'):
            # For supply list
            if picking_obj.is_supply_list:
                default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.supplylist')
        res = super(stock_picking_out, self).copy(cr, uid, id, default=default, context=context)
        return res

    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name') == '/'):
            # For supply list
            seq_obj_name = vals.get('is_supply_list', False) and 'stock.picking.supplylist' or False
            if seq_obj_name:
                vals['name'] = self.pool.get('ir.sequence').get(cr, user, seq_obj_name)
        new_id = super(stock_picking_out, self).create(cr, user, vals, context)
        return new_id

stock_picking_out()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
