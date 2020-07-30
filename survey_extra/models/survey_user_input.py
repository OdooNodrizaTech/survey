# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'

    date_done = fields.Datetime(
        string="Date done"
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User id'
    )
    user_id_done = fields.Many2one(
        comodel_name='res.users',
        string='User id done'
    )
    survey_id_survey_type = fields.Selection(
        string="Survey type",
        related='survey_id.survey_type',
        store=False,
        readonly=True
    )
    survey_url = fields.Char(
        compute='_compute_survey_url',
        string="Url",
        readonly=True
    )
    partner_id_phone = fields.Char(
        string="Phone",
        related='partner_id.phone',
        store=False,
        readonly=True
    )
    partner_id_mobile = fields.Char(
        string="Mobile",
        related='partner_id.mobile',
        store=False,
        readonly=True
    )

    @api.multi
    @api.depends('survey_id')
    def _compute_survey_url(self):
        for item in self:
            item.survey_url = '%s/survey/fill/%s/%%s' % (
                self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
                item.survey_id.id,
                item.token
            )

    @api.model
    def action_boton_pedir_llamada(self):
        response = {
            'errors': True,
            'error': _("You don't have a call answer to be assigned")
        }
        # survey_user_input_ids
        user_input_ids = self.env['survey.user_input'].sudo().search(
            [
                ('type', '=', 'manually'),
                ('survey_id.survey_type', '=', 'phone'),
                ('state', 'not in', ('done', 'expired')),
                ('user_id', '=', False),
                ('test_entry', '=', False)
            ],
            order='date_create asc'
        )
        if user_input_ids:
            user_input_ids[0].user_id = self._uid

            response['errors'] = False
        # return
        return response

    @api.multi
    def write(self, vals):
        # stage date_done
        if vals.get('state') == 'done' and not self.date_done:
            vals['date_done'] = fields.datetime.now()
            # user_id_done
            context = self._context
            if 'uid' in context:
                vals['user_id_done'] = context.get('uid')
        # write
        return super(SurveyUserinput, self).write(vals)
