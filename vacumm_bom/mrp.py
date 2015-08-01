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
import logging
from openerp.osv import osv

_logger = logging.getLogger(__name__)


class mrp_bom(osv.osv):

    _inherit = 'mrp.bom'

    def process_vacumm_bom(self, cr, uid, journal_ids=None, context=None):
        
        try:
            print '--> Start'
            cr.execute("""
                delete from mrp_bom where id not in 
                (
                -- BOM Template
                select id from mrp_bom where is_bom_template is true union
                select id from mrp_bom where bom_id in (select id from mrp_bom where is_bom_template is true)
                union
                -- BOM still in Draft state
                select bom_id as id from mrp_production where state in ('draft') union
                select id from mrp_bom where bom_id in (select bom_id as id from mrp_production where state in ('draft'))
                union
                -- BOM created within 1 month
                select id from mrp_bom where create_date > (now() - INTERVAL '1 month') union
                select id from mrp_bom where bom_id in (select id from mrp_bom where create_date > (now() - INTERVAL '1 month'))
                union
                -- Standard AHU
                select id from mrp_bom
                where product_id in 
                (select pp.id from product_product pp join product_template pt on pt.id = pp.product_tmpl_id where categ_id = 5)
                and bom_id is null
                union select id from mrp_bom where bom_id in (select id from mrp_bom
                    where product_id in 
                    (select pp.id from product_product pp join product_template pt on pt.id = pp.product_tmpl_id where categ_id = 5)
                    and bom_id is null)
                );
            """)
            print '--> End'
        except Exception:
            _logger.exception("Failed processing vacumm bom")

mrp_bom()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
