# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MarketingFee(models.Model):
	_inherit = 'sale.order'

	od_id = fields.Many2one('res.partner', string='OD', domain=[('category_id.name', '=', 'OD')])

	def _prepare_invoice(self):
		res = super(MarketingFee,self)._prepare_invoice()
		# for res in self	:
		# 	invoice_vals = {
		# 		'od_id' : self.od_id.name
		# 	}
		return res

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	od_id = fields.Many2one('res.partner', string='OD', domain=[('category_id.name', '=', 'OD')])

	def action_invoice_open(self):
		res = super(AccountInvoice, self).action_invoice_open()
		object_journal = self.env['account.journal'].search([('type','=','purchase')])
		account = self.env['account.account'].search([('user_type_id','=','Payable')])
		unit_price = self.partner_id.marketing_fee * self.amount_total / 100.0
		self.ensure_one()
		for res in self:
			# if object_journal.journal_id.type == 'purchase' and object_journal.journal_id.name == 'Vendor Bills':
				inv_line_vals = []
				inv_line_vals.append((0,0,{
					'name': 'Disposal %s'%(self.name),
					'account_id': account.id,
					'quantity': 1,
					# 'invoice_line_tax_ids': [(6,None,self.disposal_line.disposal_tax.ids)],
					'price_unit': unit_price 
					# self.disposal_line.value_residual,self.parnter_id.marketing_fee * self.amount_total / 100.0
				}))

				invoice_id = self.env['account.invoice'].create({
					'partner_id': self.od_id,
					'journal_id': object_journal.id,
					'reference' : self.name,
					'account_id': account.id,
					'type': 'in_invoice',
					'origin': self.name,
					'invoice_line_ids': inv_line_vals,
					'comment': "Marketing Fee",
				})
		return res

class VendorMarketing(models.Model):
	_inherit = 'res.partner'

	marketing_fee = fields.Integer(string="Marketing Fee")