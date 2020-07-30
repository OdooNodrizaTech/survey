# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning as UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def action_set_lost(self):
        allow_action = True
        for item in self:
            allow_action = True
            if item.type == 'opportunity' and item.partner_id:
                survey_id = item.get_survey_id()
                if survey_id > 0:
                    user_input_ids = self.env['survey.user_input'].search(
                        [
                            ('survey_id', '=', int(survey_id)),
                            ('state', '=', 'done'),
                            ('lead_id', '=', item.id)
                        ]
                    )
                    if len(user_input_ids) == 0:
                        allow_action = False
                        raise UserError(
                            _('It is necessary to complete the why not to '
                              'be able to give up the opportunity')
                        )

        if allow_action:
            return super(CrmLead, self).action_set_lost()

    @api.model
    def get_survey_id(self):
        survey_id = 0
        survey_ids = self.env['survey.survey'].search(
            [
                ('survey_type', '=', 'popup'),
                ('survey_subtype', '=', 'why_not'),
                ('active', '=', True)
            ]
        )
        if survey_ids:
            survey_id = survey_ids[0].id
        # return
        return survey_id
