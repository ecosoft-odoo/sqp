# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import jasper_reports
from osv import osv,fields 
import pooler
import datetime

def sqp_report_thai_tax_parser( cr, uid, ids, data, context ):
    return {
        'parameters': {	
            'company_id': data['form']['company_id'],
            'period_id': data['form']['period_id'],
            'tax_id': data['form']['tax_id'],
            'base_code_id': data['form']['base_code_id'],
            'tax_code_id': data['form']['tax_code_id'],
            'type_tax_use': data['form']['type_tax_use'],
        },
   }

jasper_reports.report_jasper(
    'report.sqp_report_thai_tax',
    'account.move',
    parser=sqp_report_thai_tax_parser
)
