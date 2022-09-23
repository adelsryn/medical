
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError,Warning

GET_STATE = [
                ('draft', 'Draft'),
                ('hc', 'HC'),
                ('setlement', 'Settlement'),
                ('close', 'Close'),
            ]


class MedicalClaim(models.Model):
    _name = 'medical.claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Medical Claim"
    _rec_name = "employee_id"

    def _default_employee_id(self):
        if self.env.context.get('uid', False):
            inv = self.env.context.get('uid', False)
            employee_obj=self.env['hr.employee'].search([('user_id', '=', inv)])
                
        return employee_obj

    state = fields.Selection(GET_STATE,string='State', default="draft")

    employee_id = fields.Many2one("hr.employee","Employee Name", default=_default_employee_id)
    employee_id_number = fields.Char(related="employee_id.employee_id_number")
    employee_grade = fields.Many2one('employee.grade','Employee Grade', related="employee_id.employee_grade")
    responsible_id = fields.Many2one("hr.employee","Responsible HC")
    job_id = fields.Many2one('hr.job','Position', related="employee_id.job_id")
    department_id = fields.Many2one('hr.department','Department',related="employee_id.department_id")
    claim_date = fields.Date("Claim Date")
    total_claim = fields.Float("Total Claim", compute="_depends_total_claim")

    claim_type_ids= fields.Many2many('claim.type')
    medical_claim_ids = fields.One2many("medical.claim.line","medical_id","Medical Claim Line")
    medical_history_ids = fields.One2many("medical.claim.history","medical_id","Medical Claim History")
    x_css = fields.Html(string='CSS', sanitize=False, store=False)

    inv = fields.Boolean(compute='_compute_responsible_id', string='Responsible ID Computed')

    def _compute_responsible_id(self):
        if self.env.context.get('uid', False):
            inv = self.env.context.get('uid', False)
            if inv == self.responsible_id.user_id.id:
                self.inv=True
            else:
                self.inv=False
                
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.employee_id_number = self.employee_id.employee_id_number
            self.employee_grade = self.employee_id.employee_grade.id

    @api.depends('medical_claim_ids')
    def _depends_total_claim(self):
        for rec in self:
            rec.total_claim = sum(line.amount_claim for line in rec.medical_claim_ids)
 
    # @api.onchange('medical_claim_ids')
    # def _onchange_total_claim(self):
    #     total = 0
    #     for rec in self:
    #         for med in rec.medical_claim_ids:

    #             medical_obj = self.env['medical.claim'].sudo().search([('id', '=', self._origin.id)])
    #             print(self._origin.id, '===============================')
    #             total += med.amount_claim
    #             medical_obj.write({'total_claim':total})



    # @api.depends('state')
    # def _compute_css(self):
    #     for rec in self:
    #         # Modify below condition
    #         if rec.state == 'hc':
    #             rec.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
    #         else:
    #             rec.x_css = False

    # def decrease_limit(self):
    #     for rec in self:

    #         # print

    #             for med in rec.medical_claim_ids:
    #                 domain = ['&',
    #                                 ('employee_id', '=', rec.employee_id.id),
    #                                 ('claim_type_id', '=', med.claim_type.id),
    #                             ]

    #                 lmt_klaim_obj = self.env['limit.klaim'].sudo().search(domain, limit=1)

    #                 if med.claim_type.is_unlimited == True:
    #                     if med.amount_claim > lmt_klaim_obj.batas_limit:
    #                         res = {'warning': {
    #                             'title': _('Warning'),
    #                             'message': _('Amount claim is greater than your limit')
    #                         }}
                    
    #                 else:
    #                     lmt_lama = float(lmt_klaim_obj.sisa_limit)
    #                     lmt_baru = lmt_lama - float(med.amount_claim)
    #                     lmt_klaim_obj.write({'sisa_limit':lmt_baru})

    def action_ref_submited(self):
        return {
                'name' : _("Submit With Comment"),
                'context': {'default_type_aprove':'1', 'default_employee_id':self.employee_id.id},
                'view_type' : 'form',
                'res_model' : 'approve.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }
        

    def action_ref_approve(self):
        return {
                'name' : _("Approve the Submission"),
                'context': {'default_type_aprove':'1'},
                'view_type' : 'form',
                'res_model' : 'approve.after.submit.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }

    def action_ref_close(self):
        return {
                'name' : _("Close the Submission"),
                'context': {'default_type_aprove':'1'},
                'view_type' : 'form',
                'res_model' : 'close.after.submit.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }

    def action_ref_reject(self):

        # for rec in self:

        #     for med in rec.medical_claim_ids:
        #         domain = ['&',
        #                     ('employee_id', '=', rec.employee_id.id),
        #                     ('claim_type_id', '=', med.claim_type.id),
        #                 ]

        #         lmt_klaim_obj = self.env['limit.klaim'].sudo().search(domain, limit=1)
        #         lmt_lama = float(lmt_klaim_obj.sisa_limit)
        #         lmt_baru = lmt_lama + float(med.amount_claim)
        #         lmt_klaim_obj.write({'sisa_limit':lmt_baru})

        return {
                'name' : _("Reject the Submission"),
                'context': {'default_type_aprove':'1', 'default_employee_id':self.employee_id.id},
                'view_type' : 'form',
                'res_model' : 'reject.medical.history.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            } 
    
    def action_ref_reminder(self):
        template= self.env.ref('x_medical_insurance.email_kelengkapan_dokumen_claim')
        template.send_mail(self.id, force_send=True)

        # mymodule = self.get_server_info(self.name)
        
        message_id = self.env['message.wizard'].create({'message': _("Email is successfully sent")})
        return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new'}

class MedicalClaimLine(models.Model):
    _name = 'medical.claim.line'
    _description = "MedicalClaimLine"


    medical_id = fields.Many2one("medical.claim","Medical Claim")
    claim_type = fields.Many2one("claim.type","Claim Type", domain="[('id', 'in', compute_claim_ids)]")
    patient_name = fields.Char("Patient Name")
    description = fields.Char("Description")
    card_number_insurance = fields.Char("Card Number Insurance")
    invoice_date = fields.Date("Invoice Date")
    amount_claim = fields.Float("Amount Claim")
    limit_claim = fields.Float("Limit Claim", compute='_compute_claim_type')
    attachment = fields.Binary("Attachment")
    state = fields.Selection(GET_STATE,string='State', related="medical_id.state")
    is_setlement = fields.Boolean(default=False, compute='_compute_setlement')
    employee_grade = fields.Many2one('employee.grade','Employee Grade')
    compute_claim_ids = fields.Many2many('claim.type', string='Compute Claim', compute='_compute_try')

    # @api.onchange('medical_id.employee_id')
    # def _onchange_assignedto(self):
    #     for rec in self:
    #         print({'domain' : {'claim_type' : [('id', 'in', [u.id for r in rec.claim_type for u in r.employee_grade_ids])] } }, '===========================================ddd')
    #         return {'domain' : {'claim_type' : [('id', 'in', [u.id for r in rec.claim_type for u in r.employee_grade_ids])] } }

    @api.depends('medical_id.employee_id', 'medical_id.employee_grade', 'claim_type')
    def _compute_try(self):
        for rec in self:
            domain = [('employee_grade_ids', 'in', rec.medical_id.employee_grade.id)]
            rec.compute_claim_ids = self.env['claim.type'].search(domain)

    @api.depends('medical_id.state')
    def _compute_setlement(self):
        print(self)
        for rec in self:
            if rec.medical_id.state == 'setlement':
                rec.is_setlement = True
            else:
                rec.is_setlement = False

    @api.onchange('claim_type')
    def _compute_claim_type(self):
        for rec in self:
            if rec.claim_type:
                rec.limit_claim = rec.claim_type.limit_amount

    # @api.depends('medical_id')
    # def _compute_claim_ids(self):
    #     if self.env.context.get('default_medical_id'):
    #         medical_obj = self.env['medical.claim'].search([('id', '=', self.env.context.get('default_medical_id'))])
    #         if medical_obj:
    #             grade_obj = self.env['employee.grade'].sudo().search([('id', '=', medical_obj.employee_grade.id)])
    #             print(grade_obj, '==========')
    #             self.compute_claim_ids = grade_obj.ids


    # @api.onchange('medical_id.employee_id')
    # def _depends_medical_id(self):
    #     for rec in self:
    #         print(rec.id, '=========================')
    #         rec.employee_grade = rec.medical_id.employee_grade.id

    # @api.onchange('amount_claim')
    # def _onchange_claim_type(self):

    #     for rec in self:
    #         if rec.claim_type:

    #             claim_type_obj = self.env['claim.type'].sudo().search([('id', '=', rec.claim_type.id)])
    #             rec.limit_claim = claim_type_obj.limit_amount

    #             domain = ['&',
    #                             ('employee_id', '=', rec.medical_id.employee_id.id),
    #                             ('claim_type_id', '=', rec.claim_type.id),
    #                         ] 
    #             sisa_lmt_obj = self.env['limit.klaim'].sudo().search(domain)

    #             if float(sisa_lmt_obj.sisa_limit) < float(rec.amount_claim):
    #                 rec.amount_claim = sisa_lmt_obj.sisa_limit
    #                 res = {'warning': {
    #                             'title': _('Warning'),
    #                             'message': _('Out of used')
    #                         }}

    #             if float(sisa_lmt_obj.sisa_limit) == 0:
    #                 res = {'warning': {
    #                             'title': _('Warning'),
    #                             'message': _('Sorry, you have no longer claim limit')
    #                         }}
    #                 return res

    # @api.onchange('claim_type'):

    






