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
import time
from openerp.osv import fields, osv
from datetime import datetime
from dateutil.relativedelta import relativedelta

class sqp_report_production_daily(osv.osv_memory):

    _name = 'sqp.report.production.daily'

    _columns = {
        'date': fields.date('Date', required=True),
        'dept': fields.selection([('SF', 'Sheet Forming'),
                                    ('AS', 'Assembly'),
                                    ('IJ', 'Injection'),
                                    ('DO', 'Door'),
                                    ('FN', 'Finishing')], 'Department', required=True),
        'format': fields.selection([('pdf', 'PDF'),
                                    ('xls', 'Excel')], 'Format', required=True)
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'format': 'pdf',
    }

    def start_report(self, cr, uid, ids, data, context=None):
        for wiz_obj in self.read(cr, uid, ids):
            if 'form' not in data:
                data['form'] = {}
            data['form']['report_date'] = wiz_obj['date']
            data['form']['dept'] = wiz_obj['dept']
            if wiz_obj['format'] == 'xls':
                report_name = 'sqp_report_production_daily_excel'
            else:
                report_name = 'sqp_report_production_daily'
            return {
                'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data,
            }
    
sqp_report_production_daily()
