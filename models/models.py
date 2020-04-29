# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	od_id = fields.Many2one('res.partner', string='OD', domain=[('category_id.name', '=', 'OD')])

	def _prepare_invoice(self):
		invoice_vals = super(SaleOrder,self)._prepare_invoice()

		if not self.od_id:
			return invoice_vals

		invoice_vals.update({
			'od_id': self.od_id.id,
		 })

		_logger.info("-------- invoice vals %s", invoice_vals)
		return invoice_vals

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	marketing_pct = fields.Float(string="Market Pct(%)")
	marketing_nom = fields.Float(string="Market Nominal")

	def _prepare_invoice_line(self, qty):
		res = super(SaleOrderLine,self)._prepare_invoice_line(qty)
		res.update({
			'marketing_pct': self.marketing_pct,
			'marketing_nom': self.marketing_nom
		})
		
		_logger.info("-------- res %s", res)
		return res

class AccountInvoiceLine(models.Model):
	_inherit = 'account.invoice.line'

	marketing_pct = fields.Float(string="Market Pct(%)")
	marketing_nom = fields.Float(string="Market Nominal")

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	od_id = fields.Many2one('res.partner', string='OD', domain=[('category_id.name', '=', 'OD')])
	
	def action_invoice_open(self):
		res = super(AccountInvoice, self).action_invoice_open()
		if self.type != 'out_invoice' or not self.od_id:
			return res
		self.ensure_one()
		object_journal = self.env['account.journal'].search([('type','=','purchase')], limit=1)
		account = self.env['account.account'].search([('user_type_id','=','Payable')], limit=1)
		marketing_fee = self.env['product.template'].search([('name','=','Marketing Fee')], limit=1)
		unit_price = 0.0
		for line in self.invoice_line_ids:
			unit_price += (line.marketing_pct/100.0) * line.price_unit + line.marketing_nom
		
		inv_line_vals = []
		inv_line_vals.append((0,0,{
			# 'name': 'Disposal %s'%(self.name),
			'product_id': marketing_fee.id,
			'name': 'Marketing Fee',
			'account_id': account.id,
			'quantity': 1,
			'price_unit': unit_price 
		}))

		_logger.info("---- od %s",self.od_id)

		invoice_id = self.env['account.invoice'].create({
			# 'partner_id': self.od_id,
			'partner_id': self.od_id.id,
			'journal_id': object_journal.id,
			'reference' : self.number,
			'account_id': account.id,
			'type': 'in_invoice',
			'origin': self.origin,
			'invoice_line_ids': inv_line_vals,
			'comment': "Marketing Fee: %s" % self.origin ,
		})
		invoice_id.action_date_assign()
		invoice_id.action_move_create()
		invoice_id.invoice_validate()
		# invoice_id.write({'state': 'open'})
		return res
		

class Partner(models.Model):
	_inherit = 'res.partner'

	bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Banks')