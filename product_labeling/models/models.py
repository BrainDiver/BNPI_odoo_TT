from odoo import models, fields, api


class Product(models.Model):
    _name = "product.model"

    name = fields.Char(required=True)
    description = fields.Text(required=True)

class Properties(models.Model):
    _name = "properties.properties"

    status = fields.Selection(selection = lambda self: self.method())
    stock_from = fields.Char(required = True)
    stock_where = fields.Char(required = True)
    product = fields.Many2one(Product, ondelete = 'no action')
    count = fields.Integer(required = True)

    @api.model
    def _select_choise(self):
        select_list = ["Продажа", "Покупка"]
        return select_list
