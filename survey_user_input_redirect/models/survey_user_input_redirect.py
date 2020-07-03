# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveyUserInputRedirect(models.Model):
    _name = 'survey.user_input.redirect'
    _description = 'Survey User Input Redirect'
            
    token = fields.Char('Modelo')
    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey'
    )
    user_input_id = fields.Many2one(
        comodel_name='survey.user_input',
        string='Survey User Input '
    )