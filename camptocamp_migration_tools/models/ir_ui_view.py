# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    active_backup = fields.Boolean(
        string="Active (backup)",
        # NOTE: do not use 'related="active"' on purpose. Having a compute
        # method ensures 'active_backup' field is synced with 'active' field only
        # on environments having the module code available, so not on Odoo S.A.
        # Upgrade platform.
        # Indeed related fields can be computed directly by Odoo even if current
        # module is not available on the system (i.e. when sending the DB for
        # migration to Odoo S.A. Upgrade service).
        compute="_compute_active_backup",
        store=True,
        help=(
            "Store the value of 'active' field to help on the migration.\n"
            "Odoo S.A. disables views that can't be applied during their "
            "database migration process, and we need to restore the previous "
            "values at the end of our own migration."
        ),
    )

    @api.depends("active")
    def _compute_active_backup(self):
        for rec in self:
            rec.active_backup = rec.active
