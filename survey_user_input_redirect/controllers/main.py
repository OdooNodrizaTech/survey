# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import request

import odoo.addons.survey.controllers.main as main


class Survey(main.Survey):
    def _check_bad_cases(self, survey, token=None):
        redirect_ids = request.env['survey.user_input.redirect'].sudo().search(
            [
                ('survey_id', '=', survey.id),
                ('token', '=', token)
            ]
        )
        if redirect_ids:
            for redirect_id in redirect_ids:
                return request.redirect('/survey/start/%s/%s' % (
                    redirect_id.user_input_id.survey_id.id,
                    redirect_id.user_input_id.token
                ))
        return super(Survey, self)._check_bad_cases(survey, token)
