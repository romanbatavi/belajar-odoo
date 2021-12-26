from odoo import fields, models, api
from datetime import timedelta, datetime, date
from dateutil import relativedelta
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell


class ReportManifestXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_manifest_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        
        # text_style = workbook.add_format({'font_size': 10, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter', 
        # 'text_wrap': True, })
        # sub_header = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'size': 11, 'bold': True})
        # cell_text_format = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bold': True, 'size': 12})
        # cell_text_format_top_left_right = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'size': 11, 'top': 1,
        # 'left': 1, 'right': 1, 'bottom': 1})
        # cell_text_format_top_left_right.set_bg_color('#80a7fa')
        # worksheet = workbook.add_worksheet('Laporan Pinjaman Karyawan')
        
        worksheet = workbook.add_worksheet('Travel Package %s' % obj.name)
        text_style = workbook.add_format({'font_size': 10, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        text_top_style = workbook.add_format({'font_size': 10, 'bold': True ,'font_color' : 'white', 'bg_color': '#00348A', 'valign': 'vcenter', 'text_wrap': True})
        text_header_style = workbook.add_format({'font_size': 10, 'bold': True ,'font_color' : 'white', 'bg_color': '#00348A', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        
        worksheet.write(0, 1, "REPORT MANIFEST", text_top_style)
        worksheet.write(0, 3, obj.ref)
        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 2, 10)#
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 16, 10)
        
        row = 5
        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 9, 15)
        header = ['NO', 'TITLE','GENDER' , 'FULLNAME', 'TEMPAT LAHIR', 'TANGGAL LAHIR','NO.PASSPOR', 'PASSPOR ISSUED', 'PASSPOR EXPIRED','IMIGRASI','MAHROM','USIA','NIK','ORDER','ROOM TYPE','ROOM LEADER','NO.ROOM','ALAMAT']
        worksheet.write_row(row, 0, header, text_header_style)
        
        no_list = []
        title = []
        gender = []
        fullname = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passpor = []
        passpor_issued = []
        passpor_expired = []
        imigrasi = []
        mahrom = []
        usia = []
        nik = []
        order = []
        room_type = []
        room_leader = []
        no_room = []
        alamat = []
        
        no = 1
        for x in obj.manifest_paket_line:
            no_list.append(no)
            title.append(x.title or '')
            gender.append(x.jenis_kelamin)
            fullname.append(x.nama_passpor)
            tempat_lahir.append(x.tempat_lahir)
            tanggal_lahir.append(x.tanggal_lahir.strftime('%d-%m-%Y') if x.tanggal_lahir else '')
            no_passpor.append(x.no_passpor)
            passpor_issued.append(x.tanggal_berlaku.strftime('%d-%m-%Y') if x.tanggal_berlaku else '')
            passpor_expired.append(x.tanggal_habis.strftime('%d-%m-%Y') if x.tanggal_habis else '')
            imigrasi.append(x.imigrasi)
            usia.append(x.umur)
            nik.append(x.ktp)
            # order.append(x.ref)
            mahrom.append(x.mahram_id if x.mahram_id else '-')
            room_type.append(x.tipe_kamar)
            alamat.append(x.partner_id.city)
            no+=1
            
        row += 1
        worksheet.write_column(row, 0, no_list, text_style)
        worksheet.write_column(row, 1, title, text_style)
        worksheet.write_column(row, 2, gender, text_style)
        worksheet.write_column(row, 3, fullname, text_style)
        worksheet.write_column(row, 4, tempat_lahir, text_style)
        worksheet.write_column(row, 5, tanggal_lahir, text_style)
        worksheet.write_column(row, 6, no_passpor, number_style)
        worksheet.write_column(row, 7, passpor_issued, number_style)
        worksheet.write_column(row, 8, passpor_expired, number_style)
        worksheet.write_column(row, 9, imigrasi, text_style)
        worksheet.write_column(row, 10, mahrom, text_style)
        worksheet.write_column(row, 11, usia, text_style)
        worksheet.write_column(row, 12, nik, text_style)
        worksheet.write_column(row, 13, order, text_style)
        worksheet.write_column(row, 14, room_type, text_style)
        worksheet.write_column(row, 15, room_leader, text_style)
        worksheet.write_column(row, 16, no_room, text_style)
        worksheet.write_column(row, 17, alamat, text_style)
        
        bawah = no
        row = 5 + bawah
        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 9, 15)
        header = ['NO', 'AIRLINE','DEPARTURE DATE' , 'DEPARTURE CITY', 'ARIVAL CITY']
        worksheet.write_row(row, 2, header, text_header_style)

        nomer = []
        airline = []
        departure_date = []
        departure_city = []
        arrival_city = []

        nomr = 1
        for a in obj.airline_line:
            nomer.append(nomr)
            airline.append(a.partner_id.name)
            departure_date.append(a.tanggal_berangkat.strftime('%d-%m-%Y') if a.tanggal_berangkat else '')
            departure_city.append(a.kota_asal)
            arrival_city.append(a.kota_tujuan)

            nomr+=1
    
        row += 1
        worksheet.write_column(row, 2, nomer, text_style)
        worksheet.write_column(row, 3, airline, text_style)
        worksheet.write_column(row, 4, departure_date, text_style)
        worksheet.write_column(row, 5, departure_city, text_style)
        worksheet.write_column(row, 6, arrival_city, text_style)

        