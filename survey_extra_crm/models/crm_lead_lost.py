# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'

    survey_url = fields.Char(
        string='Survey',
        store=False
    )

    @api.model
    def default_get(self, fields):
        res = super(CrmLeadLost, self).default_get(fields)

        lead_obj_return = self.env['crm.lead'].search(
            [
                ('id', '=', self.env.context.get('active_id'))
            ]
        )
        survey_id = lead_obj_return.get_survey_id()

        if survey_id > 0:
            survey_obj_return = self.env['survey.survey'].search(
                [
                    ('id', '=', survey_id)
                ]
            )
            res['survey_url'] = '%s?lead_id=%s' % (
                survey_obj_return.public_url,
                lead_obj_return.id
            )
        # return
        return res
