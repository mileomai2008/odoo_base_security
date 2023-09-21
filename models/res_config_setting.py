# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request
import uuid

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    activate_feature = fields.Boolean(string="Activate Feature", default=False)
    debuggers = fields.Char(string="Debuggers", help="""Ids separated with a coman.
    For example: 1,2,3,4""")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            activate_feature=self.env["ir.config_parameter"].sudo().get_param("activate_feature"),
            debuggers=self.env["ir.config_parameter"].sudo().get_param("debuggers"),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        self.env["ir.config_parameter"].sudo().set_param("debuggers", self.debuggers)
        self.env["ir.config_parameter"].sudo().set_param("activate_feature", self.activate_feature)

    def check_allowed_users(self, kwargs):
        """Function to check if the feature of not allowing changing the core data by admin users is activated
        and if the user using the system is allowed to change in the core."""
        if self.env["res.config.settings"].sudo().get_values()["activate_feature"]:
            _logger.info(_("Iron Fist Is Activate"))
            _logger.info(_(f"Checking if user ID:{self._uid} is a debugger"))
            debuggers = self.env["res.config.settings"].sudo().get_values()["debuggers"].strip()
            if str(self._uid) not in list(debuggers.split(",")):
                _logger.info(_(f"The user  ID:{self._uid} tried change the core but he is not a debugger."))
                raise ValidationError(_("You are not allowed to change "
                                        "the system core please contact the administrator."))
            self.add_to_log_table(kwargs)
            _logger.info(_(f"User  ID:{self._uid} is a debugger and has made an alteration."))
        else:
            _logger.info(_("Iron Fist Is Deactivate"))

    @staticmethod
    def get_user_info():

        ip_address = request.httprequest.remote_addr
        #mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

        return ip_address

    def add_to_log_table(self, kwargs):
        """Adding to the new the security_logs table the changes made to the core models."""

        table = kwargs['table']
        record_id = kwargs['record_id']
        operation = kwargs['operation']
        details = str(kwargs['vals']).replace("'", "")
        ip_address = self.get_user_info()
        time_to_minute = str(fields.Datetime.now())[0:16]
        notes = f"""The user  {self.env.user.name} ID: {self.env.user.id} with the IP {ip_address} has
        preformed a ({operation}) operation on the table ({table}) at ({time_to_minute}).

        More details about the altered vals: {details [0:5000]} """

        vals = {"table": table,
                "record_id": record_id,
                "user_id": self._uid,
                "notes": notes}
        self.env['security.logs'].sudo().create(vals)
        self._cr.execute(
            f"""DELETE FROM security_logs 
            WHERE id not in 
                (SELECT max(id) 
                FROM security_logs 
                WHERE notes='{notes}'
                Group BY date::date,notes,user_id,"table",record_id)
            and notes='{notes}';
                
            """)
