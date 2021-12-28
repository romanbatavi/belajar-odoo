
from typing_extensions import Required
from odoo import api, fields, models
from datetime import timedelta, datetime, date    
class PaketPerjalanan(models.Model):
    _name = 'paket.perjalanan'
    _description = 'Travel Package'
    
    tanggal_berangkat = fields.Date(string="Tanggal Berangkat",required=True, readonly=True, states={'draft': [('readonly', False)]})
    tanggal_kembali = fields.Date(string="Tanggal Kembali", required=True, readonly=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', string="Sale", readonly=True,required=True, states={'draft': [('readonly', False)]})
    bom_id = fields.Many2one('product.product', string="Package", readonly=True, required=True, states={'draft': [('readonly', False)]})
    
    #KUOTA
    quota = fields.Integer(string='Quota', help='Jumlah Quota', readonly=True, states={'draft': [('readonly', False)]})
    remaining_quota = fields.Integer(related='quota', string='Remaining Quota', store=True)
    quota_progress = fields.Integer(string='Quota Progress', compute='_compute_seats', readonly=True)
    
    hotel_line = fields.One2many('hotel.line', 'paket_id', string='Hotel Line',readonly=True, states={'draft': [('readonly', False)]})
    airline_line = fields.One2many('airline.line', 'paket_id', string='Airline Line') 
    schedule_line = fields.One2many('schedule.line', 'paket_id', string='Schedule Line')
    hpp_line = fields.One2many('hpp.line', 'paket_id', string='HPP Line') 
    manifest_paket_line = fields.One2many('manifest.paket', 'paket_id', string='Manifest Line', readonly=True)
    
    manifest_line = fields.One2many('sale.order', 'paket_id', string='Penghubung Antar Manifest')
    
    #REF
    name = fields.Char(string='Referensi', readonly=True, default='-')
    total_cost = fields.Float(string='Total cost' , readonly=True ,store=True, compute='_compute_total_cost')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')],
        string='Status', readonly=True, default='draft')
    
    @api.depends('quota','manifest_paket_line')
    def _compute_seats(self):
        for rec in self:
            rec.quota_progress = 0
            if rec.manifest_paket_line and rec.quota:
                rec.remaining_quota = rec.quota - len(rec.manifest_paket_line)
                rec.quota_progress = 100 * len(rec.manifest_paket_line) / rec.quota
    
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
            
    def name_get(self):
        listget = []
        for record in self:
            name = (record.name)+' - '+(record.product_id.name)
            listget.append((record.id, name))
        return listget
            
    
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
    
    def action_update(self):
        self.write({'state': 'confirm'})
    
    def action_report_excel(self):
        template_report = 'ab_travel_umroh.report_manifest_xlsx'
        return self.env.ref(template_report).report_action(self)
    
    def action_update(self):
        for rec in self:
            lines = [(5, 0, 0)]
            asd =  self.env['sale.order'].search([('paket_id', '=', self.id),('state', '=', 'sale')])
            for x in asd:
                for a in x.manifest_sale_line:
                    vals = {
                        'partner_id': a.partner_id.id,
                        'title': a.partner_id.title.name,
                        'ktp': a.partner_id.ktp,
                        'nama_passpor': a.partner_id.nama_passpor,
                        'jenis_kelamin': a.partner_id.jenis_kelamin,
                        'no_passpor': a.partner_id.no_passpor,
                        'tanggal_lahir': a.partner_id.tanggal_lahir,
                        'tempat_lahir': a.partner_id.tempat_lahir,
                        'tanggal_berlaku': a.partner_id.tanggal_berlaku,
                        'tanggal_habis': a.partner_id.tanggal_habis,
                        'imigrasi': a.partner_id.imigrasi,
                        'umur': a.partner_id.umur,
                        'tipe_kamar': a.tipe_kamar,
                        'order_id': a.id,
                        'mahram_id': a.mahram_id.id
                    }
                    lines.append((0, 0, vals))
                rec.manifest_paket_line = lines
            
class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'
    
    partner_id = fields.Many2one('res.partner', required=True, string='Nama Hotel', domain=[('hotels', '=', True)])
    paket_id = fields.Many2one('paket.perjalanan', string='Hotel Line')
    nama_kota = fields.Char(string='Nama Kota', related='partner_id.city', tracking=True)
    tanggal_masuk = fields.Date(string='Tanggal Masuk')
    tanggal_keluar = fields.Date(string='Tanggal Keluar')
    
class AirlineLine(models.Model):
    _name = 'airline.line'
    _description = 'Airline Line'
    
    partner_id = fields.Many2one('res.partner', required=True, string='Nama Pesawat', domain=[('airlines', '=', True)])
    paket_id = fields.Many2one('paket.perjalanan', String='Airline Line')
    tanggal_berangkat = fields.Date(string='Tanggal Keberangkatan')
    kota_asal = fields.Char(string='Kota Asal')
    kota_tujuan = fields.Char(string='Kota Tujuan')
    
class ScheduleLine(models.Model):
    _name = 'schedule.line'
    _description = 'Schedule Line'
    
    schedule = fields.Char(string='Nama Kegiatan',required=True)
    paket_id = fields.Many2one('paket.perjalanan', string='Hotel Line')
    tanggal_kegiatan = fields.Date(string='Tanggal Kegiatan')
    
class ManifestPaket(models.Model):
    _name = 'manifest.paket'
    _description = 'Manifest Paket'
    
    paket_id = fields.Many2one('paket.perjalanan', required=True, string='Manifest Paket')
    order_id = fields.Many2one('sale.order', required=True, string='Manifest Paket')
    partner_id = fields.Many2one('res.partner', string='Nama Jamaah')
    title = fields.Char(string='Title', required=True, related='partner_id.title.name')
    nama_passpor = fields.Char(string='Nama Passpor', related='partner_id.nama_passpor')
    jenis_kelamin = fields.Selection([
        ('Laki-Laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin', help='Gender', related='partner_id.jenis_kelamin')
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