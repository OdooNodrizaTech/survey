# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveyLabel(models.Model):
    _inherit = 'survey.label'

    internal_value = fields.Char(
        string='Internal value'
    )