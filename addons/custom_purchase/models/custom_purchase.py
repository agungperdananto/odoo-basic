from odoo import models, fields, _


class CustomPurchase(models.Model):
    _name = 'custom.purchase'

    name = fields.Char(string='name')
    date = fields.Date(string='date')
    status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('done', 'Done')], default='draft')
    purchase_line_ids = fields.One2many('custom.purchase.line', 'purchase_id', string='custom purchase lines')


class CustomPurchaseLine(models.Model):
    _name = 'custom.purchase.line'

    purchase_id = fields.Many2one('custom.purchase', string='custom purchase id')
    product_id = fields.Many2one('product.product', string='product id')
    quantity = fields.Float(string='quantity', default=0)
    uom_id = fields.Many2one('uom.uom', string='measure')
