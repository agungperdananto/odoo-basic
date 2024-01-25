from odoo import models, fields, _

class CustomPurchase(models.Model):
    _name = 'custom.purchase'

    name = fields.Char(string='name')
    date = fields.Date(string='date')
    status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('done', 'Done')])
