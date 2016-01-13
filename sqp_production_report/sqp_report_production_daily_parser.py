# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import jasper_reports

def sqp_report_production_daily_parser( cr, uid, ids, data, context ):
    return {
        'parameters': {
            'report_date': data['form']['report_date'],
            'dept': data['form']['dept'],
        },
   }

jasper_reports.report_jasper(
    'report.sqp_report_production_daily',
    'mrp.production',
    parser=sqp_report_production_daily_parser
)

jasper_reports.report_jasper(
    'report.sqp_report_production_daily_excel',
    'mrp.production',
    parser=sqp_report_production_daily_parser
)
