# -*- coding: utf-8 -*-
# © 2013 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, exceptions, fields, models
from openerp.http import request
from dateutil.relativedelta import relativedelta
from datetime import datetime

import pytz

import logging
_logger = logging.getLogger(__name__)

class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'
    
    user_id = fields.Many2one(
        comodel_name='res.users',        
        string='Comercial'
    )
    user_id_done = fields.Many2one(
        comodel_name='res.users',        
        string='Comercial hecho'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',        
        string='Flujo de ventas'
    )    
    date_done = fields.Datetime(
        string="Fecha fin"
    )
    state = fields.Selection(
        [
            ('new', 'Sin comenzar aun'),
            ('skip', 'Parcialmente completado'),
            ('done', 'Completado'),
            ('expired', 'Caducado'),        
        ],
        default='new',        
        string='Estado',
        readonly=True
    )
    call_tried = fields.Integer(        
        string='Nº intentos'
    )
    date_next_tried = fields.Datetime(        
        string='Fecha siguiente intentos'
    )
    survey_id_survey_type = fields.Char(
        compute='_survey_id_survey_type',
        string="Tipo de encuesta",
        readonly=True
    )
    survey_url = fields.Char(
        compute='_survey_url',
        string="Url",
        readonly=True
    )
    partner_id_phone = fields.Char(
        compute='_partner_id_phone',
        string="Telefono",
        readonly=True
    )
    partner_id_mobile = fields.Char(
        compute='_partner_id_mobile',
        string="Movil",
        readonly=True
    )
    
    @api.depends('survey_id')    
    def _survey_id_survey_type(self):
        for item in self:
            item.survey_id_survey_type = item.survey_id.survey_type
            
    @api.depends('survey_id')    
    def _survey_url(self):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for item in self:
            item.survey_url = str(web_base_url)+'/survey/fill/'+str(item.survey_id.id)+'/'+str(item.token)    
    
    @api.depends('partner_id')    
    def _partner_id_phone(self):
        for item in self:
            item.partner_id_phone = item.partner_id.phone
    
    @api.depends('partner_id')    
    def _partner_id_mobile(self):
        for item in self:
            item.partner_id_mobile = item.partner_id.mobile            
    
    @api.multi    
    def cron_change_to_expired(self, cr=None, uid=False, context=None):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        
        survey_user_input_ids = self.env['survey.user_input'].search(
            [ 
                ('deadline', '!=', False),                
                ('deadline', '<=', current_date.strftime("%Y-%m-%d")),
                ('state', 'not in', ('done', 'expired'))
            ]
        )
        if len(survey_user_input_ids)>0:
            for survey_user_input_id in survey_user_input_ids:
                survey_user_input_id.state = 'expired'    
        
    @api.model                        
    def action_boton_pedir_llamada(self):
        response = {
            'errors': True,
            'error': "No tienes respuesta de llamada para poder asignarte"
        }
        #survey_user_input_ids
        survey_user_input_ids = self.env['survey.user_input'].search(
            [ 
                ('type', '=', 'manually'),                
                ('survey_id.survey_type', '=', 'phone'),
                ('state', 'not in', ('done', 'expired')),
                ('user_id', '=', False),
                ('test_entry', '=', False)
            ],
            order='date_create asc'
        )
        if len(survey_user_input_ids)>0:
            survey_user_input_id = survey_user_input_ids[0]
            survey_user_input_id.user_id = self._uid
            
            response['errors'] = False                         
        #return
        return response
    
    @api.model
    def create(self, values):                    
        return_object = super(SurveyUserinput, self).create(values)
        
        if request:                           
            lead_id_get = str(request.httprequest.args.get('lead_id'))
                    
            if lead_id_get!="None":                
                return_object.lead_id = int(lead_id_get)
                
                if return_object.lead_id.id!=False:             
                    return_object.partner_id = return_object.lead_id.partner_id.id
                    
                    if return_object.lead_id.user_id.id!=False:
                        return_object.user_id = return_object.lead_id.user_id                                                                                
                            
        return return_object
        
    @api.multi
    def write(self, vals):
        # stage date_done
        if vals.get('state')=='done' and self.date_done==False:
            vals['date_done'] = fields.datetime.now()
            #user_id (override previously 'incorrect' assigment in phone)
            if self.lead_id!=False:
                if self.lead_id.user_id!=False:
                    vals['user_id'] = self.lead_id.user_id.id         
            
            elif self.order_id!=False:
                if self.order_id.user_id!=False:
                    vals['user_id'] = self.order_id.user_id.id
            #user_id_done
            context = self._context
            if 'uid' in context:
                vals['user_id_done'] = context.get('uid')                              
                                                                
        return super(SurveyUserinput, self).write(vals)                                                          