from odoo import api, fields, models
 
class UmrohTravel(models.Model):
    _name = 'umroh.travel'
    _description = 'Umroh Travel'
     
    name = fields.Char(string='Judul', required=True)
    description = fields.Text(string='Keterangan')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
            
class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'
    
    tanggal_berangkat = fields.Date(string="Tanggal Berangkat")
    tanggal_kembali = fields.Date(string="Tanggal Kembali")
    sale = fields.Many2one('product_id', string="Produk", tracking=True)

