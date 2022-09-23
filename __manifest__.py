# -*- coding: utf-8 -*-
{
    'name': "Medical Insurance",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr','x_employee_status_grade'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/medical_claim.xml',
        'views/excess_claim.xml',
        'views/client_type.xml',
        # 'views/limit_claim.xml',
        'views/menu.xml',
        'wizard/approve_history.xml',
        'data/email_template.xml',
        'wizard/message.xml'
    ]
}
