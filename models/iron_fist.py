from odoo import models, fields , api
from datetime import datetime, timedelta

class IronFist(models.Model):
    _name = "security.logs"
    _description = "Security Logs"

    date = fields.Datetime(string="Change Date", default=lambda self: fields.Datetime.now())
    notes = fields.Text(string="Notes")
    table = fields.Char(string="Models")
    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.uid)
    record_id = fields.Integer(string="Record ID")

    def clear_log_table(self, date):

        if self.env['security.logs'].sudo().search([('date', '<=', date)]):
            self._cr.execute(
                f"""DELETE  from security_logs 
                where date<='{date}'
            """)
            ip_address = self.env["res.config.settings"].sudo().get_user_info()
            vals = {"table": self._table,
                    "user_id": self._uid,
                    "notes": f"The user  {self.env.user.name} ID: {self.env.user.id} with the "
                             f"IP {ip_address} has cleared "
                             f"the{self._table} up to the date {date}."}
            self.env['security.logs'].sudo().create(vals)
        else:
            pass

    @api.model
    def _cron_clear_logs(self):
        today = datetime.today()
        last_year = today - timedelta(days=365)
        date = last_year.strftime('%Y-%m-%d')

        self.clear_log_table(date)
