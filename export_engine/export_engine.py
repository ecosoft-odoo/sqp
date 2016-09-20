# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Author: Naresh Soni
#    Copyright 2016 Cozy Business Solutions Pvt.Ltd
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
import xlwt
import re
import types
from datetime import datetime
from openerp.osv import fields, osv


class export_config(osv.osv):
    _name = 'export.config'

    _columns = {

    'name': fields.char('Name', translate=True, required=True),
    'model_id' : fields.many2one('ir.model', 'Model', required=True, domain=[('osv_memory','=',False)]),
    # 'field_ids': fields.many2many('ir.model.fields','model_field_rel', 'model_id', 'field_id', string='Fields'),
    'field_ids': fields.one2many('export.column', 'config_id', string='Fields'),
    'start_export_on': fields.datetime('Launch Export on', help="Date on which records needs to be exported."),
    'last_exported_on': fields.datetime('Last Exported on', readonly=True, select=True, help="Date on which last export was done."),
    'exported': fields.boolean('Exported ?'),
    'allow_to_export_updated_rec': fields.boolean('Allow to Export Updated records ?'),
    'export_sequence': fields.integer('Export Sequence', help="Export will be done in this order. Lower the number, higher the priority."),
    'exported_ids': fields.one2many('export.ids', 'config_id', 'Exported Records'),
    'search_domain':fields.char('Domain'),
    'limit_rec': fields.integer('Limit', help="Limit your records"),
    'order_by_field' : fields.many2one('ir.model.fields','Order BY',domain="[('model_id','=',model_id)]",help="Sort order by Field. default by ID Ascending"),
    'offset': fields.integer('Offset'),
    'domain_lines': fields.one2many('domain.line','export_cofig_id', 'Domain',help="Record Filters !"),
    'custom_labels': fields.one2many('custom.label','export_cofig_id', 'Custom Labels',help="Custom Field Labels to be shown !"),
    }


    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
        default = default.copy()
        default['exported_ids'] = []
        default['start_export_on'] = False
        default['last_exported_on'] = False
        default['exported'] = False
        return super(export_config, self).copy(cr, uid, id, default, context=context)

    def onchange_exported(self, cr, uid, ids, exported, context=None):
        res = {}
        res['value'] = {'last_exported_on':False}
        if exported:
            res['value'] = {'last_exported_on':datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        return res

    def onchange_model(self, cr, uid, ids, context=None):
        res = {}
        res['value'] = {'field_ids':[]}
        return res

    def init_excel(self):
        workbook = xlwt.Workbook()
        data_style = xlwt.easyxf('font: name Times New Roman,bold off, italic off; align: wrap yes')
        return workbook, data_style

    def export_headers(self, workbook, title, headers):
        title_style = xlwt.easyxf('font: name Times New Roman,bold on, italic on')
        al = xlwt.Alignment()
        al.horz = xlwt.Alignment.HORZ_CENTER
        title_style.alignment = al

        sheet = workbook.add_sheet('Exported-%s'%(title))
        sheet.row(0).height = 256*3
        # sheet.write(row, col, title, main_title_style)
        row = 0
        col = 0
        for i, fieldname in enumerate(headers):
            sheet.write(row, col, fieldname, title_style)
            sheet.col(i).width = 8000
            col += 1
        return sheet

    def export_data(self, sheet, rows, style):
        row = 1
        col = 0
        for data in rows:
            for cell_value in data:
                if isinstance(cell_value, basestring):
                    cell_value = re.sub("\r", " ", cell_value)
                if cell_value is False: cell_value = None
                sheet.write(row, col, cell_value, style)
                col += 1
            row += 1
            col = 0
        return True

    def get_domain(self, record):
        domain = []
        for line in record.domain_lines:
            val = str(line.value) or False
            if val in ('false','False'):
                val = False
            if val in ('true','True'):
                val  = True
            domain.append((line.field_name.name, line.operator, val))
        for export_row in record.exported_ids:
            exported_ids = \
                [int(x) for x in export_row.name.replace(" ", "").split(",")]
            domain.append(('id', 'not in', exported_ids))
        return domain

    def get_unique_records(self, record, data):
        unique_records = []
        exported = []
        for rec in record.exported_ids:
            exported += rec.name.split(',')
        exported = map(lambda x:int(x),exported)
        if not len(exported): return data
        for export_id in data:
            if export_id not in list(set(exported)):
                unique_records.append(export_id)
        return unique_records

    def start_export(self, cr, uid, ids, *args):
        for rec in self.browse(cr, uid, ids):
            if rec.exported and not rec.allow_to_export_updated_rec: continue
            fields_to_export = []
            fields_title = []
            custom_labels = {}
            workbook, data_style = self.init_excel()
            for custom_label in rec.custom_labels:
                custom_labels.update({custom_label.field_name.id:custom_label.value})
            for column in rec.field_ids:
                field = column.field_id
                if field.ttype in ('one2many','many2many'):
                    child_fields = self.pool.get(field.relation).fields_view_get(cr, uid, view_type='tree')['fields']
                    for child in child_fields.keys():
                        fields_to_export.append(field.name+'/'+child)
                        if field.id in custom_labels:
                            fields_title.append(custom_labels[field.id]+'/'+child_fields[child]['string'])
                        else:
                            fields_title.append(field.field_description+'/'+child_fields[child]['string'])
                else:
                    fields_to_export.append(field.name)
                    if field.id in custom_labels:
                        fields_title.append(custom_labels[field.id])
                    else:
                        fields_title.append(field.field_description)
            domain = self.get_domain(rec)
            if rec.allow_to_export_updated_rec:
                domain.append(('write_date','>=',rec.last_exported_on))
            order = rec.order_by_field and rec.order_by_field.name or None
            sheet = self.export_headers(workbook, rec.name, fields_title)
            print '----------------'
            print domain
            print '----------------'
            rec_to_export = self.pool.get(rec.model_id.model).search(cr, uid, domain, offset=rec.offset, limit=rec.limit_rec or None, order=order)
            print rec_to_export
            unique_records = rec_to_export
            if not rec.allow_to_export_updated_rec:
                unique_records = self.get_unique_records(rec, rec_to_export)
            if not len(unique_records):continue
            result = self.pool.get(rec.model_id.model).export_data(cr, uid, unique_records, fields_to_export).get('datas',[])
            self.export_data(sheet, result, data_style)
            export_path = self.pool.get('ir.config_parameter').get_param(cr, uid, 'export_path')
            last_exported_on = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            workbook.save(export_path+'/'+rec.name+'_'+last_exported_on+'.xls')
            self.log_export(cr, uid, rec, unique_records, last_exported_on)
        return True

    def log_export(self, cr, uid, rec, exported_records, last_exported_on):
        vals = {'exported':True,'last_exported_on':last_exported_on}
        if len(exported_records):
             vals.update({
                         'exported_ids':[(0, 0,  {'model_id':rec.model_id.id,
                                                     'config_id':rec.id,
                                                     'last_logged_on':last_exported_on,
                                                     'name':', '.join(str(x) for x in exported_records)})]})
        self.write(cr, uid, rec.id, vals)
        return True

    def launch_export(self, cr, uid, context=None):
        search_domain = [('start_export_on', '<=', datetime.today().strftime('%Y-%m-%d %H:%M:00')),
                         '|',('exported','=', False),('allow_to_export_updated_rec','=',True)]
        records = self.search(cr, uid, search_domain, order='export_sequence asc')
        if records:
            self.start_export(cr, uid, records)
        return True

export_config()


class export_column(osv.osv):
    _name = 'export.column'
    _order = 'sequence, id'

    def _get_fields_type(self, cr, uid, context=None):
        # Avoid too many nested `if`s below, as RedHat's Python 2.6
        # break on it. See bug 939653.
        return sorted([(k, k) for k, v in fields.__dict__.iteritems()
                          if type(v) == types.TypeType and \
                             issubclass(v, fields._column) and \
                             v != fields._column and \
                             not v._deprecated and \
                             not issubclass(v, fields.function)])

    _columns = {
        'config_id': fields.many2one('export.config', 'Config',
                                     ondelete='cascade', select=True,
                                     readonly=True,),
        'sequence': fields.integer('Sequence'),
        'field_id': fields.many2one('ir.model.fields', 'Column'),
        'ttype': fields.related('field_id', 'ttype', type="selection",
                                selection=_get_fields_type,
                                store=True, string="Type", readonly=True,),
        'field_description': fields.related('field_id', 'field_description',
                                            type="char", store=True,
                                            string="Description",
                                            readonly=True,),
    }
    _defaults = {
        'sequence': 1000,
    }
export_column()


class export_ids(osv.osv):
    _name = 'export.ids'

    _columns = {
            'model_id' : fields.many2one('ir.model', 'Object', required=True, domain=[('osv_memory','=',False)]),
            'config_id' : fields.many2one('export.config', 'Export Config'),
            'name':fields.char('Records'),
            'last_logged_on': fields.datetime('Last Logged on', readonly=True, select=True, help="Date on which last log was done."),
                }
export_ids()


class custom_label(osv.osv):
    _name = 'custom.label'
    _columns = {
            'export_cofig_id': fields.many2one('export.config','Export Config'),
            'field_name' : fields.many2one('ir.model.fields','Field Name', domain="[('model_id','=',parent.model_id)]"),
            'value' : fields.char('Value'),
                }
custom_label()

class domain_line(osv.osv):
    _name = 'domain.line'
    _columns = {
            'export_cofig_id': fields.many2one('export.config','Export Config'),
            'field_name' : fields.many2one('ir.model.fields','Field Name', domain="[('model_id','=',parent.model_id)]"),
            'operator': fields.selection([('ilike','Contains'),('=','Equal'),('!=','Not Equal'),('<','Less Than'),('>','Greater Than'),('<=','Less Than Equal To'),('>=','Greater Than Equal To')],'Operator'),
            'value' : fields.char('Value'),
                }
domain_line()
