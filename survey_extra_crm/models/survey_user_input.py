# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models
from openerp.http import request

import logging
_logger = logging.getLogger(__name__)

class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead'
    )
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order'
    )

    @api.model
    def create(self, values):
        return_object = super(SurveyUserinput, self).create(values)
        #request
        if request:
            lead_id_get = str(request.httprequest.args.get('lead_id'))
            if lead_id_get != "None":
                return_object.lead_id = int(lead_id_get)
                if return_object.lead_id.id>0:
                    return_object.partner_id = return_object.lead_id.partner_id.id
                    #user_id
                    if return_object.lead_id.user_id.id>0:
                        return_object.user_id = return_object.lead_id.user_id
        #return
        return return_object

    @api.multi
    def write(self, vals):
        # stage date_done
        if vals.get('state') == 'done':
            for item in self:
                if item.date_done == False:
                    if item.lead_id.id>0:
                        if item.lead_id.user_id.id>0:
                            vals['user_id'] = item.lead_id.user_id.id
                    elif item.order_id.id>0:
                        if item.order_id.user_id.id>0:
                            vals['user_id'] = item.order_id.user_id.id
            # user_id_done
            context = self._context
            if 'uid' in context:
                vals['user_id_done'] = context.get('uid')
        #write
        return super(SurveyUserinput, self).write(vals)