from odoo import models, fields, _


class LibraryTransaction(models.Model):
    _name = 'library.transaction'

    member_id = fields.Many2one('library.member', string='Member ID')
    created_at = fields.Datetime(string='Created_at', default=fields.Datetime.now(), required=True)
    updated_at = fields.Datetime(string='Updated_at', default=fields.Datetime.now(), required=True)

    library_items = fields.One2many('library.transaction.item', 'transaction_id', string='Library Items')


class LibraryTransactionItem(models.Model):
    _name = 'library.transaction.item'

    transaction_id = fields.Many2one('library.transaction', string='Transaction ID')
    book_item_id = fields.Many2one('library.book.item', string='Book Item')
    initial_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken')], default='good')
    return_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken')], default='good')
    lend_date = fields.Datetime(string='created_at', default=fields.Datetime.now(), required=True)
    return_date = fields.Datetime(string='updated_at')
    status = fields.Selection([('on_customer', 'On Customer'), ('returned', 'returned')], default='on_customer')
