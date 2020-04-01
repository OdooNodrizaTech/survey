# -*- coding: utf-8 -*-
from openerp import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import urlparse
import logging
import uuid
import pytz

_logger = logging.getLogger(__name__)

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _rec_name = 'internal_name'
    
    active = fields.Boolean(
        string='Activo'
    )
    internal_name = fields.Char(
        string='Nombre interno'
    )
    survey_type_origin = fields.Selection(
        [
            ('none', 'Ninguna'),
            ('phone', 'Telefono')                    
        ],
        size=15, 
        string='Origen de encuesta', 
        default='none'
    )
    survey_type = fields.Selection(
        [
            ('mail', 'Email'),
            ('phone', 'Telefono'),
            ('popup', 'Popup'),
            ('other', 'Otra'),        
        ],
        size=15, 
        string='Tipo de encuesta', 
        default='mail'
    )
    survey_subtype = fields.Selection(
        [
            ('satisfaction', 'Satisfaccion'),
            ('satisfaction_recurrent', 'Satisfaccion recurrente'),
            ('why_not', 'Why not'),
            ('marketing', 'Marketing'),   
        ],
        size=15, 
        string='Subtipo de encuesta', 
        default='satisfaction'
    )
    survey_frequence = fields.Selection(
        [
            ('custom', 'Personalizada'),
            ('week', 'Semanal'),
            ('month', 'Mensual'),
            ('year', 'Anual'),        
        ],
        size=15, 
        string='Frecuencia de la encuesta', 
        default='custom'
    )    
    deadline_days = fields.Integer(
        string='Fecha limite dias',
    )    
    automation_difference_days = fields.Integer(
        string='Diferencia de dias de automatizacion',
    )            
    mail_template_id = fields.Many2one(
        'mail.template', 
        string='Plantilla de email',
        domain=[('model_id.model', '=', 'survey.survey')],
    )                                    
    
    @api.one    
    def send_survey_satisfaction_phone(self):
        return super(SurveySurvey, self).send_survey_satisfaction_phone()
    
    @api.multi    
    def cron_send_surveys_satisfaction_phone(self, cr=None, uid=False, context=None):
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', 'satisfaction')                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:
                survey_survey_id.send_survey_satisfaction_phone()    
    
    @api.one    
    def send_survey_satisfaction_recurrent_phone(self):
        return super(SurveySurvey, self).send_survey_satisfaction_recurrent_phone()
        
    @api.multi    
    def cron_send_surveys_satisfaction_recurrent_phone(self, cr=None, uid=False, context=None):
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', 'satisfaction_recurrent')                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:
                survey_survey_id.send_survey_satisfaction_recurrent_phone()                        
    
    @api.one    
    def send_survey_real_satisfaction_mail(self):
        #Send by mail real
        return super(SurveySurvey, self).send_survey_real_satisfaction_mail()
    
    @api.one    
    def send_survey_satisfaction_mail(self, survey_survey_input_expired_ids):
        #change other source to mail if conditions
        return super(SurveySurvey, self).send_survey_satisfaction_mail(survey_survey_input_expired_ids)
        
    @api.multi    
    def cron_send_surveys_satisfaction_mail(self, cr=None, uid=False, context=None):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction'),
                ('mail_template_id', '!=', False)                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:
                #send_survey_real_satisfaction_mail
                survey_survey_id.send_survey_real_satisfaction_mail()
        #other origin                
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'phone'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction'),
                ('mail_template_id', '!=', False)                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:                                
                #phone
                survey_survey_ids_phone = self.env['survey.survey'].search(
                    [ 
                        ('active', '=', True),                
                        ('survey_type_origin', '=', 'none'),
                        ('survey_type', '=', 'phone'),
                        ('survey_subtype', '=', survey_survey_id.survey_subtype)                
                    ]
                )
                if len(survey_survey_ids_phone)>0:
                    survey_survey_id_phone = survey_survey_ids_phone[0]                    
                    #expired results
                    survey_survey_input_expired_ids = self.env['survey.user_input'].search(
                        [
                            ('state', '=', 'expired'),
                            ('survey_id', '=', survey_survey_id_phone.id)
                        ]
                    )
                    #send_survey_satisfaction_mail
                    survey_survey_id.send_survey_satisfaction_mail(survey_survey_input_expired_ids)                        
        
    @api.one    
    def send_survey_real_satisfaction_recurrent_mail(self):
        #Send by mail real
        return super(SurveySurvey, self).send_survey_real_satisfaction_recurrent_mail()
    
    @api.one    
    def send_survey_satisfaction_recurrent_mail(self, survey_survey_input_expired_ids):
        #change other source to mail if conditions
        return super(SurveySurvey, self).send_survey_satisfaction_recurrent_mail(survey_survey_input_expired_ids)
    
    @api.multi    
    def cron_send_surveys_satisfaction_recurrent_mail(self, cr=None, uid=False, context=None):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction_recurrent'),
                ('mail_template_id', '!=', False)                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:
                #send_survey_real_satisfaction_recurrent_mail
                survey_survey_id.send_survey_real_satisfaction_recurrent_mail()
        #other origin
        survey_survey_ids = self.env['survey.survey'].search(
            [ 
                ('active', '=', True),                
                ('survey_type_origin', '=', 'phone'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction_recurrent'),
                ('mail_template_id', '!=', False)                
            ]
        )
        if len(survey_survey_ids)>0:
            for survey_survey_id in survey_survey_ids:                                
                #phone
                survey_survey_ids_phone = self.env['survey.survey'].search(
                    [ 
                        ('active', '=', True),                
                        ('survey_type_origin', '=', 'none'),
                        ('survey_type', '=', 'phone'),
                        ('survey_subtype', '=', survey_survey_id.survey_subtype)                
                    ]
                )
                if len(survey_survey_ids_phone)>0:
                    survey_survey_id_phone = survey_survey_ids_phone[0]                    
                    #expired results
                    survey_survey_input_expired_ids = self.env['survey.user_input'].search(
                        [
                            ('state', '=', 'expired'),
                            ('survey_id', '=', survey_survey_id_phone.id)
                        ]
                    )
                    #send_survey_satisfaction_recurrent_mail
                    survey_survey_id.send_survey_satisfaction_recurrent_mail(survey_survey_input_expired_ids)                    