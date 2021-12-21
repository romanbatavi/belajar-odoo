from odoo import api, fields, models
from datetime import timedelta, datetime, date
 
class Partner(models.Model):
    _inherit = 'res.partner'
 
    # ADDICTIONAL INFORMATION
    ktp = fields.Char(string='No.KTP')
    ayah = fields.Char(string='Nama Ayah')
    pekerjaan_ayah = fields.Char(string='Pekerjaan Ayah')
    tempat_lahir = fields.Char(string='Tempat Lahir')
    pendidikan = fields.Selection([
        ('sd', 'Sekolah Dasar'), 
        ('smp', 'Sekolah Menengah Pertama'), 
        ('sma', 'Sekolah Menengah Atas/Kejuruan'),
        ('d3', 'Diploma 3'), 
        ('s1', 'S1'), 
        ('s2', 'S2'), 
        ('s3', 'S3')], 
        string='Pendidikan', help='Pendidikan Terakhir')
    status_hubungan = fields.Selection([
        ('single', 'Belum Menikah'), 
        ('married', 'Menikah'), 
        ('divorced', 'Cerai')], 
        string='Status Pernikahan', help='Status Pernikahan')
    jenis_kelamin = fields.Selection([
        ('laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin', help='Gender')
    ibu = fields.Char(string='Nama Ibu')
    pekerjaan_ibu = fields.Char(string='Pekerjaan Ibu')
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    golongan_darah = fields.Selection([
        ('a', 'A'), 
        ('b', 'B'), 
        ('ab', 'AB'), 
        ('o', 'O')], 
        string='Golongan Darah', help='Golongan Darah')
    ukuran_baju = fields.Selection([
        ('xs', 'XS'), 
        ('s', 'S'), 
        ('m', 'M'), 
        ('l', 'L'), 
        ('xl', 'XL'), 
        ('xxl', 'XXL'), 
        ('xxxl', 'XXXL'), 
        ('4l', '4L')], 
        string='Ukuran Baju', help='Ukuran Baju')
    
    #TRIGGER UMUR SALE ORDER
    umur = fields.Char(compute='_compute_umur', string='Umur')
    
    @api.depends('tanggal_lahir')
    def _compute_umur(self):
        today_date = date.today()
        for usia in self:
            usia.umur=today_date.year - usia.tanggal_lahir.year
    
    # PASSPOR INFORMATION
    no_passpor = fields.Char(string='No.Passpor')
    tanggal_berlaku = fields.Date(string='Tanggal Berlaku')
    imigrasi = fields.Char(string='Imigrasi')
    nama_passpor = fields.Char(string='Nama Passpor')
    tanggal_habis = fields.Date(string='Tanggal Habis')
    
    # SCAN DOCUMENT
    gambar_passpor = fields.Image(string="Scan Passpor")
    gambar_ktp = fields.Image(string="Scan KTP")
    gambar_bukuk_nikah = fields.Image(string="Scan Buku Nikah")
    gambar_kartu_keluarga = fields.Image(string="Scan Kartu Keluarga")
    
    #LOGIC TEXTBOOK
    airlines = fields.Boolean(string='Airlines')
    hotels = fields.Boolean(string='Hotel')