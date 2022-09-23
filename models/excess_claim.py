from odoo import models, fields, api, _
from odoo.http import request

GET_STATE = [
                ('draft', 'Draft'),
                ('employee', 'Employee'),
                ('close', 'Close'),
            ]


class ExcessClaim(models.Model):
    _name = 'excess.claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Medical Claim"
    _rec_name = "employee_id"


    state = fields.Selection(GET_STATE,string='State', default="draft")

    employee_id = fields.Many2one("hr.employee","Employee Name")
    employee_id_number = fields.Char(related="employee_id.employee_id_number")
    employee_grade = fields.Many2one('employee.grade','Employee Grade', related="employee_id.employee_grade")
    payment_type_id = fields.Many2one("payment.type","Payment Type")
    job_id = fields.Many2one('hr.job','Position', related="employee_id.job_id")
    department_id = fields.Many2one('hr.department','Department',related="employee_id.department_id")
    claim_date = fields.Date("Claim Date")
    total_claim = fields.Float("Total Claim", compute="_compute_total_claim_excess")

    excess_claim_ids = fields.One2many("excess.claim.line","excess_id","Medical Claim Line")
    excess_history_ids = fields.One2many("medical.claim.history","excess_id","Excess Claim History")
    x_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.employee_id_number = self.employee_id.employee_id_number
            self.employee_grade = self.employee_id.employee_grade.id

    # @api.onchange('excess_claim_ids')
    # def _onchange_total_claim(self):
    #     total = 0
    #     for rec in self:
    #         for med in rec.excess_claim_ids:

    #             medical_obj = self.env['excess.claim'].sudo().search([('id', '=', self._origin.id)])
    #             print(self._origin.id, '===============================')
    #             total += med.amount_exsess
    #             medical_obj.write({'total_claim':total})

    # @api.depends('excess_claim_ids.amount_exsess')
    @api.depends('excess_claim_ids')
    def _compute_total_claim_excess(self):
        for rec in self:
            rec.total_claim = sum(line.amount_exsess for line in rec.excess_claim_ids)
 

    # @api.onchange('excess_claim_ids')
    # def _onchange_total_claim_excess(self):
    #     total = 0
    #     for rec in self:
    #         for med in rec.excess_claim_ids:
    #             excess_obj = self.env['excess.claim'].sudo().search([('id', '=', self._origin.id)])
    #             total += med.amount_exsess
    #             rec.total_claim=total
    #             excess_obj.write({'total_claim':total})

    @api.depends('state')
    def _compute_css(self):
        for rec in self:
            # Modify below condition
            if rec.state == 'close':
                rec.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.x_css = False

    @api.model
    def get_full_url(self):
        self.ensure_one()
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        message_body = base_url
        
        return message_body

    def action_ref_submited(self):

        return {
                'name' : _("Submit With Comment"),
                'context': {'default_type_aprove':'2', 'default_employee_id':self.employee_id.id},
                'view_type' : 'form',
                'res_model' : 'approve.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }

    def action_ref_submit_claim(self):

        return {
                'name' : _("Submit Claim With Comment"),
                'context': {'default_type_aprove':'2'},
                'view_type' : 'form',
                'res_model' : 'close.after.submit.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }
    
    def action_ref_reminder(self):

        for record in self:

            template= self.env.ref('x_medical_insurance.email_notif_claim_excess')
            template.send_mail(record.id, force_send=True)

            message_id = self.env['message.wizard'].create({'message': _("Email is successfully sent")})
            return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new'}

            
class ExcessClaimLine(models.Model):
    _name = 'excess.claim.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Excess Claim Line"
    _rec_name = "invoice_id"


    excess_id = fields.Many2one("excess.claim","Excess")
    invoice_id = fields.Char("Invoice Excess Number")
    claim_number = fields.Char("Claim Number")
    patient_number = fields.Char("Patient Number")
    patient_name = fields.Char("Patient Name")
    in_patient_date = fields.Date("In Patient Date")
    out_patient_date = fields.Date("Out Patient Date")
    amount_exsess = fields.Float("Amount Excess")
    bank_id = fields.Char("Bank")
    attachment = fields.Binary("Attachment")
    is_employee = fields.Boolean(default=False, compute='_compute_state')

    @api.depends('excess_id.state')
    def _compute_state(self):
        print(self)
        for rec in self:
            if rec.excess_id.state == 'employee':
                rec.is_employee = True
            else:
                rec.is_employee = False

class PaymentType(models.Model):
    _name = 'payment.type'
    _description="Payment Type"
    _rec_name = "name"


    name = fields.Char("Name")