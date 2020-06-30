# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models
from openerp.http import request
from datetime import datetime

import pytz

import logging
_logger = logging.getLogger(__name__)

class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'

    state = fields.Selection(
        [
            ('new', 'Sin comenzar aun'),
            ('skip', 'Parcialmente completado'),
            ('done', 'Completado'),
            ('expired', 'Caducado'),
        ],
        default='new',
        string='Estado',
        readonly=True
    )

    @api.model
    def cron_change_to_expired(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))

        survey_user_input_ids = self.env['survey.user_input'].search(
            [
                ('deadline', '!=', False),
                ('deadline', '<=', current_date.strftime("%Y-%m-%d")),
                ('state', 'not in', ('done', 'expired'))
            ]
        )
        if len(survey_user_input_ids) > 0:
            for survey_user_input_id in survey_user_input_ids:
                survey_user_input_id.state = 'expired'