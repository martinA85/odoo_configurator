# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import ipdb

# Herite du model produit pour rajouter un champ configurable
class Product(models.Model):
	_inherit = 'product.template'

	is_configurable = fields.Boolean(string="Configurable", index=True, default=False)

	variant_ids = fields.Many2many('configurateur_product.variant', string="Variantes")
	background = fields.Binary("Image", attachment=True, help="This field holds the image used as image for the product, limited to 1024x1024px.")


class Variant(models.Model):
	_name="configurateur_product.variant"

	name = fields.Char()
	libelle = fields.Char(string = "libelle(afficher sur le site)")
	nb_line = fields.Integer(compute="_compute_nb_line", readonly="1")
	var_material_id = fields.Many2many('configurateur.material', string = "material")

	def _compute_nb_line(self):
		for record in self:
			record.nb_line = 5

	@api.onchange('line_ids')
	def _update_nb_line(self):
		for record in self:
			record.nb_line = len(record.line_ids)


class Line_variant(models.Model):
	_name="configurateur_product.line"
	_rec_name = 'name'

	name = fields.Char()
	libelle = fields.Char(string = "libelle(afficher sur le site)")
	image = fields.Binary("Image", attachment=True, help="This field holds the image used as image for the product, limited to 1024x1024px.")
	icon = fields.Binary("Image", attachment=True, help="This field holds the image used as image for the product, limited to 1024x1024px.")
	extra_price = fields.Float("supplément", default=0)
	
	@api.onchange('icon')
	def _update_icon(self):
		for record in self:
			resized_images = tools.image_get_resized_images(record.icon, return_big=True, avoid_resize_medium=True)
			record.icon = resized_images['image_small']


class variant_material(models.Model):
	_name="configurateur.material"

	name = fields.Char()
	libelle = fields.Char(string = "libelle")
	line_ids = fields.Many2many('configurateur_product.line', string="Liste des changement")
	href_id = fields.Char(compute="_compute_href", readonly="1")

	def _compute_href(self):
		for record in self:
			record.href_id = "#"+str(record.id)

class ConfigProduct(models.Model):
	_name="configurateur.config"

	total_price = fields.Float("Cout Total", default=0)
	variant_line_ids = fields.Many2many("configurateur_product.line")

class SaleOrderLine(models.Model):
	_inherit="sale.order.line"

	extra_config = fields.Monetary(string="extra config price")
	config = fields.Many2one("configurateur.config")
	variant_line_ids = fields.Many2many("configurateur_product.line")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None,config=None,**kwargs):
    	to_return = super(SaleOrder, self)._cart_update(product_id=int(product_id),add_qty=add_qty, set_qty=set_qty)
    	order_line = self._cart_find_product_line(product_id, line_id, **kwargs)
    	product = self.env['product.product'].browse(product_id)

    	if config != None:
    		config_tmp = self.env['configurateur.config']
    		config = config_tmp.browse(int(config))
    		price = config.total_price
    		order_line.config = config.id
    		order_line.variant_line_ids = config.variant_line_ids
    		order_line.price_unit = price
    		order_line.product_uom_qty = 1;
    		order_line.extra_config = price - product.price
    		return {"line_id":order_line.id, 'quantity':1}
    	else:
    		return to_return
