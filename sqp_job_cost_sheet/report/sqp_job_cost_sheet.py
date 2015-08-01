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

from openerp import tools
from openerp.osv import fields, osv


class sqp_job_cost_sheet(osv.osv):

    _name = "sqp.job.cost.sheet"
    _description = "Job Cost Sheet"
    _auto = False

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, False)
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'mrp_main_rm_amount': 0.0,
                'mrp_rm_amount': 0.0,
                'labor_amount': 0.0,
                'transport_amount': 0.0,
                'electric_amount': 0.0,
                'supply_list_amount': 0.0,
                'subcontract_amount': 0.0,
                'commission_amount': 0.0,
                'expense_list_amount': 0.0,
                'plane_ticket_invoice_list_amount': 0.0,
                'comm_install_invoice_list_amount': 0.0,
                'other_invoice_list_amount': 0.0,
                'total_cost_amount': 0.0,
                'profit_amount': 0.0,
                'total_cost_percent': 0.0,
                'profit_percent': 0.0,
            }

            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_mrp_rm_list a 
                            join product_product b on b.id = a.product_id
                            where a.order_id = %s and b.main_material = %s""", (order.id, True))
            res[order.id]['mrp_main_rm_amount'] = cr.fetchone()[0] or 0.0    
            
            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_mrp_rm_list a 
                            join product_product b on b.id = a.product_id
                            where a.order_id = %s and b.main_material = %s""", (order.id, False))
            res[order.id]['mrp_rm_amount'] = cr.fetchone()[0] or 0.0         
            
            cr.execute("""select sum(amount) from sqp_job_book_labor
                            where order_id = %s""", (order.id,))
            res[order.id]['labor_amount'] = cr.fetchone()[0] or 0.0 
             
            cr.execute("""select sum(amount) from sqp_job_book_transport
                            where order_id = %s""", (order.id,))
            res[order.id]['transport_amount'] = cr.fetchone()[0] or 0.0 
            
            cr.execute("""select sum(amount) from sqp_job_book_electric
                            where order_id = %s""", (order.id,))
            res[order.id]['electric_amount'] = cr.fetchone()[0] or 0.0 
            
            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_supply_list
                            where order_id = %s""", (order.id,))
            res[order.id]['supply_list_amount'] = cr.fetchone()[0] or 0.0 
            
            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_po_subcontract
                            where order_id = %s""", (order.id,))
            res[order.id]['subcontract_amount'] = cr.fetchone()[0] or 0.0 

            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_expense_list
                            where order_id = %s""", (order.id,))
            res[order.id]['expense_list_amount'] = cr.fetchone()[0] or 0.0 
            
            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_invoice_list a 
                            join product_product b on b.id = a.product_id
                            where a.order_id = %s and b.job_cost_type = %s""", (order.id, 'plane_ticket'))
            res[order.id]['plane_ticket_invoice_list_amount'] = cr.fetchone()[0] or 0.0      

            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_invoice_list a 
                            join product_product b on b.id = a.product_id
                            where a.order_id = %s and b.job_cost_type = %s""", (order.id, 'comm_install'))
            res[order.id]['comm_install_invoice_list_amount'] = cr.fetchone()[0] or 0.0            

            cr.execute("""select sum(price_subtotal) from sqp_job_cost_sheet_invoice_list a 
                            join product_product b on b.id = a.product_id
                            where a.order_id = %s and b.job_cost_type is %s""", (order.id, None))
            res[order.id]['other_invoice_list_amount'] = cr.fetchone()[0] or 0.0    
            
            # Commisison Amount
            cwl_ids = self.pool.get('commission.worksheet.line').search(cr, uid, [('order_id', '=', order.id), ('commission_state', 'in', ('valid', 'done'))])
            for cwl in self.pool.get('commission.worksheet.line').read(cr, uid, cwl_ids, ['commission_amt']):
                res[order.id]['commission_amount'] = cwl['commission_amt']
                break
            # Finalize
            res[order.id]['total_cost_amount'] = res[order.id]['commission_amount'] + res[order.id]['mrp_main_rm_amount'] + res[order.id]['mrp_rm_amount'] \
                + res[order.id]['labor_amount'] + res[order.id]['transport_amount'] + res[order.id]['electric_amount'] \
                + res[order.id]['supply_list_amount'] + res[order.id]['subcontract_amount'] \
                + res[order.id]['expense_list_amount'] + res[order.id]['plane_ticket_invoice_list_amount'] \
                + res[order.id]['comm_install_invoice_list_amount'] + res[order.id]['other_invoice_list_amount']
            res[order.id]['profit_amount'] = order.amount_net - res[order.id]['total_cost_amount']
            res[order.id]['profit_percent'] = order.amount_net and (res[order.id]['profit_amount'] / order.amount_net) * 100 or 100
            res[order.id]['total_cost_percent'] = order.amount_net and (res[order.id]['total_cost_amount'] / order.amount_net) * 100 or 100
        return res

    def _search_amount(self, cr, uid, obj, name, args, query, context):
        ids = set()
        for cond in args:
            amount = cond[2]
            if isinstance(cond[2], (list, tuple)):
                if cond[1] in ['in', 'not in']:
                    amount = tuple(cond[2])
                else:
                    continue
            else:
                if cond[1] in ['=like', 'like', 'not like', 'ilike', 'not ilike', 'in', 'not in', 'child_of']:
                    continue
            cr.execute("select id from (" + query + ") a where a.amount %s %%s" % (cond[1]), (amount,))
            res_ids = set(id[0] for id in cr.fetchall())
            ids = ids and (ids & res_ids) or res_ids
        if ids:
            return [('id', 'in', tuple(ids))]
        return [('id', '=', '0')]

    # ============ SEARCH FUNCTIONS ============
    # main_material = True    
    QUERY_MAIN_RM_AMOUNT = """
            (select so.id, sum(case when coalesce(pp.main_material, false) = true then coalesce(rm.price_subtotal, 0.0) else 0 end) amount
                from sale_order so
                left outer join sqp_job_cost_sheet_mrp_rm_list rm on so.id = rm.order_id
                left outer join product_product pp on pp.id = rm.product_id
            group by so.id)
    """

    def _search_mrp_main_rm_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_MAIN_RM_AMOUNT, context=context)

    # main_material = False
    QUERY_RM_AMOUNT = """
            (select so.id, sum(case when coalesce(pp.main_material, false) = false then coalesce(rm.price_subtotal, 0.0) else 0 end) amount
                from sale_order so
                left outer join sqp_job_cost_sheet_mrp_rm_list rm on so.id = rm.order_id
                left outer join product_product pp on pp.id = rm.product_id
            group by so.id)
    """

    def _search_mrp_rm_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_RM_AMOUNT, context=context)

    QUERY_LABOR_AMOUNT = """
        (select so.id, sum(coalesce(labor.amount, 0)) amount
            from sale_order so
            left outer join sqp_job_book_labor labor on so.id = labor.order_id
        group by so.id)
    """

    def _search_labor_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_LABOR_AMOUNT, context=context)

    QUERY_TRANSPORT_AMOUNT = """
        (select so.id, sum(coalesce(transport.amount, 0)) amount
            from sale_order so
            left outer join sqp_job_book_transport transport on so.id = transport.order_id
        group by so.id)
    """

    def _search_transport_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_TRANSPORT_AMOUNT, context=context)

    QUERY_ELECTRIC_AMOUNT = """
        (select so.id, sum(coalesce(electric.amount, 0)) amount
            from sale_order so
            left outer join sqp_job_book_electric electric on so.id = electric.order_id
        group by so.id)
    """

    def _search_electric_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_ELECTRIC_AMOUNT, context=context)

    QUERY_SUPPLY_LIST_AMOUNT = """
        (select so.id, sum(coalesce(supply_list.price_subtotal, 0)) amount
            from sale_order so
            left outer join sqp_job_cost_sheet_supply_list supply_list on so.id = supply_list.order_id
        group by so.id)
    """

    def _search_supply_list_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_SUPPLY_LIST_AMOUNT, context=context)

    QUERY_SUBCONTRACT_AMOUNT = """
        (select so.id, sum(coalesce(po_subcontract.price_subtotal, 0)) amount
            from sale_order so
            left outer join sqp_job_cost_sheet_po_subcontract po_subcontract on so.id = po_subcontract.order_id
        group by so.id)
    """

    def _search_subcontract_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_SUBCONTRACT_AMOUNT, context=context)

    QUERY_EXPENSE_LIST_AMOUNT = """
        (select so.id, sum(coalesce(expense_list.price_subtotal, 0)) amount
            from sale_order so
            left outer join sqp_job_cost_sheet_expense_list expense_list on so.id = expense_list.order_id
        group by so.id)
    """

    def _search_expense_list_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_EXPENSE_LIST_AMOUNT, context=context)

    QUERY_PLANE_TICKET_AMOUNT = """
        (select so.id, sum(case when pp.job_cost_type = 'plane_ticket' then coalesce(invoice_list.price_subtotal, 0) else 0 end) amount
            from sale_order so
            join sqp_job_cost_sheet_invoice_list invoice_list on so.id = invoice_list.order_id
            join product_product pp on pp.id = invoice_list.product_id
        group by so.id)
    """

    def _search_plane_ticket_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_PLANE_TICKET_AMOUNT, context=context)

    QUERY_COMM_INSTALL_AMOUNT = """
        (select so.id, sum(case when pp.job_cost_type = 'comm_install' then coalesce(invoice_list.price_subtotal, 0) else 0 end) amount
            from sale_order so
            join sqp_job_cost_sheet_invoice_list invoice_list on so.id = invoice_list.order_id
            join product_product pp on pp.id = invoice_list.product_id
        group by so.id)
    """

    def _search_comm_install_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_COMM_INSTALL_AMOUNT, context=context)

    QUERY_OTHER_AMOUNT = """
        (select so.id, sum(case when pp.job_cost_type is null then coalesce(invoice_list.price_subtotal, 0) else 0 end) amount
            from sale_order so
            join sqp_job_cost_sheet_invoice_list invoice_list on so.id = invoice_list.order_id
            join product_product pp on pp.id = invoice_list.product_id
        group by so.id)
    """

    def _search_other_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_OTHER_AMOUNT, context=context)

    QUERY_COMMISSION_AMOUNT = """
        (select so.id, sum(coalesce(comm_line.commission_amt, 0)) amount
            from sale_order so
            left outer join commission_worksheet_line comm_line on so.id = comm_line.order_id
        group by so.id)
    """

    def _search_commission_amount(self, cr, uid, obj, name, args, context):
        return self._search_amount(cr, uid, obj, name, args, self.QUERY_COMMISSION_AMOUNT, context=context)

    QUERY_TOTAL_COST_AMOUNT = QUERY_MAIN_RM_AMOUNT + ' union ' \
        + QUERY_RM_AMOUNT + ' union ' \
        + QUERY_LABOR_AMOUNT + ' union ' \
        + QUERY_TRANSPORT_AMOUNT + ' union ' \
        + QUERY_ELECTRIC_AMOUNT + ' union ' \
        + QUERY_SUPPLY_LIST_AMOUNT + ' union ' \
        + QUERY_SUBCONTRACT_AMOUNT + ' union ' \
        + QUERY_EXPENSE_LIST_AMOUNT + ' union ' \
        + QUERY_PLANE_TICKET_AMOUNT + ' union ' \
        + QUERY_COMM_INSTALL_AMOUNT + ' union ' \
        + QUERY_OTHER_AMOUNT + ' union ' \
        + QUERY_COMMISSION_AMOUNT

    def _search_total_cost_amount(self, cr, uid, obj, name, args, context):
        QUERY = '(select id, sum(amount) amount from ( ' + self.QUERY_TOTAL_COST_AMOUNT + ' ) b group by id)'
        return self._search_amount(cr, uid, obj, name, args, QUERY, context=context)

    def _search_total_cost_percent(self, cr, uid, obj, name, args, context):
        QUERY = """(select c.id, case when coalesce(sale_order.amount_net, 0) = 0 then 100 else c.amount / sale_order.amount_net * 100 end amount
                from sale_order left outer join
                (select id, sum(amount) amount from ( """ + self.QUERY_TOTAL_COST_AMOUNT + """ ) b group by id) c on sale_order.id = c.id)"""
        return self._search_amount(cr, uid, obj, name, args, QUERY, context=context)

    def _search_profit_amount(self, cr, uid, obj, name, args, context):
        QUERY = """(select c.id, sale_order.amount_net - c.amount amount
                from sale_order left outer join
                (select id, sum(amount) amount from ( """ + self.QUERY_TOTAL_COST_AMOUNT + """ ) b group by id) c on sale_order.id = c.id)"""
        return self._search_amount(cr, uid, obj, name, args, QUERY, context=context)

    def _search_profit_percent(self, cr, uid, obj, name, args, context):
        QUERY = """(select c.id, case when coalesce(sale_order.amount_net, 0) = 0 then 100 else (sale_order.amount_net - c.amount) / sale_order.amount_net * 100 end amount
                from sale_order left outer join
                (select id, sum(amount) amount from ( """ + self.QUERY_TOTAL_COST_AMOUNT + """ ) b group by id) c on sale_order.id = c.id)"""
        print QUERY
        return self._search_amount(cr, uid, obj, name, args, QUERY, context=context)

    def _area_so(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for sheet in self.browse(cursor, user, ids, context=context):
            area = sheet.order_id.area_so
#             for line in sheet.order_id.order_line:
#                 if line.product_uom and line.product_uom.name.lower() == 'sqm':
#                     area += line.product_uom_qty
            res[sheet.id] = area
        return res
    
    def _area_mo(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for sheet in self.browse(cursor, user, ids, context=context):
            area = 0.0
            for mo in sheet.order_id.ref_mo_ids:
                for line in mo.product_lines:
                    area += (line.L/1000 * line.W/1000) - line.cut_area
            res[sheet.id] = area
        return res

    _columns = {
        'name': fields.char('Name', readonly=True),
        'order_id': fields.many2one('sale.order', 'Sales Order', readonly=True),
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
        ], 'Status', readonly=True),
        'ref_project_name': fields.char('Ref Project Name', readonly=True),
        'product_tag_id': fields.many2one('product.tag', 'Product Tag', readonly=True),
        'user_id': fields.many2one('res.users', 'Salesperson', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'month': fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                                   ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
                                   ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'add_disc': fields.float('Final Discount (%)', readonly=True),
        'amount_net': fields.float('Final Order Amount', readonly=True),
        'mrp_main_rm_amount': fields.function(_amount_all, string='Material', multi="sums", fnct_search=_search_mrp_main_rm_amount),
        'mrp_rm_amount': fields.function(_amount_all, string='Supply', multi="sums", fnct_search=_search_mrp_rm_amount),
        'labor_amount': fields.function(_amount_all, string='Labor', multi="sums", fnct_search=_search_labor_amount),
        'transport_amount': fields.function(_amount_all, string='Transport', multi="sums", fnct_search=_search_transport_amount),
        'electric_amount': fields.function(_amount_all, string='Electric', multi="sums", fnct_search=_search_electric_amount),
        'supply_list_amount': fields.function(_amount_all, string='Supply List', multi="sums", fnct_search=_search_supply_list_amount),
        'subcontract_amount': fields.function(_amount_all, string='Subcontract', multi="sums", fnct_search=_search_subcontract_amount),
        'commission_amount': fields.function(_amount_all, string='Sales Commission', multi="sums", fnct_search=_search_commission_amount),
        'expense_list_amount': fields.function(_amount_all, string='Expenses', multi="sums", fnct_search=_search_expense_list_amount),
        'plane_ticket_invoice_list_amount': fields.function(_amount_all, string='Plane Ticket', multi="sums", fnct_search=_search_plane_ticket_amount),
        'comm_install_invoice_list_amount': fields.function(_amount_all, string='Commission / Installation', multi="sums", fnct_search=_search_comm_install_amount),
        'other_invoice_list_amount': fields.function(_amount_all, string='Others', multi="sums", fnct_search=_search_other_amount),
        'total_cost_amount': fields.function(_amount_all, string='Total Cost', multi="sums", fnct_search=_search_total_cost_amount),
        'total_cost_percent': fields.function(_amount_all, string='Percent Total Cost', multi="sums", fnct_search=_search_total_cost_percent),
        'profit_amount': fields.function(_amount_all, string='Profit Amount', multi="sums", fnct_search=_search_profit_amount),
        'profit_percent': fields.function(_amount_all, string='Percent Profit', multi="sums", fnct_search=_search_profit_percent),
        # Tabs
        'order_line': fields.one2many('sqp.job.cost.sheet.order.line', 'order_id', 'Order Lines', readonly=True),
        'mrp_main_rm_list': fields.one2many('sqp.job.cost.sheet.mrp.rm.list', 'order_id', 'Main Material', domain=[('product_id.main_material', '=', 'True')], readonly=True),
        'mrp_rm_list': fields.one2many('sqp.job.cost.sheet.mrp.rm.list', 'order_id', 'Supply Material', domain=[('product_id.main_material', '!=', 'True')], readonly=True),
        'labor_list': fields.one2many('sqp.job.book.labor', 'order_id', 'Labor List', readonly=True),
        'transport_list': fields.one2many('sqp.job.book.transport', 'order_id', 'Transport List', readonly=True),
        'electric_list': fields.one2many('sqp.job.book.electric', 'order_id', 'Electric List', readonly=True),
        'supply_list': fields.one2many('sqp.job.cost.sheet.supply.list', 'order_id', 'Supply List', readonly=True),
        'po_subcontract': fields.one2many('sqp.job.cost.sheet.po.subcontract', 'order_id', 'PO Subcontract', readonly=True),
        'expense_list': fields.one2many('sqp.job.cost.sheet.expense.list', 'order_id', 'Expense', readonly=True),
        'plane_ticket_invoice_list': fields.one2many('sqp.job.cost.sheet.invoice.list', 'order_id', 'Plane Ticket', domain=[('product_id.job_cost_type', '=', 'plane_ticket')], readonly=True),
        'comm_install_invoice_list': fields.one2many('sqp.job.cost.sheet.invoice.list', 'order_id', 'Commission / Installation', domain=[('product_id.job_cost_type', '=', 'comm_install')], readonly=True),
        'other_invoice_list': fields.one2many('sqp.job.cost.sheet.invoice.list', 'order_id', 'Others', domain=[('product_id.job_cost_type', '=', False)], readonly=True),
        'area_so': fields.function(_area_so, string='Area (sqm) from SO', help="From sales order line with UoM = 'sqm' only"),
        'area_mo': fields.function(_area_mo, string='Area (sqm) from MO', help="From manufacturing order's product line with formula L/1000 * W/1000 - cut_area")
    }
    _order = 'date'

    def init(self, cr):
        # Order
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select sub.id, sub.order_id, sub.state, sub.name, sub.ref_project_name, sub.product_tag_id,
            sub.user_id, sub.partner_id, sub.date, sub.year, sub.month, sub.day, sub.add_disc,
            case when curr.type_ref_base = 'smaller' then
                sub.amount_net / cr.rate_sell else sub.amount_net * cr.rate_sell
            end AS amount_net
            from
            (select so.id as id,
                so.id as order_id,
                price.currency_id,
                so.state,
                so.name,
                so.ref_project_name,
                so.product_tag_id,
                so.user_id,
                so.partner_id,
                so.date_order as date,
                to_char(so.date_order::timestamp with time zone, 'YYYY'::text) AS year,
                to_char(so.date_order::timestamp with time zone, 'MM'::text) AS month,
                to_char(so.date_order::timestamp with time zone, 'YYYY-MM-DD'::text) AS day,
                so.add_disc,
                case when coalesce(so.amount_final, 0) = 0 then so.amount_net else so.amount_final end as amount_net
            from
            sale_order so join product_pricelist price on so.pricelist_id = price.id
            where so.state not in ('draft', 'cancel')) sub
            -- currency
            JOIN res_currency_rate cr ON cr.currency_id = sub.currency_id
            JOIN res_currency curr ON curr.id = cr.currency_id
              WHERE cr.id IN (
            SELECT cr2.id
               FROM res_currency_rate cr2
              WHERE cr2.currency_id = sub.currency_id AND (sub.date IS NOT NULL AND cr2.name <= sub.date OR  sub.date IS NULL AND cr2.name <= now())
              ORDER BY name DESC LIMIT 1)
        )""" % (self._table,))

