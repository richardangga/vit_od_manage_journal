# -*- coding: utf-8 -*-
{
    'name': "vit_od_manage_journal",

    'summary': """
        Markerting Fee Invoice Vendor Bill""",

    'description': """
        Markerting Fee Invoice Vendor Bill
    """,

    'author': "Richard Anggaswara",
    'website': "http://www.vitraining.com",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','contacts','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/product.xml',
        'demo/res_partner_category.xml',
    ],
}