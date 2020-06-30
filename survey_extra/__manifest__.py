# -*- coding: utf-8 -*-
{
    'name': 'Survey Extra',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'survey', 'survey_user_input_expired'],
    'data': [
        'data/ir_cron.xml',
        'views/survey_question.xml',
        'views/survey_user_input.xml',
        'views/survey_survey.xml',
    ],
    'installable': True,
    'auto_install': False,
}