# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyKpiGroup(models.Model):
    _name = 'survey.kpi.group'
    _description = 'Survey Kpi Group'
    
    name = fields.Char(        
        string='Nombre'
    )                                                                                                               