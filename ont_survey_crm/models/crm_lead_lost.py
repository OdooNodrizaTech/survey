# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'        

    survey_url = fields.Char(
        string='Encuesta',
        store=False
    )
        
    @api.model
    def default_get(self, fields):
        res = super(CrmLeadLost, self).default_get(fields)
                        
        lead_obj_return = self.env['crm.lead'].search([('id', '=', self.env.context.get('active_id'))])
        survey_id = lead_obj_return.get_survey_id()        
        
        if survey_id>0:
            survey_obj_return = self.env['survey.survey'].search([('id', '=', survey_id)])                
            res['survey_url'] = survey_obj_return.public_url+'?lead_id='+str(lead_obj_return.id)        
            
        return res    