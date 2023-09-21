from odoo import models, fields, api, _


class InheritIRUIView(models.Model):
    _inherit = "ir.ui.view"

    @api.model
    def create(self, vals):
        rec = super(InheritIRUIView, self).create(vals)
        param = {'record_id': rec.id,
                 'table': self._table,
                 'vals': vals,
                 'operation': 'create'}
        self.env["res.config.settings"].sudo().check_allowed_users(param)
        return rec

    def write(self, vals):
        param = {'record_id': self.id,
                 'table': self._table,
                 'vals': vals,
                 'operation': 'write'}
        self.env["res.config.settings"].sudo().check_allowed_users(param)
        return super(InheritIRUIView, self).write(vals)

    def unlink(self):
        for rec in self:
            param = {'record_id': rec.id,
                     'table': self._table,
                     'vals': '',
                     'operation': 'unlink'}
            rec.env["res.config.settings"].sudo().check_allowed_users(param)
        return super(InheritIRUIView, self).unlink()
