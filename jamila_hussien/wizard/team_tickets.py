# -*- coding: utf-8 -*-
###########
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *
from datetime import datetime



class Vehiclevehiclematriculation(models.Model):
    _name = 'team.ticket.report'
    _description = 'Ticket For Specific Team'

    team_id = fields.Many2one('hd.team','Team',required=True)
    state = fields.Selection([('draft','New'),('progress','In Progress'),('done','Done'),('cancel','Cancel')],
                           string='State')

    def print_report(self):
        for report in self:
            a = 1
            logo = report.env.user.company_id.logo
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            file_name = _('Team Ticket.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            report_title = 'Tickets for Team '
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'white', 'bg_color': '#0080ff', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '10'})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format.set_align('center')
            format.set_align('center')
            header_format_sequence.set_align('center')
            format.set_text_wrap()
            format.set_num_format('#,##0.000')
            sequence_format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            sequence_format.set_align('center')
            sequence_format.set_text_wrap()
            total_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#808080', 'border': 1, 'font_size': '10'})
            if self.state:
                excel_sheet = workbook.add_worksheet(self.state)
                excel_sheet.merge_range('A1:G1', report_title, title_format)
                col = 0
                row = 3
                excel_sheet.set_column(col, col, 25)
                excel_sheet.write(row, col, 'Ticket ID', header_format)
                col += 1
                excel_sheet.set_column(col, col, 25)
                excel_sheet.write(row, col, 'Name', header_format)
                col += 1
                excel_sheet.set_column(col, col, 25)
                excel_sheet.write(row, col, 'Time Submitted', header_format)
                col += 1
                excel_sheet.set_column(col, col, 20)
                excel_sheet.write(row, col, 'Priority', header_format)
                col += 1
                excel_sheet.set_column(col, col, 20)
                excel_sheet.write(row, col, 'Resolution Time', header_format)
                col += 1
                tickets = self.env['hd.ticket'].search([('state','=',self.state)])
                col = 0
                row += 1
                for tic in tickets:
                    excel_sheet.write(row, col,tic.sequence, format)
                    a = a + 1
                    col += 1
                    excel_sheet.write(row, col, tic.name, format)
                    col += 1
                    excel_sheet.write(row, col, tic.time_submit, format)
                    col += 1
                    excel_sheet.write(row, col, tic.priority, format)
                    col += 1
                    excel_sheet.write(row, col, tic.resolution_time, format)
                    col += 1
                    col = 0
                    row += 1
            else:
                    excel_sheet = workbook.add_worksheet('New')
                    excel_sheet1 = workbook.add_worksheet('In Progress')
                    excel_sheet2 = workbook.add_worksheet('Done')
                    excel_sheet3 = workbook.add_worksheet('Cancel')
                    excel_sheet.merge_range('A1:G1', report_title, title_format)
                    col = 0
                    row = 3
                    excel_sheet.set_column(col, col, 25)
                    excel_sheet.write(row, col, 'Ticket ID', header_format)
                    col += 1
                    excel_sheet.set_column(col, col, 25)
                    excel_sheet.write(row, col, 'Name', header_format)
                    col += 1
                    excel_sheet.set_column(col, col, 25)
                    excel_sheet.write(row, col, 'Time Submitted', header_format)
                    col += 1
                    excel_sheet.set_column(col, col, 20)
                    excel_sheet.write(row, col, 'Priority', header_format)
                    col += 1
                    excel_sheet.set_column(col, col, 20)
                    excel_sheet.write(row, col, 'Resolution Time', header_format)

                    tickets = self.env['hd.ticket'].search([('state', '=', 'draft')])
                    col = 0
                    row += 1
                    for tic in tickets:
                        excel_sheet.write(row, col, tic.sequence, format)
                        a = a + 1
                        col += 1
                        excel_sheet.write(row, col, tic.name, format)
                        col += 1
                        excel_sheet.write(row, col, str(tic.time_submit), format)
                        col += 1
                        excel_sheet.write(row, col, tic.priority, format)
                        col += 1
                        excel_sheet.write(row, col, tic.resolution_time, format)
                        col += 1
                        col = 0
                        row += 1
                    excel_sheet1.set_column(col, col, 25)
                    excel_sheet1.write(row, col, 'Ticket ID', header_format)
                    col += 1
                    excel_sheet1.set_column(col, col, 25)
                    excel_sheet1.write(row, col, 'Name', header_format)
                    col += 1
                    excel_sheet1.set_column(col, col, 25)
                    excel_sheet1.write(row, col, 'Time Submitted', header_format)
                    col += 1
                    excel_sheet1.set_column(col, col, 20)
                    excel_sheet1.write(row, col, 'Priority', header_format)
                    col += 1
                    excel_sheet1.set_column(col, col, 20)
                    excel_sheet1.write(row, col, 'Resolution Time', header_format)
                    col += 1
                    ticket_progress = self.env['hd.ticket'].search([('state', '=', 'progress')])
                    col = 0
                    row += 1
                    for tic in ticket_progress:
                        excel_sheet1.write(row, col, tic.sequence, format)
                        a = a + 1
                        col += 1
                        excel_sheet1.write(row, col, tic.name, format)
                        col += 1
                        excel_sheet1.write(row, col, str(tic.time_submit), format)
                        col += 1
                        excel_sheet1.write(row, col, tic.priority, format)
                        col += 1
                        excel_sheet1.write(row, col, tic.resolution_time, format)
                        col += 1
                        col = 0
                        row += 1
                    excel_sheet2.set_column(col, col, 25)
                    excel_sheet2.write(row, col, 'Ticket ID', header_format)
                    col += 1
                    excel_sheet2.set_column(col, col, 25)
                    excel_sheet2.write(row, col, 'Name', header_format)
                    col += 1
                    excel_sheet2.set_column(col, col, 25)
                    excel_sheet2.write(row, col, 'Time Submitted', header_format)
                    col += 1
                    excel_sheet2.set_column(col, col, 20)
                    excel_sheet2.write(row, col, 'Priority', header_format)
                    col += 1
                    excel_sheet2.set_column(col, col, 20)
                    excel_sheet2.write(row, col, 'Resolution Time', header_format)
                    col += 1
                    ticket_done = self.env['hd.ticket'].search([('state', '=', 'done')])
                    col = 0
                    row += 1
                    for tic in ticket_done:
                        excel_sheet2.write(row, col, tic.sequence, format)
                        a = a + 1
                        col += 1
                        excel_sheet2.write(row, col, tic.name, format)
                        col += 1
                        excel_sheet2.write(row, col, str(tic.time_submit), format)
                        col += 1
                        excel_sheet2.write(row, col, tic.priority, format)
                        col += 1
                        excel_sheet2.write(row, col, tic.resolution_time, format)
                    col += 1
                    col = 0
                    row += 1
                    excel_sheet3.set_column(col, col, 25)
                    excel_sheet3.write(row, col, 'Ticket ID', header_format)
                    col += 1
                    excel_sheet3.set_column(col, col, 25)
                    excel_sheet3.write(row, col, 'Name', header_format)
                    col += 1
                    excel_sheet3.set_column(col, col, 25)
                    excel_sheet3.write(row, col, 'Time Submitted', header_format)
                    col += 1
                    excel_sheet3.set_column(col, col, 20)
                    excel_sheet3.write(row, col, 'Priority', header_format)
                    col += 1
                    excel_sheet3.set_column(col, col, 20)
                    excel_sheet3.write(row, col, 'Resolution Time', header_format)
                    col += 1
                    ticket_cancel = self.env['hd.ticket'].search([('state', '=', 'cancel')])
                    col = 0
                    row += 1
                    for tic in ticket_cancel:
                        excel_sheet3.write(row, col, tic.sequence, format)
                        a = a + 1
                        col += 1
                        excel_sheet3.write(row, col, tic.name, format)
                        col += 1
                        excel_sheet3.write(row, col, str(tic.time_submit), format)
                        col += 1
                        excel_sheet3.write(row, col, tic.priority, format)
                        col += 1
                        excel_sheet3.write(row, col, tic.resolution_time, format)
                        col += 1
                        col = 0
                        row += 1
            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['team.ticket.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'team.ticket.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class TeamTicketExcel(models.TransientModel):
    _name = 'team.ticket.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)
