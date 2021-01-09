# Copyright 2020 David Wulliamoz
# License AGPL-3.0 or later (https://www.gnuorg/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import UserError

class Gen_SD_Wizard(models.TransientModel):
    _name = 'hr.salary_declaration.wizard'
    _description = 'Generate salary declaration'

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')
    grossincome_id = fields.Many2one(comodel_name='hr.salary.rule', string='Gross income code')
    social_deduction_code_ids = fields.Many2many(comodel_name='hr.salary.rule', string='social deduction codes',
                                                 relation='social_codes_salary_declaration_rel')
    pension_deduction_code_ids = fields.Many2many(comodel_name='hr.salary.rule', string='pension deduction codes',
                                                  relation='pension_codes_salary_declaration_rel')


    def gen_sd(self):
        sd_obj = self.env['hr.salary_declaration']
        sd_obj.generate_yearly_declaration(self.date_from, self.date_to,
                                           self.grossincome_id.code,
                                           self.social_deduction_code_ids.mapped('code'),
                                           self.pension_deduction_code_ids.mapped('code'))
