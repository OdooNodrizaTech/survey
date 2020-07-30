# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveyKpiGroup(models.Model):
    _name = 'survey.kpi.group'
    _description = 'Survey Kpi Group'
    
    name = fields.Char(        
        string='Name'
    )
