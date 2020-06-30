# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyLabel(models.Model):
    _inherit = 'survey.label'

    internal_value = fields.Char(
        string='Valor interno'
    )