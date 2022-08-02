import ast
import datetime

from dateutil import relativedelta
from odoo import api, fields, models, _
from odoo.addons.helpdesk.models.helpdesk_ticket import TICKET_PRIORITY
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from random import randint


class Tickets(models.Model):
    _name = "hd.ticket"
    _inherit = [ 'mail.thread', 'mail.activity.mixin']
    _description = "Create Tickets for Help Desk Team "



    name = fields.Char(string='Subject', required=True, index=True, track=True)
    description = fields.Text('Description', track=True,required=True)
    sequence = fields.Char("Sequence",default=lambda self: _('New'),readonly=True)
    team_id = fields.Many2one('hd.team', string='Helpdesk Team', index=True,required=True)
    assign_to = fields.Many2many('res.users', string='Assign To',domain=[('team_id','=',team_id)])
    priority=fields.Selection([('low','Low'),('medium','Medium'),('high','High')],string='Priority')
    tag_ids=fields.Many2many('hd.tags', string='Tags')
    time_submit=fields.Datetime(string="Open Date", default=lambda *a: datetime.datetime.now())
    partner_id=fields.Many2one('res.partner', string='Customer',required=True)
    partner_name=fields.Char(string='Customer Name', related='partner_id.name')
    partner_email=fields.Char(string='Customer Email', related='partner_id.email')
    customer_phone=fields.Char(string='Customer Phone', related='partner_id.phone')
    host_type=fields.Selection([('premise','On-Premise'),('cloud','Cloud')],string='Host Type',
                               default='premise',required=True)
    server_url=fields.Char(string='Server URL', track=True,required=True)
    resolution_time=fields.Float(string='Resolution Time',track=True,readonly=True)
    state=fields.Selection([('draft','New'),('progress','In Progress'),('done','Done'),('cancel','Cancel')],
                           string='Status', index=True, readonly=True, default='draft',
                           track_visibility='onchange', copy=False)

    @api.model
    def create(self, vals):
        ticket = super(Tickets, self).create(vals)
        for x in ticket:
            if vals.get('sequence', 'New') == 'New':
                x.sequence = x.team_id.name + '/' + 'No.'+self.env['ir.sequence'].next_by_code('ticket.no') or 'New'
        return ticket

    def unlink(self):
        for x in self:
            if any(x.filtered(lambda ticket: ticket.state not in ('draft', 'cancel'))):
                raise UserError(_('You cannot delete a Record which is not draft or cancelled!'))
            return super(Tickets, x).unlink()

    def in_progress(self):
        self.write({'state': 'progress'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_done(self):
        day=datetime.datetime.now().day - self.time_submit.day
        print('tttttttt',day)
        self.write({'state': 'done'})
        self.write({'resolution_time': day})



class Tags(models.Model):
    _name='hd.tags'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

class Partner(models.Model):
    _inherit='res.partner'

    open_ticket=fields.Integer('Tickets',compute='get_tickets',tracking=True)

    def get_tickets(self):
        tickets_id = self.env['hd.ticket'].search([('partner_id', '=', self.id)])
        self.open_ticket = len(tickets_id)

class Users(models.Model):
    _inherit='res.users'

    assign_ticket=fields.Integer('Tickets',compute='get_tickets',tracking=True)
    team_id = fields.Many2one('hd.team', string="Team")


    def get_tickets(self):
        tickets_id = self.env['hd.ticket'].search([('assign_to', '=', self.id)])
        self.assign_ticket = len(tickets_id)