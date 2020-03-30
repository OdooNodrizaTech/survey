# -*- coding: utf-8 -*-
# © 2013 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveyLabel(models.Model):
    _inherit = 'survey.label'

    internal_value = fields.Char(
        string='Valor interno'
    )