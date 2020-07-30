# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models
from datetime import datetime

import pytz


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _rec_name = 'internal_name'

    active = fields.Boolean(
        string='Active'
    )
    internal_name = fields.Char(
        string='Internal name'
    )
    survey_type_origin = fields.Selection(
        [
            ('none', 'None'),
            ('phone', 'Phone')
        ],
        size=15,
        string='Survey type origin',
        default='none'
    )
    survey_type = fields.Selection(
        [
            ('mail', 'Mail'),
            ('phone', 'Phone'),
            ('popup', 'Popup'),
            ('other', 'Other'),
        ],
        size=15,
        string='Survey type',
        default='mail'
    )
    survey_subtype = fields.Selection(
        [
            ('satisfaction', 'Satisfaction'),
            ('satisfaction_recurrent', 'Recurrent satisfaction'),
            ('why_not', 'Why not'),
            ('marketing', 'Marketing'),
        ],
        size=15,
        string='Survey subtype',
        default='satisfaction'
    )
    survey_frequence = fields.Selection(
        [
            ('custom', 'Custom'),
            ('week', 'Week'),
            ('month', 'Month'),
            ('year', 'Year'),
        ],
        size=15,
        string='Survey frequence',
        default='custom'
    )
    deadline_days = fields.Integer(
        string='Deadline days',
    )
    automation_difference_days = fields.Integer(
        string='Automation difference days',
    )
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Mail template',
        domain=[('model_id.model', '=', 'survey.survey')],
    )

    @api.multi
    def send_survey_satisfaction_phone(self):
        return super(SurveySurvey, self).send_survey_satisfaction_phone()

    @api.model
    def cron_send_surveys_satisfaction_phone(self):
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', 'satisfaction')
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                survey_id.send_survey_satisfaction_phone()

    @api.multi
    def send_survey_satisfaction_recurrent_phone(self):
        return super(SurveySurvey, self).send_survey_satisfaction_recurrent_phone()

    @api.model
    def cron_send_surveys_satisfaction_recurrent_phone(self):
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', 'satisfaction_recurrent')
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                survey_id.send_survey_satisfaction_recurrent_phone()
                # get_phone_survey_surveys (reuse in Arelux)

    @api.multi
    def get_phone_survey_surveys(self):
        return self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'phone'),
                ('survey_subtype', '=', self.survey_subtype)
            ]
        )

    @api.multi
    def send_survey_real_satisfaction_mail(self):
        # Send by mail real
        return super(SurveySurvey, self).send_survey_real_satisfaction_mail()

    @api.multi
    def send_survey_satisfaction_mail(self, survey_survey_input_expired_ids):
        # change other source to mail if conditions
        return super(SurveySurvey, self).send_survey_satisfaction_mail(survey_survey_input_expired_ids)

    @api.model
    def cron_send_surveys_satisfaction_mail(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction'),
                ('mail_template_id', '!=', False)
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                # send_survey_real_satisfaction_mail
                survey_id.send_survey_real_satisfaction_mail()
        # other origin
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'phone'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction'),
                ('mail_template_id', '!=', False)
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                # phone
                survey_ids_phone = survey_id.get_phone_survey_surveys()
                if survey_ids_phone:
                    # expired results
                    user_input_ids = self.env['survey.user_input'].search(
                        [
                            ('state', '=', 'expired'),
                            ('survey_id', '=', survey_ids_phone[0].id)
                        ]
                    )
                    # send_survey_satisfaction_mail
                    survey_id.send_survey_satisfaction_mail(user_input_ids)

    @api.multi
    def send_survey_real_satisfaction_recurrent_mail(self):
        # Send by mail real
        return super(SurveySurvey, self).send_survey_real_satisfaction_recurrent_mail()

    @api.multi
    def send_survey_satisfaction_recurrent_mail(self, survey_survey_input_expired_ids):
        # change other source to mail if conditions
        return super(SurveySurvey, self).send_survey_satisfaction_recurrent_mail(survey_survey_input_expired_ids)

    @api.model
    def cron_send_surveys_satisfaction_recurrent_mail(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'none'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction_recurrent'),
                ('mail_template_id', '!=', False)
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                # send_survey_real_satisfaction_recurrent_mail
                survey_id.send_survey_real_satisfaction_recurrent_mail()
        # other origin
        survey_ids = self.env['survey.survey'].search(
            [
                ('active', '=', True),
                ('survey_type_origin', '=', 'phone'),
                ('survey_type', '=', 'mail'),
                ('survey_subtype', '=', 'satisfaction_recurrent'),
                ('mail_template_id', '!=', False)
            ]
        )
        if survey_ids:
            for survey_id in survey_ids:
                # phone
                survey_ids_phone = survey_id.get_phone_survey_surveys()
                if survey_ids_phone:
                    # expired results
                    user_input_ids = self.env['survey.user_input'].search(
                        [
                            ('state', '=', 'expired'),
                            ('survey_id', '=', survey_ids_phone[0].id)
                        ]
                    )
                    # send_survey_satisfaction_recurrent_mail
                    survey_id.send_survey_satisfaction_recurrent_mail(user_input_ids)
