from odoo import api, fields, models
from datetime import timedelta, datetime, date    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    paket_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan', domain=[('state', '=', 'confirm')])
    manifest_sale_line = fields.One2many('manifest.sale', 'sale_id', string='')
    
    @api.onchange('paket_id')
    def _onchange_paket_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.paket_id.product_id:
                vals = {
                    'product_id': line.id,
                    'name': line.name,
                    'product_uom': line.uom_id,
                    'price_unit': line.list_price
                }
                lines.append((0, 0, vals))
            rec.order_line = lines
            
class ManifestSale(models.Model):
    _name = 'manifest.sale'
    _description = 'Manifest Sale'
    
    sale_id = fields.Many2one('sale.order', string='Manifest Sale')
    partner_id = fields.Many2one('res.partner', string='Nama Jamaah')
    title = fields.Char(string='Title', Required=True, related='partner_id.title.name')
    nama_passpor = fields.Char(string='Nama Passpor', related='partner_id.nama_passpor')
    jenis_kelamin = fields.Selection([
        ('Laki-Laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin',related='partner_id.jenis_kelamin', help='Gender')
    ktp = fields.Char(string='No.KTP', related='partner_id.ktp')
    no_passpor = fields.Char(string='No.Passpor', related='partner_id.no_passpor')
    tanggal_lahir = fields.Date(string='Tanggal Lahir', related='partner_id.tanggal_lahir')
    tempat_lahir = fields.Char(string='Tempat Lahir', related='partner_id.tempat_lahir')
    tanggal_berlaku = fields.Date(string='Tanggal Berlaku', related='partner_id.tanggal_berlaku')
    tanggal_habis = fields.Date(string='Tanggal Expired', related='partner_id.tanggal_habis')
    imigrasi = fields.Char(string='Imigrasi', related='partner_id.imigrasi')
    tipe_kamar = fields.Selection([
        ('double', 'Double'), 
        ('triple', 'Triple'), 
        ('quad', 'Quad')], 
        string='Tipe Kamar', default='quad', required=True)
    umur = fields.Char(string='Umur', related='partner_id.umur')
    mahram_id = fields.Many2one('res.partner', string='Mahram')
    notes = fields.Char(string='Notes') 
    
    gambar_passpor = fields.Image(string="Scan Passpor", related='partner_id.gambar_passpor')
    gambar_ktp = fields.Image(string="Scan KTP", related='partner_id.gambar_ktp')
    gambar_bukuk_nikah = fields.Image(string="Scan Buku Nikah", related='partner_id.gambar_bukuk_nikah')
    gambar_kartu_keluarga = fields.Image(string="Scan Kartu Keluarga", related='partner_id.gambar_kartu_keluarga')
    