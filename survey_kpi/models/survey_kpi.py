# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyKpi(models.Model):
    _name = 'survey.kpi'
    _description = 'Survey Kpi'
    
    name = fields.Char(        
        compute='_get_name',
        string='Nombre',
        store=False
    )
    
    @api.one        
    def _get_name(self):            
        for obj in self:
            obj.name = obj.code
            
    code = fields.Char(        
        string='Codigo', 
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
    
    @api.multi    
    def cron_update_survey_user_input_line(self, cr=None, uid=False, context=None):
        survey_kpi_ids = self.env['survey.kpi'].search([('id', '>', 0)])
        if len(survey_kpi_ids)>0:
            for survey_kpi_id in survey_kpi_ids:
                if survey_kpi_id.survey_label_id.id>0:
                    survey_user_input_line_ids = self.env['survey.user_input_line'].search(
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
                    survey_user_input_line_ids = self.env['survey.user_input_line'].search(
                        [                            
                            ('user_input_id.test_entry', '=', False),
                            ('user_input_id.survey_id', '=', self.survey_id.id),                
                            ('user_input_id.state', '=', 'done'),
                            ('question_id', '=', self.survey_question_id.id), 
                            ('survey_kpi_id', '=', False)
                         ]
                    )
                
                #assign_survey_kpi_id
                if len(survey_user_input_line_ids)>0:
                    for survey_user_input_line_id in survey_user_input_line_ids:
                        survey_user_input_line_id.survey_kpi_id = survey_kpi_id.id                                                                                                       