sqp_job_cost_sheet()


class sqp_job_cost_sheet_order_line(osv.osv):

    _name = "sqp.job.cost.sheet.order.line"
    _description = "Job Cost Sheet's Order Line"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of sales order lines."),
        'product_id': fields.many2one('product.product', 'Product'),
        'name': fields.text('Description'),
        'product_uom_qty': fields.float('Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'discount': fields.float('Discount (%)'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'sequence'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select id, sequence, order_id, product_id, name, product_uom_qty, product_uom, price_unit, discount,
            (product_uom_qty * price_unit) * (1-discount/100) as price_subtotal
            from sale_order_line
            order by order_id, sequence
        )""" % (self._table,))

sqp_job_cost_sheet_order_line()


class sqp_job_cost_sheet_mrp_rm_list(osv.osv):

    _name = "sqp.job.cost.sheet.mrp.rm.list"
    _description = "Job Cost Sheet's Raw Material List"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'product_id': fields.many2one('product.product', 'Product'),
        'product_code': fields.char('Product Code'),
        'planned_qty': fields.float('Planned Quantity'),
        'actual_qty': fields.float('Actual Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'product_code'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select min(id) id, order_id, product_id, product_code, product_uom, sum(planned_qty) planned_qty, sum(actual_qty) actual_qty, avg(price_unit) price_unit, sum(price_subtotal) price_subtotal
            from (
                  select a.id, a.order_id, a.product_id, pp.default_code product_code, a.product_uom, a.planned_qty, a.actual_qty, (pt.standard_price * uom.factor) as price_unit, (pt.standard_price * uom.factor * a.actual_qty) price_subtotal
                  from (select id, x.order_id, x.product_id, product_uom, planned_qty, actual_qty from
                  (select plan.id, plan.order_id, plan.product_id, plan.product_uom, plan.planned_qty, actual.actual_qty from
                    -- Planned
                    (select mrp.order_id, mpl.product_id, mpl.product_uom, min(mpl.id) as id, sum(mpl.product_qty) as planned_qty
                    from mrp_production_product_line mpl
                    join mrp_production mrp on mrp.id = mpl.production_id
                    and mrp.state = 'done' and mrp.parent_id is not null
                    group by mrp.order_id, mpl.product_id, mpl.product_uom) plan
                    join
                    -- Actual
                    (select mrp.order_id, sm.product_id, sum(coalesce(sm.product_qty, 0.0)) as actual_qty from stock_move sm
                    join mrp_production_move_ids rel on rel.move_id = sm.id and sm.state = 'done'
                    join mrp_production mrp on mrp.id = rel.production_id
                    and mrp.state = 'done' and mrp.parent_id is not null
                    group by  mrp.order_id, sm.product_id) actual
                    on actual.product_id = plan.product_id and actual.order_id = plan.order_id) x
                    -- Not include those in internal move
                            left join (select sp.ref_order_id, product_id
                            from stock_picking sp
                            join stock_move sm on sm.picking_id = sp.id
                            where sp.type = 'internal' and sp.state = 'done' and sp.ref_order_id is not null) y
                            on x.order_id = y.ref_order_id and x.product_id = y.product_id
                            where y.ref_order_id is null and y.product_id is null
                            -- Union Internal Move
                            --- (It might be possible also for internal move to join with planned, to get the planned amount.
                            ---  But it might cause even more performance drop)
                            union
                            (select sm.id, sp.ref_order_id order_id, product_id, product_uom, 0 as planned_qty, product_qty actual_qty
                            from stock_picking sp
                            join stock_move sm on sm.picking_id = sp.id
                            where sp.type = 'internal' and sp.state = 'done' and sp.ref_order_id is not null)) a
                          join product_uom uom on uom.id = a.product_uom
                          join product_product pp on pp.id = a.product_id
                          join product_template pt on pt.id = pp.product_tmpl_id
                          order by pp.default_code) b
                        group by order_id, product_id, product_code, product_uom
        )""" % (self._table,))

