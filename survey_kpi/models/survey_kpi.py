# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyKpi(models.Model):
    _name = 'survey.kpi'
    _description = 'Survey Kpi'
    _rec_name = 'code'

    code = fields.Char(        
        string='Code',
    )
    survey_kpi_group_id = fields.Many2one(
        comodel_name='survey.kpi.group',
        string='Survey Kpi Group'
    )
    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        context="{'active_test':False}",
        string='Survey'
    )                
    survey_page_id = fields.Many2one(
        comodel_name='survey.page',
        string='Survey Page'
    )
    survey_question_id = fields.Many2one(
        comodel_name='survey.question',
        string='Survey Question'
    )
    survey_label_id = fields.Many2one(
        comodel_name='survey.label',
        string='Survey Label'
    )
    
    @api.model    
    def cron_update_survey_user_input_line(self):
        kpi_ids = self.env['survey.kpi'].search([('id', '>', 0)])
        if kpi_ids:
            for kpi_id in kpi_ids:
                if kpi_id.survey_label_id:
                    user_input_line_ids = self.env['survey.user_input_line'].search(
                        [                            
                            ('user_input_id.test_entry', '=', False),
                            ('user_input_id.survey_id', '=', self.survey_id.id),                
                            ('user_input_id.state', '=', 'done'),
                            ('question_id', '=', self.survey_question_id.id), 
                            ('value_suggested_row', '=', self.survey_label_id.id),
                            ('survey_kpi_id', '=', False)
                         ]
                    )
                else:
                    user_input_line_ids = self.env['survey.user_input_line'].search(
                        [                            
                            ('user_input_id.test_entry', '=', False),
                            ('user_input_id.survey_id', '=', self.survey_id.id),                
                            ('user_input_id.state', '=', 'done'),
                            ('question_id', '=', self.survey_question_id.id), 
                            ('survey_kpi_id', '=', False)
                         ]
                    )
                # assign_survey_kpi_id
                if user_input_line_ids:
                    for user_input_line_id in user_input_line_ids:
                        user_input_line_id.survey_kpi_id = kpi_id.id
