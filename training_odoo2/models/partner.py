from odoo import api, fields, models
 
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
    tanggal_lahir = fields.Date(string='Tanggal_Lahir')
    golongan_darah = fields.Selection([
        ('a', 'A'), 
        ('b', 'B'), 
        ('ab', 'AB'), 
        ('o', 'O')], 
        string='Golongan Darah', help='Golongan Darah')
    baju = fields.Selection([
        ('xs', 'XS'), 
        ('s', 'S'), 
        ('m', 'M'), 
        ('l', 'L'), 
        ('xl', 'XL'), 
        ('xxl', 'XXL'), 
        ('xxxl', 'XXXL'), 
        ('4l', '4L')], 
        string='Ukuran Baju', help='Ukuran Baju')
    
    # PASSPOR INFORMATION
    passpor = fields.Char(string='No.Passpor')
    tanggal_akpass = fields.Date(string='Tanggal Berlaku')
    imigrasi = fields.Char(string='Imigrasi')
    nama_passpor = fields.Char(string='Nama Passpor')
    tanggal_habpass = fields.Date(string='Tanggal Habis')
    
    # SCAN DOCUMENT
    gambar_pass = fields.Image(string="Scan Passpor")
    gambar_ktp = fields.Image(string="Scan KTP")
    gambar_bknikah = fields.Image(string="Scan Buku Nikah")
    gambar_kk = fields.Image(string="Scan Kartu Keluarga")
    
    airlines = fields.Boolean(string='Airlines')
    hotels = fields.Boolean(string='Hotel')
    
    