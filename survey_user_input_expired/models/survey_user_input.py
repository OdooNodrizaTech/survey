# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime
import pytz


class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'

    state = fields.Selection(
        [
            ('new', 'New'),
            ('skip', 'Skip'),
            ('done', 'Done'),
            ('expired', 'Expired'),
        ],
        default='new',
        string='State',
        readonly=True
    )

    @api.model
    def cron_change_to_expired(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))

        user_input_ids = self.env['survey.user_input'].search(
            [
                ('deadline', '!=', False),
                ('deadline', '<=', current_date.strftime("%Y-%m-%d")),
                ('state', 'not in', ('done', 'expired'))
            ]
        )
        if user_input_ids:
            for user_input_id in user_input_ids:
                user_input_id.state = 'expired'
