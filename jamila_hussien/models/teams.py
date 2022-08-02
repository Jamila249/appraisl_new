# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL-Intellisoft International Pvt. Ltd.
#    Copyright (C) 2021 Tech-Receptives(<http://www.iatl-intellisoft.com>).
#
###############################################################################

from odoo import models, fields, api, _


class Teams(models.Model):
    _name = 'hd.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Create Teams'

    name=fields.Char(string='Name', required=True, track=True)
    member=fields.Many2many('res.users',string='Members')




