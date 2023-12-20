from odoo import api, models, fields
from . import mahasiswa

class Tim(models.Model):
    _name = 'minat.data'
    _description = 'Data Minat'
    _rec_name = 'minat_ids'

    minat_ids = fields.Char(string='Nama Minat / Keahlian', required=True)

