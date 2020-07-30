# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models
from openerp.http import request


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
        res = super(SurveyUserinput, self).create(values)
        # request
        if request:
            lead_id_get = str(request.httprequest.args.get('lead_id'))
            if lead_id_get != "None":
                res.lead_id = int(lead_id_get)
                if res.lead_id:
                    res.partner_id = return_object.res.partner_id.id
                    # user_id
                    if res.lead_id.user_id:
                        res.user_id = res.lead_id.user_id
        # return
        return res

    @api.multi
    def write(self, vals):
        # stage date_done
        if vals.get('state') == 'done':
            for item in self:
                if not item.date_done:
                    if item.lead_id:
                        if item.lead_id.user_id:
                            vals['user_id'] = item.lead_id.user_id.id
                    elif item.order_id:
                        if item.order_id.user_id:
                            vals['user_id'] = item.order_id.user_id.id
            # user_id_done
            context = self._context
            if 'uid' in context:
                vals['user_id_done'] = context.get('uid')
        # write
        return super(SurveyUserinput, self).write(vals)
