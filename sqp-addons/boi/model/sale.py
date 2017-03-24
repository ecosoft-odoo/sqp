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
        order_list = self.browse(cr, uid, ids)
        for order in order_list:
            quotation_type = order.product_tag_id and order.product_tag_id.name or False
            boi_type = quotation_type == 'BOI' and 'BOI' or 'NONBOI'
            line_ids = line_obj.search(cr, uid, [('order_id','=',order.id)])
            for line in line_obj.browse(cr, uid, line_ids):
                for tag in line.product_id.tag_ids:
                    if (boi_type == 'BOI' and tag.name != 'BOI') or (boi_type == 'NONBOI' and tag.name == 'BOI'):
                        return False
        return True

    _columns = {
        'boi_cert_id': fields.many2one('boi.certificate', 'BOI Number', ondelete="restrict"),
        'is_boi': fields.boolean('BOI', default=False),
        'ref_order_id': fields.many2one('sale.order', 'Ref BOI Quotation', ondelete="restrict"),
    }

    _constraints = [(_check_product_name, 'Please specific the correct product !', ['Product'])]

    def create(self, cr, uid, vals, context=None):
        order_id = super(sale_order, self).create(cr, uid, vals, context=context)
        if order_id:
            tag_obj = self.pool.get('product.tag')
            order = self.browse(cr, uid, order_id, context=context)
            product_tag_id = vals.get('product_tag_id', False)
            boi_type = False
            if product_tag_id:
                tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
                boi_type = tag.name == 'BOI' and 'BOI' or 'NONBOI'
            name = '%s-%s'%(boi_type,order.name)
            self.write(cr, uid, order_id, {'name': name}, context=context)
        return order_id

    def copy(self, cr, uid, id, default=None, context=None):
        order_id = super(sale_order, self).copy(cr, uid, id, default=default, context=context)
        if order_id:
            order = self.browse(cr, uid, order_id, context=context)
            name = order.name
            boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            name = (name.find('BOI') >= 0 and name.find('NONBOI') < 0 and boi_type == 'NONBOI') \
                        and name.replace('BOI','NONBOI') \
                        or (name.find('NONBOI') >= 0 and boi_type == 'BOI') \
                        and name.replace('NONBOI','BOI')  \
                        or name
            self.write(cr, uid, [order_id], {'name': name}, context=context)
        return order_id

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        product_tag_id = vals.get('product_tag_id', False)
        if product_tag_id:
            tag_obj = self.pool.get('product.tag')
            line_obj = self.pool.get('sale.order.line')
            product_obj = self.pool.get('product.product')
            tag = tag_obj.browse(cr, uid, product_tag_id, context=context)
            boi_type = (tag.id and tag.name == 'BOI') and 'BOI' or 'NONBOI'
            for order in self.browse(cr, uid, ids, context=context):
                vals['name'] = order.name
                vals['name'] = (vals['name'].find('BOI') >= 0 and vals['name'].find('NONBOI') < 0 and boi_type == 'NONBOI') \
                                    and vals['name'].replace('BOI','NONBOI') \
                                    or (vals['name'].find('NONBOI') >= 0 and boi_type == 'BOI') \
                                    and vals['name'].replace('NONBOI','BOI')  \
                                    or vals['name']
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    def action_wait(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                            and 'BOI' or 'NONBOI'
            name = '%s-%s'%(boi_type,order.name)
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

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        order_ids = self.search(cr, user, args, limit=limit, context=context)
        if context.get('ref_product_tag', False):
            tag_obj = self.pool.get('product.tag')
            tag_ids = tag_obj.search(cr, user, [('name','=',context.get('ref_product_tag'))], context=context)
            order_ids = self.search(cr, user, [('product_tag_id','in',tag_ids),('state','=','draft')] + args, limit=limit, context=context)
        return self.name_get(cr, user, order_ids, context=context)

    def _prepare_order_picking(self, cr, uid, order, context=None):
        result = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        boi_type = (order.product_tag_id and order.product_tag_id.name == 'BOI') \
                        and 'BOI' or 'NONBOI'
        boi_cert_id = order.boi_cert_id and order.boi_cert_id.id or False
        name = ''
        if result.get('name', False):
            name = '%s-%s'%(boi_type,result.get('name'))
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
