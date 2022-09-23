from odoo import api, fields, models, _
from datetime import datetime, time, timedelta
from odoo.http import request, Response

class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True, readonly=True)

    def action_ok(self):

        return {'type': 'ir.actions.act_window_close'}