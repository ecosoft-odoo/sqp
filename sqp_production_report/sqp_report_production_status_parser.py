# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import jasper_reports

def sqp_report_production_status_parser( cr, uid, ids, data, context ):
    return {
        'parameters': {
            'partner_id': data['form']['partner_id'],
        },
   }

jasper_reports.report_jasper(
    'report.sqp_report_production_status',
    'mrp.production',
    parser=sqp_report_production_status_parser
)

jasper_reports.report_jasper(
    'report.sqp_report_production_status_excel',
    'mrp.production',
    parser=sqp_report_production_status_parser
)
