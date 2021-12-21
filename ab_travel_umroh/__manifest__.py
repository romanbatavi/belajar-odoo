# -*- coding: utf-8 -*-
{
    'name': "Umroh Travel",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PT.Ismata Nusantara Abadi",
    'website': "http://ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sequence_data.xml',
        'views/produk_views.xml',
        'views/paket_produk_views.xml',
        'views/jamaah_views.xml',
        'views/airlines_views.xml',
        'views/hotels_views.xml',
        'views/travel_package_views.xml',
        'views/customer_invoice_views.xml',
        'views/sales_order_views.xml',
        'views/menuitem_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application":True
}
