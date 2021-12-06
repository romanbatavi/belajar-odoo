from odoo import api, fields, models
 
class Partner(models.Model):
    _inherit = 'res.partner'
 
    ktp = fields.Char(string='KTP')
    ayah = fields.Char(string='Ayah')
