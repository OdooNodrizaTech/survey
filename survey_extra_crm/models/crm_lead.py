# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def action_set_lost(self):
        allow_action = True
        for lead_obj in self:
            allow_action = True
            if lead_obj.type == 'opportunity' and lead_obj.partner_id.id > 0:
                survey_id = lead_obj.get_survey_id()
                if survey_id > 0:
                    survey_user_input_ids = self.env['survey.user_input'].search(
                        [
                            ('survey_id', '=', int(survey_id)),
                            ('state', '=', 'done'),
                            ('lead_id', '=', lead_obj.id)
                        ]
                    )
                    if len(survey_user_input_ids) == 0:
                        allow_action = False
                        raise Warning(_('It is necessary to complete the why not to be able to give up the opportunity'))

        if allow_action == True:
            return super(CrmLead, self).action_set_lost()

    @api.model
    def get_survey_id(self):
        survey_id = 0
        survey_survey_ids = self.env['survey.survey'].search(
            [
                ('survey_type', '=', 'popup'),
                ('survey_subtype', '=', 'why_not'),
                ('active', '=', True)
            ]
        )
        if len(survey_survey_ids) > 0:
            survey_survey_id = survey_survey_ids[0]
            survey_id = survey_survey_id.id
        #return
        return survey_id