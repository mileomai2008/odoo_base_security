# -*- coding: utf-8 -*-
{
    'name': "Odoo Base Security",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "mileomai2008, Ahmed-Abdelrazek33, "mohamed1527",
    'sequence': -100,
    'application': True,

    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/res_config_setting.xml',
        'data/ir_cron.xml',
        'views/security_logs.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
