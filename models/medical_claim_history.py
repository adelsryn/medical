

from odoo import models, fields, api, _




class MedicalClaimHistory(models.Model):
    _name = "medical.claim.history"
    _rec_name = "state"
    _description = "Medical History"

    medical_id = fields.Many2one("medical.claim","Medical Claim")
    excess_id = fields.Many2one("excess.claim","Medical Claim")
    state = fields.Char(string='State')
    user_id = fields.Many2one("res.users","User", default=lambda self: self.env.user)
    comment = fields.Char("Comment")