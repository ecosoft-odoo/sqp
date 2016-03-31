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

from openerp.osv import osv
from openerp import pooler

class export_all(osv.osv_memory):
    _name = "export.all"
    _description = "Export All"

    def export_all(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        records = context.get('active_ids', [])
        pool_obj = pooler.get_pool(cr.dbname)
        data_inv = pool_obj.get('export.config').start_export(cr, uid, records,context)
        return {'type': 'ir.actions.act_window_close'}

export_all()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
