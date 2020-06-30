# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyUserInput(models.Model):
    _name = 'survey.user_input'
    _inherit = ['mail.thread', 'mail.activity.mixin']