import base64
import csv
import io
from odoo import models, fields, api

class EventLomba(models.Model):
    _name = 'event.data'
    _rec_name = 'nama_event'
    _description = 'Data Event'

    nomor = fields.Char(string='Nomor', required=True)
    nama_event = fields.Char(string='Nama Event', required=True)
    deskripsi = fields.Text(string='Deskripsi', required=True)
    kategori = fields.Selection([
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Web Development', 'Web Development'),
        ('Game Development', 'Game Development'),
        ('Internet of Things', 'Internet of Things'),
        ('Robotics', 'Robotics'),
        ('Animation', 'Animation'),
        ('Business Plan', 'Business Plan'),
        ('Lainnya', 'Lainnya')
    ], string='Kategori Event', required=True)
    tanggal_pembukaan = fields.Date(string='Tanggal Pembukaan', required=True)
    tanggal_penutupan = fields.Date(string='Tanggal Penutupan', required=True)
    
    # Menambahkan field baru untuk upload gambar
    image = fields.Binary(string='Gambar Event', attachment=True, help='Unggah gambar event')
    image_filename = fields.Char(string='Nama File Gambar')

class EventImportWizard(models.TransientModel):
    _name = 'event.import.wizard'
    _description = 'Wizard untuk mengimpor data event dari file csv'

    csv_file = fields.Binary(string='File CSV', required=True)

    def import_data(self):
        csv_data = base64.b64decode(self.csv_file)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        csv_reader = csv.reader(data_file, delimiter=',')
    
        keys = ['nomor', 'nama_event', 'deskripsi', 'kategori', 'tanggal_pembukaan', 'tanggal_penutupan']
    
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            values = dict(zip(keys, row))
        
            event = self.env['event.data'].search([('nomor', '=', values['nomor'])])
            if event:
                event.write(values)
            else:
                self.env['event.data'].create(values)
            
        return {
            'name': 'Data Event',
            'type': 'ir.actions.act_window',
            'res_model': 'event.data',
            'view_mode': 'tree,form',
        }
