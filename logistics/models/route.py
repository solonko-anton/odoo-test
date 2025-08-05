from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Route(models.Model):
    _name = 'logistics.route'
    _description = 'Маршрут'

    name = fields.Char(string='Номер маршруту', required=True, default="New")
    carrier_id = fields.Many2one('res.partner', string='Перевізник',
                                 domain=[("contracor_type", "=", "Carries")], required=True)
    vehicle_id = fields.Many2one('logistics.vehicle', string='Автомобіль', required=True)
    order_ids = fields.Many2many('logistics.order', string='Замовлення')
    total_weight = fields.Float(string='Сумарна вага', compute='_compute_totals')
    total_volume = fields.Float(string='Сумарний об`єм', compute='_compute_totals')

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        for route in self:
            if route.vehicle_id:
                route.carrier_id = route.vehicle_id.carrier_id

    @api.depends('order_ids')
    def _compute_totals(self):
        for route in self:
            route.total_weight = sum(order.total_weight for order in route.order_ids)
            route.total_volume = sum(order.total_volume for order in route.order_ids)

    @api.constrains('order_ids', 'vehicle_id')
    def _check_vehicle_capacity(self):
        for route in self:
            if route.vehicle_id:
                if route.total_weight > route.vehicle_id.max_weight:
                    raise ValidationError('Сумарна вага замовлень перевищує максимальну вагу автомобіля!')
                if route.total_volume > route.vehicle_id.max_volume:
                    raise ValidationError('Сумарний об`єм замовлень перевищує максимальний об`єм автомобіля!')