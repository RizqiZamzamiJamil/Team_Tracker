from odoo import api, models, fields
from . import mahasiswa, event

class Tim(models.Model):
    _name = 'team.data'
    _description = 'Data Tim'
    _rec_name = 'nama_tim'

    nama_tim = fields.Char(string='Nama Tim', required=True)
    leader = fields.Many2one('mahasiswa.data', string='Ketua Tim')
    member_ids = fields.Many2many('mahasiswa.data', string='Anggota Tim')
    deskripsi = fields.Text(String='Deskripsi')
    kategori_lomba = fields.Selection([
        ('ai', 'Artificial Intelligence'),
        ('web', 'Web Development'),
        ('game', 'Game Development'),
        ('iot', 'Internet of Things'),
        ('robot', 'Robotics'),
        ('animasi', 'Animation'),
        ('bisnis', 'Business Plan'),
        ('lain', 'Lainnya')
    ], string='Kategori Lomba', required=True)
    
    event_lomba = fields.Many2one('event.data', string='Event')
    # mahasiswa_data_ids = fields.One2many('mahasiswa.data', 'tim_id', string='Data Mahasiswa')