# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr
_logger = logging.getLogger(__name__)

import odoo.addons.survey.controllers.main as main

class Survey(main.Survey):
    def _check_bad_cases(self, survey, token=None):
        survey_user_input_redirect_ids = request.env['survey.user_input.redirect'].sudo().search([ ('survey_id', '=', survey.id),('token', '=', token)])
        if len(survey_user_input_redirect_ids)>0:
            for survey_user_input_redirect_id in survey_user_input_redirect_ids:
                return request.redirect('/survey/start/%s/%s' % (survey_user_input_redirect_id.user_input_id.survey_id.id, survey_user_input_redirect_id.user_input_id.token))
        
        return super(Survey, self)._check_bad_cases(survey, token)                        