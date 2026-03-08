# copyright 2024 Compassion (David Wulliamoz <dwulliamoz@compassion.ch>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, models, fields, api
from odoo.tools import mod10r

# this class is highly inspired from l10n_ch/models/account_payment

class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ch_reference_warning_msg = fields.Char(compute='_compute_l10n_ch_reference_warning_msg')

    @api.onchange('partner_id', 'payment_reference', 'move_type')
    def _compute_l10n_ch_reference_warning_msg(self):
        for move in self:
            if move.move_type in  ('out_refund','in_refund','in_invoice','out_invoice') and\
                    move.partner_id.country_code in ['CH', 'LI'] and\
                    move.partner_bank_id.l10n_ch_qr_iban and\
                    not move._l10n_ch_reference_is_valid(move.payment_reference):
                move.l10n_ch_reference_warning_msg = _("Please fill in a correct QRR reference in the payment reference. The banks will refuse your payment file otherwise.")
            else:
                move.l10n_ch_reference_warning_msg = False

    def _l10n_ch_reference_is_valid(self, payment_reference):
        """Check if this invoice has a valid reference (for Switzerland)
        e.g.
        000000000000000000000012371
        210000000003139471430009017
        21 00000 00003 13947 14300 09017
        """
        self.ensure_one()
        if not payment_reference:
            return False
        ref = payment_reference.replace(' ', '')
        if re.match(r'^(\d{2,27})$', ref):
            return ref == mod10r(ref[:-1])
        return False
