from odoo import fields, models, api
from datetime import timedelta, datetime, date
from dateutil import relativedelta
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell


class CicilanReportXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_manifest_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        
        text_style = workbook.add_format({'font_size': 10, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter', 
        'text_wrap': True, })
        sub_header = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'size': 11, 'bold': True})
        cell_text_format = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bold': True, 'size': 12})
        cell_text_format_top_left_right = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'size': 11, 'top': 1,
        'left': 1, 'right': 1, 'bottom': 1})
        cell_text_format_top_left_right.set_bg_color('#80a7fa')
        worksheet = workbook.add_worksheet('Report Manifest')
        
        # worksheet.set_column('A:B', 20)
        # worksheet.set_column(1, 1, 30)
        
        # worksheet.write(2, 1, 'Isi', text_style)
        
        # worksheet.merge_range(4, 0, 5, 0, 'NO', cell_text_format_top_left_right)
        # worksheet.merge_range('D1:F2', 'LAPORAN PINJAMAN KARYAWAN', heading_format)
        
        