import uuid
from odoo import api, models, fields, _


class LibraryBook(models.Model):
    _name = 'library.book'

    isbn = fields.Char(string='ISBN', required=True)
    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    release_year = fields.Char(string='Release Year', default='1900')
    language = fields.Char(string='Language', required=True)

    book_items = fields.One2many('library.book.item', 'book_id', string='Book Items')


class LibraryBookItem(models.Model):
    _name = 'library.book.item'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    book_code = fields.Char(string='Book Code', compute='_generate_book_code', store=True)
    isbn = fields.Char(string='ISBN')

    display_name = fields.Char(compute='_compute_display_name', store=True)

    condition = fields.Selection([('good', 'Good'), ('standard', 'Standard'), ('broken', 'Broken')], default='good')
    is_ready = fields.Boolean(string='Is Ready', default=True)
    date_added = fields.Datetime(string='date added', default=fields.Datetime.now(), required=True)

    @api.depends('isbn', 'book_id.isbn')
    def _generate_book_code(self):
        for record in self:
            if record.book_id:
                record.book_code = f"{record.book_id.isbn}-{uuid.uuid4()}"
            else:
                record.book_code = f"{record.isbn}-{uuid.uuid4()}"

    @api.onchange('book_id')
    def _onchange_book_id(self):
        if self.book_id:
            self.isbn = self.book_id.isbn

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=10):
        args = args or []
        domain = [
            '|',
            ('book_code', operator, name),
            ('display_name', operator, name),
            ('book_id.title', operator, name),  # Include title search
        ]
        # Additional conditions for filtering
        domain += [('is_ready', '=', True), ('condition', '!=', 'broken')]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    @api.onchange('condition')
    @api.depends('book_code', 'condition', 'book_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.book_id.title}-[{record.condition}]-[{record.book_code}] '