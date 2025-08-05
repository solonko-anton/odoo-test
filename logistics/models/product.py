from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    weight = fields.Float(string='Вага')
    volume = fields.Float(string='Об`єм')
