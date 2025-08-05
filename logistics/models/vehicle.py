from odoo import fields, models

class Car(models.Model):
    _name = 'logistics.vehicle'
    _description = 'Автомобіль'

    name = fields.Char(string='Номер авто', required=True)
    carrier_id = fields.Many2one('res.partner', string='Перевізник',
        domain=[("contracor_type", "=", "Carries")], required=True, ondelete='cascade')
    max_weight = fields.Float(string='Максимальна вага (кг)', required=True)
    max_volume = fields.Float(string='Максимальний об\'єм (м³)', required=True)