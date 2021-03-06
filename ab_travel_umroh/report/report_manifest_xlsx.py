from odoo import fields, models, api
from datetime import timedelta, datetime, date
from dateutil import relativedelta
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell


class ReportManifestXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_manifest_xlsx'
    _description = 'Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        
        worksheet = workbook.add_worksheet('Travel Package %s' % obj.name)
        text_style = workbook.add_format({'font_size': 10, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        name_style = workbook.add_format({'font_size': 10, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        tanggal_style = workbook.add_format({'num_format': '#,##0', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        text_top_style = workbook.add_format({'font_size': 10, 'bold': True , 'align': 'center', 'font_color' : 'white', 'bg_color': '#00348A', 'valign': 'vcenter', 'text_wrap': True})
        text_header_style = workbook.add_format({'font_size': 10, 'bold': True ,'font_color' : 'white', 'bg_color': '#00348A', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        tanggal_style.set_num_format('d mmmm yyyy') 
        
        #GET OBJECT
        worksheet.write(0, 2, "MANIFEST", text_top_style)
        worksheet.write(0, 3, obj.name, name_style)
        
        #BORDER
        text_style.set_border(3)
        number_style.set_border(3)
        tanggal_style.set_border(3)
        text_top_style.set_border(3)
        name_style.set_border(3)
        
        #SET FIELD
        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 2, 10)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 16, 10)
        
        #FIELD MANIFEST
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
            gender.append(x.partner_id.jenis_kelamin)
            fullname.append(x.nama_passpor)
            tempat_lahir.append(x.tempat_lahir)
            tanggal_lahir.append(x.tanggal_lahir if x.tanggal_lahir else '')
            no_passpor.append(x.no_passpor)
            passpor_issued.append(x.tanggal_berlaku if x.tanggal_berlaku else '')
            passpor_expired.append(x.tanggal_habis if x.tanggal_habis else '')
            imigrasi.append(x.imigrasi)
            usia.append(x.umur)
            nik.append(x.ktp)
            order.append(x.order_id.name)
            mahrom.append(x.mahram_id.name if x.mahram_id else '-')
            room_type.append(x.tipe_kamar)
            room_leader.append('-')
            no_room.append('-')
            alamat.append(x.partner_id.city)
            no+=1
            
        row += 1
        worksheet.write_column(row, 0, no_list, text_style)
        worksheet.write_column(row, 1, title, text_style)
        worksheet.write_column(row, 2, gender, text_style)
        worksheet.write_column(row, 3, fullname, text_style)
        worksheet.write_column(row, 4, tempat_lahir, text_style)
        worksheet.write_column(row, 5, tanggal_lahir, tanggal_style)
        worksheet.write_column(row, 6, no_passpor, number_style)
        worksheet.write_column(row, 7, passpor_issued, tanggal_style)
        worksheet.write_column(row, 8, passpor_expired, tanggal_style)
        worksheet.write_column(row, 9, imigrasi, text_style)
        worksheet.write_column(row, 10, mahrom, text_style)
        worksheet.write_column(row, 11, usia, text_style)
        worksheet.write_column(row, 12, nik, text_style)
        worksheet.write_column(row, 13, order, text_style)
        worksheet.write_column(row, 14, room_type, text_style)
        worksheet.write_column(row, 15, room_leader, text_style)
        worksheet.write_column(row, 16, no_room, text_style)
        worksheet.write_column(row, 17, alamat, text_style)
        
        #FIELD AIRLINE
        bawah = no
        row = 7 + bawah
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
            departure_date.append(a.tanggal_berangkat if a.tanggal_berangkat else '')
            departure_city.append(a.kota_asal)
            arrival_city.append(a.kota_tujuan)
            nomr+=1
    
        row += 1
        worksheet.write_column(row, 2, nomer, text_style)
        worksheet.write_column(row, 3, airline, text_style)
        worksheet.write_column(row, 4, departure_date, tanggal_style)
        worksheet.write_column(row, 5, departure_city, text_style)
        worksheet.write_column(row, 6, arrival_city, text_style)

        