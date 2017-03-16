# -*- coding: utf-8 -*-
from osv import osv


class sale_order(osv.osv):
    _inherit = "sale.order"

    def _check_duplicate_product(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.state and obj.state == 'draft':
                product_ids = [x.product_id and x.product_id.id or False
                               for x in obj.order_line]
                dup_product_ids = \
                    list(set([x for x in product_ids
                             if (x and product_ids.count(x) > 1)]))
                if dup_product_ids:
                    return False
        return True

    _constraints = [
        (_check_duplicate_product,
         'Duplicate products is not allowed!',
         ['order_line.product_id']),
    ]


# class purchase_order(osv.osv):
#     _inherit = "purchase.order"
#
#     def _check_duplicate_product(self, cr, uid, ids, context=None):
#         for obj in self.browse(cr, uid, ids, context=context):
#             product_ids = [x.product_id and x.product_id.id or False
#                            for x in obj.order_line]
#             dup_product_ids = list(set([x for x in product_ids
#                                         if (x and product_ids.count(x) > 1)]))
#             if dup_product_ids:
#                 return False
#         return True
#
#     _constraints = [
#         (_check_duplicate_product,
#          'Duplicate products is not allowed!',
#          ['order_line']),
#     ]
#
#
# class account_invoice(osv.osv):
#     _inherit = "account.invoice"
#
#     def _check_duplicate_product(self, cr, uid, ids, context=None):
#         for obj in self.browse(cr, uid, ids, context=context):
#             product_ids = [x.product_id and x.product_id.id or False
#                            for x in obj.invoice_line]
#             dup_product_ids = list(set([x for x in product_ids
#                                         if (x and product_ids.count(x) > 1)]))
#             if dup_product_ids:
#                 return False
#         return True
#
#     _constraints = [
#         (_check_duplicate_product,
#          'Duplicate products is not allowed!',
#          ['invoice_line']),
#     ]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
