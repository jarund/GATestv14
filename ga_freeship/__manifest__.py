# -*- coding: utf-8 -*-
{
    'name': "ga_freeship",

    'summary': """
        Set up and tracking for PO's that are eligble for free shipping.""",

    'description': """
        Set up and tracking for PO's that are eligble for free shipping.
    """,

    'author': "Talus ERP",
    'website': "http://www.taluserp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
