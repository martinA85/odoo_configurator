# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from PIL import Image
import io
from io import BytesIO
import base64
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ConfigurateurProduct(http.Controller):
    

    @http.route(['/shop/config/recap'], type='http', auth="public", website=True)
    def recap_config(self, variant_lst, product_id, salable):

    	variant_id = variant_lst.split(',')
    	# var env is environement variable that we use to browse our object
    	env = request.env
    	# creating an empty product.template object
    	product_template = env['product.template']
    	# product is the product.template
    	product = product_template.browse(int(product_id))

    	# variant_template is a variant_product line
    	variant_template = env['configurateur_product.line']
        config = env['configurateur.config']

        config_image = Image.open(BytesIO(base64.b64decode(product.background)))

        config_string = ""
        config_price = product.list_price
    	# selected variant list
    	selected_variant = list()
        config_var_ids = list()
        for id_variant in variant_id:
            try:
                variant = variant_template.browse(int(id_variant))
                selected_variant.append(variant)
                config_var_ids.append(variant.id)
                config_price += variant.extra_price
                var_img = Image.open(BytesIO(base64.b64decode(variant.image))).convert("RGBA")
                var_img.convert('RGB')
                config_image.paste(var_img, (0,0),var_img)
            except:
                pass

        # ipdb.set_trace()
        print(type(config_image))

        in_nem_file = io.BytesIO()
        config_image.save(in_nem_file, format="png")
        in_nem_file.seek(0)
        config_image = base64_encoded_result_bytes = base64.b64encode(in_nem_file.read())

        vals = {
            'total_price':str(config_price),
            'variant_line_ids':[(6,0,config_var_ids)],
            'config_image' : config_image
        }

        config = config.create(vals)
        values = {

            'variants':selected_variant,
            'product':product,
            'config':config,
            'salable':salable
        }
        return request.render("configOdoo.recap_config",values)


class SaleSite(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id ,add_qty=1, set_qty=0,config=None,**kw):
        to_return = super(SaleSite, self).cart_update(product_id)
        request.website.sale_get_order(force_create=1)._cart_update(
            config=config,
            product_id=int(product_id),
            add_qty=float(add_qty),
            set_qty=float(set_qty),
            attributes=self._filter_attributes(**kw),
        )
        return request.redirect("/shop/cart")


    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        to_return = super(SaleSite, self).confirm_order(**post)
        order = request.website.sale_get_order()
        lines = order.order_line

        for line in lines:
            if line.config != None:
                order.amount_total += line.extra_config
                line.price_unit += line.extra_config

        return to_return
        
        
    @http.route(['/shop/config/valid_request'], type='http', auth="public", website=True)
    def valid_request(self, contact_name, phone, email_form, config, product_id):
        
        name = "Demande devis site web : "+contact_name
        
        config_tmp = self.env['configurateur.config']
    	config = config_tmp.browse(int(config))
        
        vals = {
            "name" : name,
            "contact_name" : contact_name,
            "phone" : phone,
            "email_from": email_form,
            "variant_line_ids": config.variant_line_ids
        }
        
        request.env['crm.lead'].create(vals)
        
        return request.render("configOdoo.thanks_page")
