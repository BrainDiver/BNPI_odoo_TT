from odoo import models, fields, api

#Модель Товара
class Product(models.Model):
    _name = "product.model"

    name = fields.Char(required=True)
    description = fields.Text(required=True)

#Модель акта для изменения свойств товара
class Properties(models.Model):
    _name = "properties.properties"

    status = fields.Selection(selection =  lambda self: self._select_choise()) #[("продажа", "Продажа"),("покупка","Покупка")])
    stock_from = fields.Char(required = True)
    stock_where = fields.Char(required = True)
    product = fields.Many2one('product.model', string="Product", ondelete = 'no action')
    count = fields.Integer(required = True)

    @api.model
    def _select_choise(self):
        select_list = [("продажа","Продажа"),("покупка","Покупка")]
        return select_list