sqp_job_cost_sheet_mrp_rm_list()


class sqp_job_cost_sheet_supply_list(osv.osv):

    _name = "sqp.job.cost.sheet.supply.list"
    _description = "Job Cost Sheet's Supply List"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'supply_list_id': fields.many2one('stock.picking', 'Supply List'),
        'product_id': fields.many2one('product.product', 'Product'),
        'product_code': fields.char('Product Code'),
        'planned_qty': fields.float('Planned Quantity'),
        'actual_qty': fields.float('Actual Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'product_code'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select min(id) id, supply_list_id, order_id, product_id, product_code, product_uom, sum(planned_qty) planned_qty, sum(actual_qty) actual_qty, avg(price_unit) price_unit, sum(price_subtotal) price_subtotal
            from (
                  select a.id, a.supply_list_id, a.order_id, a.product_id, pp.default_code as product_code, a.product_uom, a.planned_qty, a.actual_qty, (pt.standard_price * uom.factor) as price_unit, (pt.standard_price * uom.factor * a.actual_qty) price_subtotal
                  from (select sm.id, sp.id as supply_list_id, sp.ref_order_id as order_id, sm.product_id, sm.product_uom,
                      case when type='out' then sm.order_qty else 0.0 end as planned_qty,
                      case when type='out' then sm.product_qty else -sm.product_qty end as actual_qty from stock_picking sp
                      join stock_move sm on sm.picking_id = sp.id
                      where sp.is_supply_list = True
                      and sp.state = 'done') a
                  join product_uom uom on uom.id = a.product_uom
                  join product_product pp on pp.id = a.product_id
                  join product_template pt on pt.id = pp.product_tmpl_id
                  order by pp.default_code) b
                group by supply_list_id, order_id, product_id, product_code, product_uom
        )""" % (self._table,))

sqp_job_cost_sheet_supply_list()


class sqp_job_cost_sheet_po_subcontract(osv.osv):

    _name = "sqp.job.cost.sheet.po.subcontract"
    _description = "Job Cost Sheet's PO Subcontract"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'purchase_id': fields.many2one('purchase.order', 'Purchase Order'),
        'invoice_id': fields.many2one('account.invoice', 'Supplier Invoice'),
        'product_id': fields.many2one('product.product', 'Product'),
        'name': fields.text('Description'),
        'product_qty': fields.float('Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'id'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select sub.id, purchase_id, invoice_id, product_id, sub.name, order_id, product_qty, product_uom,
                case when curr.type_ref_base = 'smaller' then
                    sub.price_unit / (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                    else
                    sub.price_unit * (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                end AS price_unit,
                case when curr.type_ref_base = 'smaller' then
                    sub.price_subtotal / (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                    else
                    sub.price_subtotal * (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                end AS price_subtotal
            from
            (select ai.type, ai.date_invoice, ai.currency_id, ail.id,  po.id as purchase_id, ail.invoice_id, po.ref_order_id as order_id, ail.product_id, ail.name,
                case when ai.type = 'in_invoice' then ail.quantity else -ail.quantity end as product_qty,
                ail.uos_id product_uom, ail.price_unit,
                case when ai.type = 'in_invoice' then price_subtotal else -price_subtotal end as price_subtotal
            from account_invoice ai
            join (select purchase_id purchase_id, invoice_id from purchase_invoice_rel) pil 
            on pil.invoice_id = ai.id
            join purchase_order po on po.id = pil.purchase_id and po.is_subcontract = True and po.ref_order_id is not null
            join account_invoice_line ail on ail.invoice_id = ai.id
            where ai.state not in ('draft', 'cancel') and ai.type in ('in_invoice', 'in_refund')) sub
            -- currency
            JOIN res_currency_rate cr ON cr.currency_id = sub.currency_id
            JOIN res_currency curr ON curr.id = cr.currency_id
              WHERE cr.id IN (
            SELECT cr2.id
               FROM res_currency_rate cr2
              WHERE cr2.currency_id = sub.currency_id AND (sub.date_invoice IS NOT NULL AND cr2.name <= sub.date_invoice OR  sub.date_invoice IS NULL AND cr2.name <= now())
              ORDER BY name DESC LIMIT 1)
        )""" % (self._table,))

