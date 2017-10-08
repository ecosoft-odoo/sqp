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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from . import constant

class sale_order(osv.osv):

    _inherit = 'sale.order'

    def _check_product_name(self, cr, uid, ids):
        line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids):
            product_tag_name = order.product_tag_id and order.product_tag_id.name or False
            line_ids = line_obj.search(cr, uid, [('order_id', '=', order.id)])
            for line in line_obj.browse(cr, uid, line_ids):
                for tag in line.product_id.tag_ids:
                    if product_tag_name and ((product_tag_name == 'BOI' and tag.name != 'BOI') or (product_tag_name != 'BOI' and tag.name == 'BOI')):
                        return False
        return True

    _columns = {
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict", domain="[('start_date','!=',False),('active','!=',False)]"),
        'is_boi': fields.boolean('BOI', default=False),
        'ref_order_id': fields.many2one('sale.order', 'Ref BOI Quotation', ondelete="restrict", domain="[('product_tag_id.name','=','BOI'), ('state','not in',('cancel'))]"),
    }

    _constraints = [
        (_check_product_name, 'Please specific the correct product !', ['product_tag_id']),
    ]

    def create(self, cr, uid, vals, context=None):
        order_id = super(sale_order, self).create(cr, uid, vals, context=context)
        if order_id:
            order = self.browse(cr, uid, order_id, context=context)

            # Update name
            if order.product_tag_id and order.product_tag_id.name == 'BOI':
                boi_cert_name = order.boi_cert_id and order.boi_cert_id.name or 'BOI'
                name = '%s-%s'%(boi_cert_name, order.name[order.name.find('-') + 1:])
                self.write(cr, uid, [order_id], {'name': name}, context=context)
        return order_id

    def write(self, cr, uid, ids, vals, context=None):
        product_tag_id = vals.get('product_tag_id', False)
        boi_cert_id = vals.get('boi_cert_id', False)
        if product_tag_id or boi_cert_id:
            tag_obj = self.pool.get('product.tag')
            cert_obj = self.pool.get('boi.certificate')

            tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
            cert = cert_obj.browse(cr, uid, boi_cert_id, context=context)

            # Update name
            for order in self.browse(cr, uid, ids, context=context):
                vals['name'] = (tag.id and tag.name == 'BOI') and '%s-%s'%(cert.name, order.name[order.name.find('-') + 1:]) \
                                    or (tag.id and tag.name != 'BOI') and order.name[order.name.find('-') + 1:] \
                                    or (not tag.id and cert.id) and '%s-%s'%(cert.name, order.name[order.name.find('-') + 1:]) \
                                    or order.name
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    def action_wait(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            if order.product_tag_id and order.product_tag_id.name == 'BOI':
                boi_cert_name = order.boi_cert_id and order.boi_cert_id.name or 'BOI'
                name = '%s-%s'%(boi_cert_name, order.name[order.name.find('-') + 1:])
                self.write(cr, uid, [order.id], {'name': name}, context=context)
        return super(sale_order, self).action_wait(cr, uid, ids, context=context)

    def onchange_product_tag_id(self, cr, uid, ids, product_tag_id, context=None):
        is_boi = False
        header_msg = False
        tag_obj = self.pool.get('product.tag')
        if product_tag_id:
            tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
            is_boi = tag.name == 'BOI' and True or False
            header_msg = tag.name == 'BOI' and constant.boi_header_msg or constant.nonboi_header_msg
        return {'value': {'is_boi': is_boi, 'boi_cert_id': False, 'header_msg': header_msg}}

    def _prepare_order_picking(self, cr, uid, order, context=None):
        result = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        boi_cert_id = False
        boi_cert_name = False
        boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                        and 'BOI' or 'NONBOI'

        # Set BOI Number
        if order.boi_cert_id:
            boi_cert_id = order.boi_cert_id.id
            boi_cert_name = order.boi_cert_id.name

        # Update name
        name = result.get('name', False)
        if name:
            name = boi_type == 'BOI' and '%s-%s'%(boi_cert_name, name[name.find('-') + 1:]) or name
        result.update({'boi_type': boi_type, 'boi_cert_id': boi_cert_id, 'name': name})
        return result

sale_order()


class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        if context.get('product_tag_id', False):
            tag_obj = self.pool.get('product.tag')
            product_obj = self.pool.get('product.product')
            tag = tag_obj.browse(cr, uid, context.get('product_tag_id'), context=context)
            if (tag.name == 'BOI' or tag.name == 'Standard Product') and product:
                product = product_obj.browse(cr, uid, product, context=context)
                product_uom = product.uom_id and product.uom_id.id or False
                result['value'].update({'product_uom': product_uom})
        return result

    def button_confirm(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        product_obj = self.pool.get('product.product')
        for line in self.browse(cr, uid, ids, context=context):
            order_id = line.order_id.id
            order = order_obj.browse(cr, uid, order_id, context=context)
            if order.product_tag_id and (order.product_tag_id.name == 'Standard Product' or order.product_tag_id.name == 'BOI'):
                product = product_obj.browse(cr, uid, line.product_id.id, context=context)
                if line.product_uom.id != product.uom_id.id:
                    raise osv.except_osv(_('Error!'), _('Unit of Measure of product %s must be %s'%(line.product_id.name_template, product.uom_id.name)))
        return super(sale_order_line, self).button_confirm(cr, uid, ids, context=context)
