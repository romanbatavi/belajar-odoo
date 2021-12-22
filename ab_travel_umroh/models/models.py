
from typing_extensions import Required
from odoo import api, fields, models         
class PaketPerjalanan(models.Model):
    _name = 'paket.perjalanan'
    _description = 'Travel Package'
    
    tanggal_berangkat = fields.Date(string="Tanggal Berangkat", required=True)
    tanggal_kembali = fields.Date(string="Tanggal Kembali", required=True)
    product_id = fields.Many2one('product.product', string="Sale", required=True, tracking=True)
    bom_id = fields.Many2one('product.product', string="Package",required=True,  tracking=True)
    quota = fields.Integer(string="Quota")
    remaining_quota = fields.Integer(string="Remaining Quota", related='quota')
    quota_progress = fields.Integer(string="Quota Progress")
    
    hotel_line = fields.One2many('hotel.line', 'paket_id', string='Hotel Line')
    airline_line = fields.One2many('airline.line', 'paket_id', string='Airline Line') 
    schedule_line = fields.One2many('schedule.line', 'paket_id', string='Schedule Line')
    hpp_line = fields.One2many('hpp.line', 'paket_id', string='HPP Line') 
    manifest_line = fields.One2many('manifest.line', 'paket_id', string='Manifest Line', readonly=True)
    name = fields.Char(string='Referensi', readonly=True, default='-')
    # total_cost = fields.Float(compute='_compute_total_cost', string='Total', readonly=True)
    
    #ONCHANGE HPP
    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            total = 0
            for line in self.bom_id.bom_ids.bom_line_ids:
                # total += line.product_qty * line.product_id.standard_price
                vals = {
                    'mrp_id': line.id,
                    'hpp_barang': line.display_name,
                    'hpp_qty': line.product_qty,
                    'uom_id': line.product_uom_id.id,
                    'hpp_price': line.product_id.standard_price,
                }
                lines.append((0, 0, vals))
            rec.hpp_line = lines
            # rec.total_cost = total
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')],
        string='Status', readonly=True, default='draft')
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('paket.perjalanan')
        return super(PaketPerjalanan, self).create(vals)
    
    def action_draft(self):
        self.write({'state': 'draft'})
        
    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    def action_done(self):
        self.write({'state': 'done'})

class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'
    
    partner_id = fields.Many2one('res.partner', string='Nama Hotel', domain=[('hotels', '=', True)])
    paket_id = fields.Many2one('paket.perjalanan', string='Hotel Line')
    nama_kota = fields.Char(string='Nama Kota', related='partner_id.city', tracking=True,)
    tanggal_masuk = fields.Date(string='Tanggal Masuk')
    tanggal_keluar = fields.Date(string='Tanggal Keluar')
    
class AirlineLine(models.Model):
    _name = 'airline.line'
    _description = 'Airline Line'
    
    partner_id = fields.Many2one('res.partner', string='Nama Pesawat', domain=[('airlines', '=', True)])
    paket_id = fields.Many2one('paket.perjalanan', String='Airlines Line')
    tanggal_berangkat = fields.Date(string='Tanggal Keberangkatan')
    kota_asal = fields.Char(string='Kota Asal')
    kota_tujuan = fields.Char(string='Kota Tujuan')
    
class ScheduleLine(models.Model):
    _name = 'schedule.line'
    _description = 'Schedule Line'
    
    schedule = fields.Char(string='Nama Kegiatan')
    paket_id = fields.Many2one('paket.perjalanan', string='Hotel Line')
    tanggal_kegiatan = fields.Date(string='Tanggal Kegiatan')
    
class ManifestLine(models.Model):
    _name = 'manifest.line'
    _description = 'Manifest Line'
    
    paket_id = fields.Many2one('paket.perjalanan', string='Manifest')
    sale_id = fields.Many2one('sale.order', string='Manifest')
    partner_id = fields.Many2one('res.partner', string='Nama Jamaah')
    title = fields.Char(string='Title', Required=True, related='partner_id.title.name')
    nama_passpor = fields.Char(string='Nama Passpor', related='partner_id.nama_passpor')
    jenis_kelamin = fields.Selection([
        ('laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin', help='Gender')
    no_ktp = fields.Char(string='No.KTP', related='partner_id.ktp')
    passpor = fields.Char(string='No.Passpor', related='partner_id.no_passpor')
    tanggal_lahir = fields.Date(string='Tanggal Lahir', related='partner_id.tanggal_lahir')
    tempat_lahir = fields.Char(string='Tempat Lahir', related='partner_id.tempat_lahir')
    tanggal_berlaku = fields.Date(string='Tanggal Berlaku', related='partner_id.tanggal_berlaku')
    tanggal_expired = fields.Date(string='Tanggal Expired', related='partner_id.tanggal_habis')
    imigrasi = fields.Char(string='Imigrasi', related='partner_id.imigrasi')
    tipe_kamar = fields.Selection([
        ('double', 'Double'), 
        ('triple', 'Triple'), 
        ('quad', 'Quad')], 
        string='Tipe Kamar', default='quad', required=True)
    umur = fields.Char(string='Umur', related='partner_id.umur')
    mahram_id = fields.Many2one('res.partner', string='Mahram')
    agent = fields.Char(string='Agent')
    notes = fields.Char(string='Notes') 
    
    gambar_passpor = fields.Image(string="Scan Passpor", related='partner_id.gambar_passpor')
    gambar_ktp = fields.Image(string="Scan KTP", related='partner_id.gambar_ktp')
    gambar_bukuk_nikah = fields.Image(string="Scan Buku Nikah", related='partner_id.gambar_bukuk_nikah')
    gambar_kartu_keluarga = fields.Image(string="Scan Kartu Keluarga", related='partner_id.gambar_kartu_keluarga')
        
class HppLine(models.Model):
    _name = 'hpp.line'
    _description = 'HPP Line'
    
    paket_id = fields.Many2one('paket.perjalanan', string='HPP ID')
    mrp_id = fields.Many2one('mrp.bom', string='Barang')
    hpp_barang = fields.Char(string='Nama Barang')
    hpp_qty = fields.Float(string='Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit(s)')
    hpp_price = fields.Float(string='Unit Price')
    hpp_sub_total = fields.Float(compute='_compute_hpp_sub_total', string='Sub Total', readonly=True)
    #FUNCTION QUANTITY * PRICE
    @api.depends('hpp_qty','hpp_price')
    def _compute_hpp_sub_total(self):
        for subtot in self:
            subtot.hpp_sub_total = 0
            if subtot.hpp_qty and subtot.hpp_price:
                subtot.hpp_sub_total = subtot.hpp_qty * subtot.hpp_price
                
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    paket_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan')
    manifest_line = fields.One2many('manifest.line', 'sale_id', string='Passport Line')
    