# from unittest.case import doModuleCleanups
from odoo import models, fields, api, _

class ClaimType(models.Model):
    _name = 'claim.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description="Claim Type"
    _rec_name = "name"


    code = fields.Char("Code")
    claim_code = fields.Char("Claim ID")
    name = fields.Char("Name")
    employee_grade = fields.Many2one('employee.grade','Employee Grade')
    limit_amount = fields.Float("Limit Amount")
    coverage = fields.Char("Coverage")
    # is_unlimited = fields.Boolean("Is Unlimited ?")
    benefit = fields.Text("Benefit")
    employee_grade_ids = fields.Many2many(comodel_name = 'employee.grade', string='Employee Grade')
    
    # @api.model
    # def create(self, vals):

    #     result = super(ClaimType, self).create(vals)  

    #     for g in result.employee_grade_ids:
    #         employee_obj = self.env['hr.employee'].search([('employee_grade', '=', g.id)])

    #         vals_lmt = []
    #         for e in employee_obj:
    #             lmt_klaim = self.env['limit.klaim'].sudo()
    #             vals_lmt = {
    #                     'employee_id' : e.id,
    #                     'employee_grade': g.id,
    #                     'claim_type_id':result.id,
    #                     'batas_limit':result.limit_amount,
    #                     'sisa_limit':result.limit_amount
    #             }

    #             create_lmt = lmt_klaim.create(vals_lmt)
    #     return result

    # def write(self, vals):

    #     if vals:
    #         for d in self:
    #             domain = [
    #                         ('claim_type_id', '=', d.id),
    #                     ]
    #             lmt_klaim = self.env['limit.klaim'].sudo().search(domain)
    #             for l in lmt_klaim:

    #                 if float(vals.get('limit_amount')) != l.batas_limit:
                        
    #                     if float(vals.get('limit_amount')) < l.batas_limit:
                            
    #                         sisa_lama = l.sisa_limit
    #                         selisih_lmt = float(l.batas_limit) - float(vals.get('limit_amount'))
    #                         sisa_baru = sisa_lama - selisih_lmt
    #                         l.write({
    #                             'sisa_limit': sisa_baru,
    #                     })

    #                     if float(vals.get('limit_amount')) > l.batas_limit:
                            
    #                         sisa_lama = l.sisa_limit
    #                         selisih_lmt = float(vals.get('limit_amount')) - float(l.batas_limit)
    #                         sisa_baru = sisa_lama + selisih_lmt
    #                         l.write({
    #                             'sisa_limit': sisa_baru,
    #                     })

    #                     l.write({
    #                             'batas_limit': vals.get('limit_amount'),
    #                     })

    #             for g in d.employee_grade_ids:

    #                 domain_group = ['&',
    #                             ('claim_type_id', '=', d.id),
    #                             ('employee_grade', '=', g.id),
    #                         ]

    #                 check_lmt = self.env['limit.klaim'].sudo().search(domain_group)
    #                 if check_lmt:
    #                     pass
    #                 elif not check_lmt:
    #                     employee_obj = self.env['hr.employee'].search([('employee_grade', '=', g.id)])
    #                     print(employee_obj)

    #                     for e in employee_obj:

    #                         vals_lmt = []
    #                         lmt_klaim = self.env['limit.klaim'].sudo()
    #                         vals_lmt = {
    #                                 'employee_id' : e.id,
    #                                 'employee_grade': g.id,
    #                                 'claim_type_id':d.id,
    #                                 'batas_limit':d.limit_amount,
    #                                 'sisa_limit':d.limit_amount
    #                         }

    #                         create_lmt = lmt_klaim.create(vals_lmt)
    #                     print('else')

    #         result = super(ClaimType, self).write(vals)

    #         return result

# class LimitKlaim(models.Model):

#     _name = 'limit.klaim'

#     employee_id = fields.Many2one("hr.employee","Employee Name")
#     employee_grade = fields.Many2one('employee.grade','Employee Grade')
#     claim_type_id = fields.Many2one("claim.type","Employee Name")
#     batas_limit = fields.Float("Batas Limit")
#     sisa_limit = fields.Float("Sisa Limit")