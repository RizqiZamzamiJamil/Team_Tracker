from odoo import api, models, fields
import base64
import io
import csv
from . import minat

class Mahasiswa(models.Model):
    _name = 'mahasiswa.data'
    _rec_name = 'nama'
    _description = 'Data Mahasiswa'

    nama = fields.Char(string='Nama', required=True)
    nim = fields.Char(string="NIM")
    gender = fields.Selection([('Laki-laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], string="Jenis Kelamin")
    email = fields.Char(string="Email")
    prodi = fields.Selection([('D4 Sistem Informasi Bisnis', 'D4 Sistem Informasi Bisnis'), ('D4 Teknik Informatika', 'D4 Teknik Informatika')], string="Program Studi")
    kelas = fields.Char(string="Kelas")
    telepon = fields.Char(string="Telepon")

    minat = fields.Many2many('minat.data', relation='mahasiswa_minat_rel', column1='mahasiswa_id', column2='minat_id', string='Minat / Keahlian')
    tingkatKemampuan = fields.Integer(string="Tingkat Kemampuan Bidang")
    statusPrestasi = fields.Selection([('Tidak', 'Tidak'), ('Ya', 'Ya')], string="Memiliki Prestasi")
    peran = fields.Selection([('Hacker (Coding, Engineer, & Developer)', 'Hacker (Coding, Engineer, & Developer)'), ('Hipster (Desainer, UI & UX)', 'Hipster (Desainer, UI & UX)'), ('Hustler (Project Manager, Inisiator, Bisnis & Analyst)', 'Hustler (Project Manager, Inisiator, Bisnis & Analyst)')], string="Peran")
    ipk = fields.Float(string='IPK')

    @api.model
    def create(self, vals):
        record = super(Mahasiswa, self).create(vals)
        self.env['spk.data'].create({'mahasiswa_id': record.id})
        return record

    def write(self, vals):
        result = super(Mahasiswa, self).write(vals)
        for record in self:
            spk_record = self.env['spk.data'].search([('mahasiswa_id', '=', record.id)], limit=1)
            if not spk_record:
                self.env['spk.data'].create({'mahasiswa_id': record.id})
        return result


#  Import Mahasiswa
class MahasiswaImportWizard(models.TransientModel):
    _name = 'mahasiswa.import.wizard'
    _description = 'Wizard untuk mengimpor data mahasiswa dari file csv'

    csv_file = fields.Binary(string='File CSV', required=True)

    def import_data(self):
        csv_data = base64.b64decode(self.csv_file)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        csv_reader = csv.reader(data_file, delimiter=',')
    
        keys = ['nama', 'nim', 'gender', 'email', 'prodi', 'kelas', 'telepon', 'peran', 'ipk', 'minat','tingkatKemampuan', 'statusPrestasi']
    
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            values = dict(zip(keys, row))
        
            minat_list = values.pop('minat').split(',')
            minat_records = self.env['minat.data'].search([('minat_ids', 'in', minat_list)])
        
            values['minat'] = [(6, 0, minat_records.ids)]
        
            mahasiswa = self.env['mahasiswa.data'].search([('nim', '=', values['nim'])])
            if mahasiswa:
                mahasiswa.write(values)
            else:
                self.env['mahasiswa.data'].create(values)
            
        return {
            'name': 'Data Mahasiswa',
            'type': 'ir.actions.act_window',
            'res_model': 'mahasiswa.data',
            'view_mode': 'tree,form',
        }



# from odoo import api, models, fields
# import base64
# import io
# import csv
# from . import minat

# class Mahasiswa(models.Model):
#     _name = 'mahasiswa.data'
#     _rec_name = 'nama'
#     _description = 'Data Mahasiswa'

#     nama = fields.Char(string='Nama', required=True)
#     nim = fields.Char(string="NIM")
#     gender = fields.Selection([('Laki-laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], string="Jenis Kelamin")
#     email = fields.Char(string="Email")
#     prodi = fields.Selection([('D4 Sistem Informasi Bisnis', 'D4 Sistem Informasi Bisnis'), ('D4 Teknik Informatika', 'D4 Teknik Informatika')], string="Program Studi")
#     kelas = fields.Char(string="Kelas")
#     telepon = fields.Char(string="Telepon")

#     minat = fields.Many2many('minat.data', relation='mahasiswa_minat_rel', column1='mahasiswa_id', column2='minat_id', string='Minat / Keahlian')
#     tingkatKemampuan = fields.Integer(string="Tingkat Kemampuan Bidang")
#     statusPrestasi = fields.Selection([('Tidak', 'Tidak'), ('Ya', 'Ya')], string="Memiliki Prestasi")
#     peran = fields.Selection([('Hacker (Coding, Engineer, & Developer)', 'Hacker (Coding, Engineer, & Developer)'), ('Hipster (Desainer, UI & UX)', 'Hipster (Desainer, UI & UX)'), ('Hustler (Project Manager, Inisiator, Bisnis & Analyst)', 'Hustler (Project Manager, Inisiator, Bisnis & Analyst)')], string="Peran")
#     ipk = fields.Float(string='IPK')

#     @api.model
#     def create(self, vals):
#         record = super(Mahasiswa, self).create(vals)
#         self.env['spk.data'].create({'mahasiswa_id': record.id})
#         return record

#     def write(self, vals):
#         result = super(Mahasiswa, self).write(vals)
#         for record in self:
#             spk_record = self.env['spk.data'].search([('mahasiswa_id', '=', record.id)], limit=1)
#             if not spk_record:
#                 self.env['spk.data'].create({'mahasiswa_id': record.id})
#         return result
                
# class MahasiswaImportWizard(models.TransientModel):
#     _name = 'mahasiswa.import.wizard'
#     _description = 'Wizard untuk mengimpor data mahasiswa dari file csv'

#     csv_file = fields.Binary(string='File CSV', required=True)

#     def import_data(self):
#         csv_data = base64.b64decode(self.csv_file)
#         data_file = io.StringIO(csv_data.decode("utf-8"))
#         csv_reader = csv.reader(data_file, delimiter=',')
    
#         keys = ['nama', 'nim', 'gender', 'email', 'prodi', 'kelas', 'telepon', 'peran', 'ipk', 'minat','tingkatKemampuan', 'statusPrestasi']
    
#         for i, row in enumerate(csv_reader):
#             if i == 0:
#                 continue

#             values = dict(zip(keys, row))
        
#             minat_list = values.pop('minat').split(',')
#             minat_records = self.env['minat.data'].search([('minat_ids', 'in', minat_list)])
        
#             values['minat'] = [(6, 0, minat_records.ids)]
        
#             mahasiswa = self.env['mahasiswa.data'].search([('nim', '=', values['nim'])])
#             if mahasiswa:
#                 mahasiswa.write(values)
#             else:
#                 self.env['mahasiswa.data'].create(values)
            
#         return {
#             'name': 'Data Mahasiswa',
#             'type': 'ir.actions.act_window',
#             'res_model': 'mahasiswa.data',
#             'view_mode': 'tree,form',
#         }
