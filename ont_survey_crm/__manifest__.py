# -*- coding: utf-8 -*-
{
    'name': 'Ont Survey Crm',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'ont_base_survey'],
    'data': [
        'views/crm_lead_lost.xml',
    ],        
    'installable': True,
    'auto_install': False,    
}