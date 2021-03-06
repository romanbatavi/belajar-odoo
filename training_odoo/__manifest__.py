# -*- coding: utf-8 -*-
{
    'name': "Training Odoo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Roman",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/report_action.xml',
        'report/report_training_session.xml',
        'views/sequence_data.xml',
        'views/scheduler_data.xml',
        'views/course_views.xml',
        'views/partner_views.xml',
        'views/session_views.xml',
        'views/attende_views.xml',
        'views/menuitem_views.xml',
        'wizard/training_wizard_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application":True
}