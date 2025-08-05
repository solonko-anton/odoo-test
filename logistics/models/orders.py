from odoo import models, fields, api
from odoo.odoo.tools.populate import compute


class Order(models.Model):
    _name = 'logistics.order'

    name = fields.Char(string='Номер замовлення', reqired=True, default='New')
    date = fields.Date(string='Дата замовлення', default=fields.Date.today())
    supplier_id = fields.Many2one('res.partner', string='Постачальник',
                                  domain=[("contracor_type", "=", "Supplier")])
    customer_id = fields.Many2one('res.partner',string='Кілєнт',
                                  domain=[("contracor_type", "=", "Customer")])
    total_amount = fields.Float(string='Сумарна вартість', compute='count_totals', store=True)
    total_weight = fields.Float(string='Загальна вага', compute='count_totals', store=True)
    total_volume = fields.Float(string='Загальний об`єм', compute='count_totals', store=True)

    order_table = fields.One2many('logistics.order.table', 'order_id')

    @api.depends('order_table.products_sum', 'order_table.quantity', 'order_table.product_id')
    def count_totals(self):
        for order in self:
            order.total_amount = sum(table.products_sum for table in order.order_table)
            order.total_weight = sum(table.product_id.weight * table.quantity for table in order.order_table)
            order.total_volume = sum(table.product_id.volume * table.quantity for table in order.order_table)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('logistics.order') or 'New'
        return super(Order, self).create(vals_list)


class OrderTable(models.Model):
    _name = 'logistics.order.table'

    order_id = fields.Many2one('logistics.order', string='Замовлення', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Товар')
    price = fields.Float(string='Ціна')
    quantity = fields.Float(string='Кількість')
    products_sum = fields.Float(string='Загальна вартість')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id:
                record.price = record.product_id.lst_price
                if not record.quantity:
                    record.quantity = 1
                record.products_sum = record.price * record.quantity

    @api.onchange('quantity')
    def _onchange_quantity(self):
        for record in self:
            record.products_sum= record.price * record.quantity