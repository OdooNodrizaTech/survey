# -*- coding: utf-8 -*-
{
    'name': 'Survey Kpi',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'survey'],
    'data': [
        'data/ir_cron.xml',
        'views/survey_kpi_view.xml',        
        'security/ir.model.access.csv',
    ],        
    'installable': True,
    'auto_install': False,    
}