from email.policy import default
from odoo import api, fields, models, _
from datetime import datetime, time, timedelta
from odoo.http import request, Response
 

GET_APROVE = [
			('1', 'Claim'),
			('2', 'Excess'),
			]


class ApproveComment(models.TransientModel):
	_name = 'approve.medical.history.wizard'
	_description ="Medical Approve History"

	description = fields.Text("Description", required=True)
	type_aprove = fields.Selection(GET_APROVE,string='State')
	employee_id = fields.Many2one("hr.employee","Employee Name")

	def action_generate(self):
		model = self.env.context.get('active_model')
		docs = self.env[model].browse(self.env.context.get('active_id'))
		if self.type_aprove == '1':
			docs.state = 'hc'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Submitted',
				'comment' : self.description,
				})]
			docs.medical_history_ids = history
			self.employee_id= docs.employee_id.id

			template= self.env.ref('x_medical_insurance.email_kelengkapan_dokumen_claim')
			template.send_mail(docs.id, force_send=True)

			message_id = self.env['message.wizard'].create({'message': _("Email is successfully sent")})
			return {
				'name': _('Successfull'),
				'type': 'ir.actions.act_window',
				'view_mode': 'form',
				'res_model': 'message.wizard',
				'res_id': message_id.id,
				'target': 'new'}
			# docs.decrease_limit()
		
		if self.type_aprove == '2':
			docs.state = 'employee'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Submitted',
				'comment' : self.description,
				})]
			docs.excess_history_ids = history
			self.employee_id= docs.employee_id.id
			print(self)

			template= self.env.ref('x_medical_insurance.email_submit_to_employee_claim_excess')
			template.send_mail(docs.id, force_send=True)

			message_id = self.env['message.wizard'].create({'message': _("Email is successfully sent")})
			return {
				'name': _('Successfull'),
				'type': 'ir.actions.act_window',
				'view_mode': 'form',
				'res_model': 'message.wizard',
				'res_id': message_id.id,
				'target': 'new'}


GET_APROVE = [
			('1', 'Claim'),
			('2', 'Excess'),
			]


class ApproveCommentAfterSubmit(models.TransientModel):
	_name = 'approve.after.submit.medical.history.wizard'
	_description ="Medical Approve After Submit History"

	description = fields.Text("Description", required=True)
	type_aprove = fields.Selection(GET_APROVE,string='State')

	def action_generate_approve(self):
		model = self.env.context.get('active_model')
		docs = self.env[model].browse(self.env.context.get('active_id'))
		print(docs)
		if self.type_aprove == '1':
			docs.state = 'setlement'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Approved',
				'comment' : self.description,
				})]
			docs.medical_history_ids = history
		

		if self.type_aprove == '2':
			docs.state = 'employee'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Approved',
				'comment' : self.description,
				})]
			docs.excess_history_ids = history

GET_APROVE = [
			('1', 'Claim'),
			('2', 'Excess'),
			]

class RejectedWithComment(models.TransientModel):
	_name = 'reject.medical.history.wizard'
	_description ="Medical Reject History"

	description = fields.Text("Description", required=True)
	type_aprove = fields.Selection(GET_APROVE,string='State')
	employee_id = fields.Many2one("hr.employee","Employee Name")

	def action_generate_reject(self):
		model = self.env.context.get('active_model')
		docs = self.env[model].browse(self.env.context.get('active_id'))
		print(docs, 'docssss')
		if self.type_aprove == '1':
			docs.state = 'draft'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Rejected',
				'comment' : self.description,
				})]
			docs.medical_history_ids = history
			self.employee_id= docs.employee_id.id

			template= self.env.ref('x_medical_insurance.email_notif_reject')
			template.send_mail(self.id, force_send=True)

			message_id = self.env['message.wizard'].create({'message': _("Email is successfully sent")})
			return {
				'name': _('Successfull'),
				'type': 'ir.actions.act_window',
				'view_mode': 'form',
				'res_model': 'message.wizard',
				'res_id': message_id.id,
				'target': 'new'}
		

		if self.type_aprove == '2':
			docs.state = 'close'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Closed',
				'comment' : self.description,
				})]
			docs.excess_history_ids = history


GET_APROVE = [
			('1', 'Claim'),
			('2', 'Excess'),
			]


class CLoseCommentAfterSubmit(models.TransientModel):
	_name = 'close.after.submit.medical.history.wizard'
	_description ="Medical Close After Submit History"

	description = fields.Text("Description", required=True)
	type_aprove = fields.Selection(GET_APROVE,string='State')

	def action_generate_close(self):
		model = self.env.context.get('active_model')
		docs = self.env[model].browse(self.env.context.get('active_id'))
		print(docs)
		if self.type_aprove == '1':
			docs.state = 'close'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Closed',
				'comment' : self.description,
				})]
			docs.medical_history_ids = history

		if self.type_aprove == '2':
			docs.state = 'close'
			state = dict(docs._fields['state'].selection).get(docs.state)
			history = [(0,0,{
				'state' : 'Closed',
				'comment' : self.description,
				})]
			docs.excess_history_ids = history


		print(docs,'medicalmedicalmedicalmedicalmedicalmedicalmedicalmedicalmedicalmedical')

