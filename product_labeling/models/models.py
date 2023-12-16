from odoo import models, fields, api
#Файл моделей. Все модели для базы данных мы создаем здесь

#Модель Товара
class Product(models.Model):
    _name = "product.model"

    name = fields.Char(required = True)
    description = fields.Text(required = True)


#Модель акта для изменения свойств товара
class Properties(models.Model):
    _name = "properties.properties"

    status = fields.Selection(selection = lambda self: self._select_choise(), required = True) #[("продажа", "Продажа"),("покупка","Покупка")])
    stock_from = fields.Char()
    stock_where = fields.Char(required = True)
    product = fields.Many2one('product.model', string = "Product", ondelete = 'no action', required = True)
    count = fields.Integer(required = True, default = 1)
    cost = fields.One2many('cost.cost', 'properties')
    

    @api.model
    def _select_choise(self):
        select_list = [("продажа","Продажа"),("покупка","Покупка")]
        return select_list


#Модель Затрат и Приходов
class Cost(models.Model):
    _name = "cost.cost"

    properties= fields.Many2one("properties.properties", required = True)
    commission = fields.Float(required = True, string = "expenses", default = 1.0)
    expenses_description = fields.Char(required = True)
    sale = fields.Float(required = True, default = 1.0)
    
