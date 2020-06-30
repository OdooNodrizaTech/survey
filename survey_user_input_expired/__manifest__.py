# -*- coding: utf-8 -*-
{
    'name': 'Survey user input expired',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'survey'],
    'data': [
        'data/ir_cron.xml',
        'views/survey_user_input.xml',
    ],
    'installable': True,
    'auto_install': False,
}