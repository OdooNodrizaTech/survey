# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyLabel(models.Model):
    _inherit = 'survey.label'

    internal_value = fields.Char(
        string='Valor interno'
    )