
from typing_extensions import Required
from odoo import api, fields, models
from datetime import timedelta, datetime, date    
class PaketPerjalanan(models.Model):
    _name = 'paket.perjalanan'
    _description = 'Travel Package'
    
    tanggal_berangkat = fields.Date(string="Tanggal Berangkat", required=True, states={'draft': [('readonly', False)]})
    tanggal_kembali = fields.Date(string="Tanggal Kembali", required=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', string="Sale", required=True, tracking=True, states={'draft': [('readonly', False)]})
    bom_id = fields.Many2one('product.product', string="Package",required=True,  tracking=True, states={'draft': [('readonly', False)]})
    
    #KUOTA
    quota = fields.Integer(string='Quota', help='Jumlah Quota', default=0, readonly=True, states={'draft': [('readonly', False)]})
    remaining_quota = fields.Integer(related='quota', string='Remaining Quota', store=True)
    quota_progress = fields.Float(string='Quota Progress', compute='compute_taken_quota', readonly=True, states={'draft': [('readonly', False)]})
    jamaah_ids = fields.Many2many('jamaah.package', 'package_jamaah_rel', 'paket_id', 'jamaah_id', 'Jamaah')
    
    hotel_line = fields.One2many('hotel.line', 'paket_id', string='Hotel Line', states={'draft': [('readonly', False)]})
    airline_line = fields.One2many('airline.line', 'paket_id', string='Airline Line', states={'draft': [('readonly', False)]}) 
    schedule_line = fields.One2many('schedule.line', 'paket_id', string='Schedule Line', states={'draft': [('readonly', False)]})
    hpp_line = fields.One2many('hpp.line', 'paket_id', string='HPP Line', states={'draft': [('readonly', False)]}) 
    manifest_paket_line = fields.One2many('manifest.paket', 'paket_id', string='Manifest Line', readonly=True, states={'draft': [('readonly', False)]})
    manipes = fields.One2many('sale.order', 'paket_id', string='')
    
    #REF
    name = fields.Char(compute='_compute_name', string='')
    ref = fields.Char(string='Referensi', readonly=True, default='-')
    total_cost = fields.Float(string='Total cost' , readonly=True ,store=True, compute='_compute_total_cost')
    
    @api.depends('quota', 'jamaah_ids')
    def compute_taken_quota(self):
        for sesi in self:
            sesi.quota_progress = 0
            if sesi.quota and sesi.jamaah_ids:
                sesi.quota_progress = 100 * \
                    len(sesi.jamaah_ids) / sesi.quota
    
    #ONCHANGE HPP
    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.bom_id.bom_ids.bom_line_ids:
                vals = {
                    'mrp_id': line.id,
                    'hpp_barang': line.display_name,
                    'hpp_qty': line.product_qty,
                    'uom_id': line.product_uom_id.id,
                    'hpp_price': line.product_id.standard_price,
                }
                lines.append((0, 0, vals))
            rec.hpp_line = lines
            
    @api.depends('hpp_line')
    def _compute_total_cost(self):
        for record in self:
            total = 0
            for line in record.hpp_line: 
                total += line.hpp_total
            record.total_cost = total
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')],
        string='Status', readonly=True, default='draft')
    
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('paket.perjalanan')
        return super(PaketPerjalanan, self).create(vals)
    
    @api.depends('ref','product_id')
    def _compute_name(self):
        for i in self:
            i.name = str(i.ref) +" - "+ str(i.product_id.name)
    
    def action_draft(self):
        self.write({'state': 'draft'})
        
    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_update(self):
        self.write({'state': 'confirm'})
        
    # @api.onchange('manipes')
    # def action_update(self):
        # print('========================================',self.manipes.manifest_sale_line.partner_id.nama_passpor)
        # for rec in self:
        #     lines = [(5, 0, 0)]
        #     for line in self.manipes.manifest_sale_line:
        #         vals = {
        #             'partner_id': line.id,
        #             'title': line.partner_id.title.name,
        #             'ktp': line.ktp,
        #         }
        #         lines.append((0, 0, vals))
        #     print("============================" ,lines)
        #     rec.manifest_paket_line = lines
        
class JamaahPackage(models.Model):
    _name = 'jamaah.package'
    _inherits = {'res.partner': 'jamaah_id'}

    jamaah_id = fields.Many2one('res.partner', 'Jamaah', required=True, ondelete='cascade')

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
    
class ManifestPaket(models.Model):
    _name = 'manifest.paket'
    _description = 'Manifest Paket'
    
    paket_id = fields.Many2one('paket.perjalanan', string='Manifest Paket')
    partner_id = fields.Many2one('res.partner', string='Nama Jamaah')
    title = fields.Char(string='Title', Required=True, related='partner_id.title.name')
    nama_passpor = fields.Char(string='Nama Passpor', related='partner_id.nama_passpor')
    jenis_kelamin = fields.Selection([
        ('laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin', help='Gender', related='partner_id.jenis_kelamin')
    ktp = fields.Char(string='No.KTP', related='partner_id.ktp')
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
    hpp_total = fields.Float(string='Sub Total', compute='_compute_total_cost')
    
    #FUNCTION QUANTITY * PRICE
    @api.depends('hpp_qty')
    def _compute_total_cost(self):
        for hpp in self:
            hpp.hpp_total = 0
            if hpp.hpp_qty and hpp.hpp_price :
                hpp.hpp_total = hpp.hpp_qty * hpp.hpp_price