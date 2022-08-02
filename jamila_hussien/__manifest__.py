# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL-Intellisoft International Pvt. Ltd.
#    Copyright (C) 2021 Tech-Receptives(<http://www.iatl-intellisoft.com>).
#
###############################################################################

{
    'name': "Help Desk",

    'author': "IATL Intellisoft International",
    'website': "http://www.iatl-intellisoft.com",
    'category': '',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/helpdesk.xml',
        'views/teams_view.xml',
        'views/tickets_view.xml',
        'wizard/excel_team_ticket_view.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}


