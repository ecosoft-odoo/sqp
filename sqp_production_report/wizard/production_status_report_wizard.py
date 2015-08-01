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

class sqp_report_production_status(osv.osv_memory):

    _name = 'sqp.report.production.status'

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', required=False),
        'format': fields.selection([('pdf', 'PDF'),
                                    ('xls', 'Excel')], 'Format', required=True)
    }
    _defaults = {
        'format': 'pdf',
    }

    def start_report(self, cr, uid, ids, data, context=None):
        for wiz_obj in self.read(cr, uid, ids):
            if 'form' not in data:
                data['form'] = {}
            data['form']['partner_id'] = wiz_obj['partner_id'] and wiz_obj['partner_id'][0] or -1  # -1 means all.
            if wiz_obj['format'] == 'xls':
                report_name = 'sqp_report_production_status_excel'
            else:
                report_name = 'sqp_report_production_status'
            return {
                'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data,
            }
    
sqp_report_production_status()
