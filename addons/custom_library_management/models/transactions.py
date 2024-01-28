import uuid
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class LibraryTransaction(models.Model):
    _name = 'library.transaction'

    transaction_id = fields.Char(string='Transaction ID', default='IN-'+str(uuid.uuid4()))

    member_id = fields.Many2one('library.member', string='Member ID', required=True)
    created_at = fields.Datetime(string='Created_at', default=fields.Datetime.now(), required=True)
    updated_at = fields.Datetime(string='Updated_at', default=fields.Datetime.now(), required=True)

    transaction_items = fields.One2many('library.transaction.item', 'transaction_id', string='Library Items')

    status = fields.Selection([('on_progress', 'On Progress'), ('done', 'Done')], default='on_progress')
    
    def write(self, values):
        values['updated_at'] = fields.Datetime.now()
        result = super(LibraryTransaction, self).write(values)
        return result


class LibraryTransactionItem(models.Model):
    _name = 'library.transaction.item'

    transaction_id = fields.Many2one('library.transaction', string='Transaction ID')
    book_item_id = fields.Many2one('library.book.item', string='Book Item', required=True)
    initial_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard')])
    return_condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken'), ('lost', 'Lost')])
    lend_date = fields.Datetime(string='created_at', default=fields.Datetime.now(), required=True)
    return_date = fields.Datetime(string='updated_at')
    status = fields.Selection([('on_customer', 'On Customer'), ('returned', 'Returned'), ('lost', 'Lost')], default='on_customer')

    def _update_transaction_status(self):
        """Update parent status based on child statuses."""
        transaction = self.transaction_id

        # Check if all child items have the status 'returned'
        all_returned = all(item.status in ('returned', 'lost') for item in transaction.transaction_items)

        # Update parent status based on child statuses
        if all_returned:
            transaction.status = 'done'

    @api.model
    def create(self, values):
        record = super(LibraryTransactionItem, self).create(values)
        if not record.book_item_id.on_hand:
            raise ValidationError(f'book with code{record.book_item_id.book_code} is not ready')

        condition = record.book_item_id.condition
        record.initial_condition = condition
        record.return_condition = condition

        if record.status == 'on_customer':
            record.book_item_id.on_hand = False
        return record
    

    def write(self, values):
        values['return_date'] = fields.Datetime.now()
        result = super(LibraryTransactionItem, self).write(values)
        self._update_transaction_status()
        status = values.get('status')
        change = {}

        if status == 'returned':
            change = {
                'on_hand': True,
                }
            change['condition'] = values.get('return_condition')
        elif status == 'lost':
            status = values.get('status')
            change['condition'] = status
            self.write({'return_condition': status})
        
        self.book_item_id.write(change)

        return result
