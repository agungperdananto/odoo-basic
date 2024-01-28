from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class LibraryTransaction(models.Model):
    _name = 'library.transaction'

    member_id = fields.Many2one('library.member', string='Member ID')
    created_at = fields.Datetime(string='Created_at', default=fields.Datetime.now(), required=True)
    updated_at = fields.Datetime(string='Updated_at', default=fields.Datetime.now(), required=True)

    transaction_items = fields.One2many('library.transaction.item', 'transaction_id', string='Library Items')


class LibraryTransactionItem(models.Model):
    _name = 'library.transaction.item'

    transaction_id = fields.Many2one('library.transaction', string='Transaction ID')
    book_item_id = fields.Many2one('library.book.item', string='Book Item', required=True)
    initial_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken')])
    return_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken')])
    lend_date = fields.Datetime(string='created_at', default=fields.Datetime.now(), required=True)
    return_date = fields.Datetime(string='updated_at')
    status = fields.Selection([('on_customer', 'On Customer'), ('returned', 'Returned')], default='on_customer')

    @api.model
    def create(self, values):
        record = super(LibraryTransactionItem, self).create(values)
        if not record.book_item_id.is_ready:
            raise ValidationError(f'book with code{record.book_item_id.book_code} is not ready')

        record.initial_condition = record.book_item_id.condition
        if record.status == 'on_customer':
            record.book_item_id.is_ready = False
        return record
    

    def write(self, values):
        result = super(LibraryTransactionItem, self).write(values)
        if values.get('status') == 'returned':
            self.book_item_id.write({'is_ready': True})
        return result
