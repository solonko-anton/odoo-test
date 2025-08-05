from odoo.odoo import models, fields


class ResPartner(models.Model):
    _inherit = ['res.partner']

    contracor_type = fields.Selection(
        [('Carries', 'Перевізник'),
         ('Supplier', 'Постачальник'),
         ('Customer', 'Клієнт')], string='Вид контрагента')