sqp_job_cost_sheet_po_subcontract()


class sqp_job_cost_sheet_inovice_list(osv.osv):

    _name = "sqp.job.cost.sheet.invoice.list"
    _description = "Job Cost Sheet's Supplier Invoice"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'invoice_id': fields.many2one('account.invoice', 'Supplier Invoice'),
        'account_id': fields.many2one('account.account', 'Account'),
        'product_id': fields.many2one('product.product', 'Product'),
        'name': fields.text('Description'),
        'product_qty': fields.float('Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'id'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select * from (
            select sub.id, account_id, invoice_id, product_id, sub.name, order_id, product_qty, product_uom,
                case when curr.type_ref_base = 'smaller' then
                    sub.price_unit / (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                    else
                    sub.price_unit * (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                end AS price_unit,
                case when curr.type_ref_base = 'smaller' then
                    sub.price_subtotal / (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                    else
                    sub.price_subtotal * (case when sub.type in ('in_invoice', 'in_refund') then cr.rate else cr.rate_sell end)
                end AS price_subtotal
            from
            (select ai.type, ai.date_invoice, ai.currency_id, ail.id, ail.invoice_id, ail.account_id, ail.product_id, ail.name, inv_so.order_id,
                case when ai.type = 'in_invoice' then ail.quantity else -ail.quantity end as product_qty,
                ail.uos_id product_uom, ail.price_unit,
                case when ai.type = 'in_invoice' then price_subtotal else -price_subtotal end as price_subtotal
            from account_invoice ai
            join account_invoice_line ail on ail.invoice_id = ai.id
            join     (select invoice_id, order_id from (
                -- Invoice with Reference to PO (non-Subcontract)
                (select pil.invoice_id, po.ref_order_id as order_id from purchase_order po
                join (select purchase_id, invoice_id from purchase_invoice_rel) pil 
                        on po.id = pil.purchase_id
                where po.is_subcontract = False and po.ref_order_id is not null)
                union -- Invoice with direct reference to PO
                (select ai.id as invoice_id, ai.cost_order_id as order_id from account_invoice ai
                where ai.cost_order_id is not null)) base_inv_so) inv_so on inv_so.invoice_id = ai.id
            where ai.state not in ('draft', 'cancel') and ai.type in ('in_invoice', 'in_refund')) sub
            -- currency
            JOIN res_currency_rate cr ON cr.currency_id = sub.currency_id
            JOIN res_currency curr ON curr.id = cr.currency_id
              WHERE cr.id IN (
            SELECT cr2.id
               FROM res_currency_rate cr2
              WHERE cr2.currency_id = sub.currency_id AND (sub.date_invoice IS NOT NULL AND cr2.name <= sub.date_invoice OR  sub.date_invoice IS NULL AND cr2.name <= now())
              ORDER BY name DESC LIMIT 1)
              -- also exclude those in Supply List
              ) a where a.product_id not in (select product_id from sqp_job_cost_sheet_supply_list b where b.product_id = a.product_id and b.order_id = a.order_id)
        )""" % (self._table,))

sqp_job_cost_sheet_inovice_list()


class sqp_job_cost_sheet_expense_list(osv.osv):

    _name = "sqp.job.cost.sheet.expense.list"
    _description = "Job Cost Sheet's Expenses"
    _auto = False

    _columns = {
        'order_id': fields.many2one('sqp.job.cost.sheet', 'Sales Order'),
        'expense_id': fields.many2one('hr.expense.expense', 'Expense'),
        'product_id': fields.many2one('product.product', 'Product'),
        'name': fields.text('Description'),
        'product_qty': fields.float('Quantity'),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'price_unit': fields.float('Unit Price'),
        'price_subtotal': fields.float('Sub Total'),
    }
    _order = 'id'

    def init(self, cr):
        # Order Lines
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select sub.id, sub.expense_id, sub.product_id, sub.name, sub.order_id, sub.unit_quantity product_qty, sub.uom_id product_uom,
                case when curr.type_ref_base = 'smaller' then
                    sub.unit_amount / cr.rate
                    else
                    sub.unit_amount * cr.rate
                end AS price_unit,
                case when curr.type_ref_base = 'smaller' then
                    sub.price_subtotal / cr.rate
                    else
                    sub.price_subtotal * cr.rate
                end AS price_subtotal
            from (select x.date, x.currency_id, xl.id, expense_id, product_id, xl.name, cost_order_id as order_id, unit_quantity,
                uom_id, unit_amount, unit_quantity*unit_amount as price_subtotal
            from hr_expense_line xl
            join hr_expense_expense x on xl.expense_id = x.id
            where xl.cost_order_id is not null) sub
            -- currency
            JOIN res_currency_rate cr ON cr.currency_id = sub.currency_id
            JOIN res_currency curr ON curr.id = cr.currency_id
              WHERE cr.id IN (
            SELECT cr2.id
               FROM res_currency_rate cr2
              WHERE cr2.currency_id = sub.currency_id AND (sub.date IS NOT NULL AND cr2.name <= sub.date OR  sub.date IS NULL AND cr2.name <= now())
              ORDER BY name DESC LIMIT 1)
        )""" % (self._table,))

sqp_job_cost_sheet_expense_list()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
