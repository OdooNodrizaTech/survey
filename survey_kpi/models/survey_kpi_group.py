# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyKpiGroup(models.Model):
    _name = 'survey.kpi.group'
    _description = 'Survey Kpi Group'
    
    name = fields.Char(        
        string='Nombre'
    )                                                                                                               