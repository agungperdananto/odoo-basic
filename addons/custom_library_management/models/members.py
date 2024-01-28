import uuid
from odoo import models, fields, _

class LibraryMember(models.Model):
    _name = 'library.member'

    user_id = fields.Char(string='User ID', default=str(uuid.uuid4()))
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Text(string='Address', required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    registration_date = fields.Datetime(string='Registration Date', default=fields.Datetime.now(), required=True, readonly=True)
    is_active = fields.Boolean(string='Is Active', default=True)
