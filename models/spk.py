from odoo import api, models, fields
from . import mahasiswa, minat

class Spk(models.Model):
    _name = 'spk.data'
    _description = 'Data SPK'
    _rec_name = 'mahasiswa_id'
    _order = 'nilai_utility'
    
    # Alternatif
    mahasiswa_id = fields.Many2one('mahasiswa.data', string='Mahasiswa')

    # Kriteria
    jmlMinat = fields.Integer(string='Jumlah Minat', compute='_compute_jml_minat')
    tingkatKemampuan = fields.Integer(string='Tingkat Kemampuan', related='mahasiswa_id.tingkatKemampuan')
    ipk = fields.Float(string='IPK', related='mahasiswa_id.ipk')
    memilikiPrestasi = fields.Integer(string='Memiliki Prestasi', compute='_compute_memiliki_prestasi')

    nilai_utility = fields.Float(string='Nilai Utility', compute='_compute_nilai_utility')
    ranking = fields.Integer(string='Ranking', compute='_compute_ranking', store=True)

    @api.depends('mahasiswa_id.minat')
    def _compute_jml_minat(self):
        for record in self:
            record.jmlMinat = len(record.mahasiswa_id.minat)

    @api.depends('mahasiswa_id.statusPrestasi')
    def _compute_memiliki_prestasi(self):
        for record in self:
            record.memilikiPrestasi = 2 if record.mahasiswa_id.statusPrestasi == 'Ya' else 1

    # Perhitungan SPK
    @api.depends('jmlMinat', 'tingkatKemampuan', 'ipk', 'memilikiPrestasi')
    def _compute_nilai_utility(self):
        bobot = [0.1, 0.2, 0.5, 0.2]
        for record in self:
            kriteria = [record.jmlMinat, record.tingkatKemampuan, record.ipk, record.memilikiPrestasi]
            normalized_kriteria = [(k - min(kriteria)) / (max(kriteria) - min(kriteria)) for k in kriteria]
            weighted_normalized_kriteria = [b * k for b, k in zip(bobot, normalized_kriteria)]
            record.nilai_utility = sum(weighted_normalized_kriteria)

    @api.depends('nilai_utility')
    def _compute_ranking(self):
        records = self.search([])
        sorted_records = records.sorted(key=lambda r: r.nilai_utility, reverse=True)
        for i, record in enumerate(sorted_records, start=1):
            record.ranking = i