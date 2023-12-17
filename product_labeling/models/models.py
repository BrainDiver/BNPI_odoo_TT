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
    marked_product = fields.One2many('marked_product.model', 'properties')

    #Метод для проведения акта
    def confirm_act(self):
        count = self._context.get('count')
        status = self._context.get('status')
        values = {'product': self._context.get('product'),
                  'last_stock': self._context.get('stock_where'),
                  'last_status': self._context.get('status'),
                  'properties': self.id}

        if status == "покупка": #Для создания маркированого товара в  БД у меня было 3 возможных решения. 
                                #1) Взять модель MarkedProduct и переопределить метод create ее родительского класса и использовать его как статический метод
                                #иными словами использовать этот метод для создания экземпляра класса в обход __init__ родительского класса. Для каждого товара в цикле это выглядело бы так 
                                #MarkedProduct.create(values). Где values - словарь с нужными данными
                                #2) использовать, для создания записей товаров в бд, курсор self.env.cr.execute("INSERT SQL query") для взаимодействия с БД на прямую посредством SQL запросов.
                                #У этого способа есть свои недостатки насколько я понимаю в таком случае может не выставится пользователь который добавил записи в бд и дата создания записи create_on. 
                                #Это пришлось бы делать в ручную
                                #3) использовать стандартный метод Odoo для создания записей в БД self.env['marked_product.model'].create(values).
                                #Я выбрал 3 вариант за его простоту по отношению ко остальным двум и отсутствия недостатков второго.
            for i in range(0, count):
                record = self.env['marked_product.model'].create(values)
        else:
            for i in self.marked_product:
                i.write({'last_stock': self._context.get('stock_where'), 'last_status': self._context.get('status')})
                print(i.last_stock)
            for i in self.cost:
                i.write({'date': self.create_date})


    @api.model
    def _select_choise(self):
        select_list = [("продажа","Продажа"),("покупка","Покупка")]
        return select_list



#Модель Затрат и Приходов
class Cost(models.Model):
    _name = "cost.cost"

    date = fields.Datetime(required = False)
    properties = fields.Many2one("properties.properties", required = True)
    expenses_description = fields.Char(required = True)
    value = fields.Float(required = True, default = 1.0)


#Модель маркированого товара
class MarkedProduct(models.Model):
    _name = "marked_product.model"

    product = fields.Many2one("product.model", required = True)
    last_stock = fields.Char()
    last_status = fields.Char(required = True)
    cost = fields.One2many(related='properties.cost')
    properties = fields.Many2one("properties.properties", required = True)
