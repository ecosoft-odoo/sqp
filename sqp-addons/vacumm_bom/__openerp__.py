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

{
    'name' : "Vacumm BOM for SQP",
    'author' : 'Kitti U.',
    'summary': '',
    'description': """

Improve speed of Create One-Time Product by deleting all bom data not in use.

SQP to delete unused BOM

-- Do not delete
-- 1) BOM Templates and all record with 
select id from mrp_bom where is_bom_template is true;
select id from mrp_bom where bom_id in (select id from mrp_bom where is_bom_template is true);
-- 2) BOM with the mrp.product, still in Draft State
select bom_id as id from mrp_production where state in ('draft');
select id from mrp_bom where bom_id in (select bom_id as id from mrp_production where state in ('draft'));
-- 3) BOM that is not old yet
???


--------------------------------------------------------------------------- Backup Table

CREATE TABLE mrp_bom_bk
(
  id serial NOT NULL,
  create_uid integer,
  create_date timestamp without time zone,
  write_date timestamp without time zone,
  write_uid integer,
  date_stop date, -- Valid Until
  code character varying(16), -- Reference
  product_uom integer NOT NULL, -- Product Unit of Measure
  product_uos_qty double precision, -- Product UOS Qty
  date_start date, -- Valid From
  product_qty numeric NOT NULL, -- Product Quantity
  product_uos integer, -- Product UOS
  product_efficiency double precision NOT NULL, -- Manufacturing Efficiency
  active boolean, -- Active
  product_rounding double precision, -- Product Rounding
  name character varying(64), -- Name
  sequence integer, -- Sequence
  company_id integer NOT NULL, -- Company
  routing_id integer, -- Routing
  product_id integer NOT NULL, -- Product
  bom_id integer, -- Parent BoM
  "position" character varying(64), -- Internal Reference
  type character varying NOT NULL, -- BoM Type
  product_qty_formula character varying(512), -- Product Qty-Formula
  is_bom_template boolean, -- BOM Template
  bom_template_type character varying, -- BOM Template Type
  "L" boolean, -- length (L)
  "T" boolean, -- Thick (T)
  "W" boolean, -- Width (W)
  bom_template_id boolean, -- BOM Template
  bom_product_type character varying, -- BOM Product Type
  new_name_format character varying(256), -- New Product Naming Format
  CONSTRAINT mrp_bom_bk_pkey PRIMARY KEY (id),
  CONSTRAINT mrp_bom_bk_bom_id_fkey FOREIGN KEY (bom_id)
      REFERENCES mrp_bom_bk (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT mrp_bom_bk_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES res_company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_create_uid_fkey FOREIGN KEY (create_uid)
      REFERENCES res_users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_product_id_fkey FOREIGN KEY (product_id)
      REFERENCES product_product (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_product_uom_fkey FOREIGN KEY (product_uom)
      REFERENCES product_uom (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_product_uos_fkey FOREIGN KEY (product_uos)
      REFERENCES product_uom (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_routing_id_fkey FOREIGN KEY (routing_id)
      REFERENCES mrp_routing (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_write_uid_fkey FOREIGN KEY (write_uid)
      REFERENCES res_users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT mrp_bom_bk_bom_qty_zero CHECK (product_qty > 0::numeric)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE mrp_bom_bk
  OWNER TO openerp;
COMMENT ON TABLE mrp_bom_bk
  IS 'Bill of Material';
COMMENT ON COLUMN mrp_bom_bk.date_stop IS 'Valid Until';
COMMENT ON COLUMN mrp_bom_bk.code IS 'Reference';
COMMENT ON COLUMN mrp_bom_bk.product_uom IS 'Product Unit of Measure';
COMMENT ON COLUMN mrp_bom_bk.product_uos_qty IS 'Product UOS Qty';
COMMENT ON COLUMN mrp_bom_bk.date_start IS 'Valid From';
COMMENT ON COLUMN mrp_bom_bk.product_qty IS 'Product Quantity';
COMMENT ON COLUMN mrp_bom_bk.product_uos IS 'Product UOS';
COMMENT ON COLUMN mrp_bom_bk.product_efficiency IS 'Manufacturing Efficiency';
COMMENT ON COLUMN mrp_bom_bk.active IS 'Active';
COMMENT ON COLUMN mrp_bom_bk.product_rounding IS 'Product Rounding';
COMMENT ON COLUMN mrp_bom_bk.name IS 'Name';
COMMENT ON COLUMN mrp_bom_bk.sequence IS 'Sequence';
COMMENT ON COLUMN mrp_bom_bk.company_id IS 'Company';
COMMENT ON COLUMN mrp_bom_bk.routing_id IS 'Routing';
COMMENT ON COLUMN mrp_bom_bk.product_id IS 'Product';
COMMENT ON COLUMN mrp_bom_bk.bom_id IS 'Parent BoM';
COMMENT ON COLUMN mrp_bom_bk."position" IS 'Internal Reference';
COMMENT ON COLUMN mrp_bom_bk.type IS 'BoM Type';
COMMENT ON COLUMN mrp_bom_bk.product_qty_formula IS 'Product Qty-Formula';
COMMENT ON COLUMN mrp_bom_bk.is_bom_template IS 'BOM Template';
COMMENT ON COLUMN mrp_bom_bk.bom_template_type IS 'BOM Template Type';
COMMENT ON COLUMN mrp_bom_bk."L" IS 'length (L)';
COMMENT ON COLUMN mrp_bom_bk."T" IS 'Thick (T)';
COMMENT ON COLUMN mrp_bom_bk."W" IS 'Width (W)';
COMMENT ON COLUMN mrp_bom_bk.bom_template_id IS 'BOM Template';
COMMENT ON COLUMN mrp_bom_bk.bom_product_type IS 'BOM Product Type';
COMMENT ON COLUMN mrp_bom_bk.new_name_format IS 'New Product Naming Format';


-- Index: mrp_bom_bk_bom_id_index

-- DROP INDEX mrp_bom_bk_bom_id_index;

CREATE INDEX mrp_bom_bk_bom_id_index
  ON mrp_bom_bk
  USING btree
  (bom_id);

----------------------------------------------------------------------- Backup

insert into mrp_bom_bk select * from mrp_bom;

----------------------------------------------------------------------- Delete

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


insert into mrp_bom_bk select * from mrp_bom;


""",
    'category': 'Manufacturing',
    'website' : 'http://www.ecosoft.co.th',
    'images' : [],
    'depends' : ['mrp'],
    'demo' : [],
    'data' : [
        'mrp_view.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
