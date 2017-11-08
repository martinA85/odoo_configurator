# -*- coding: utf-8 -*-
{
    'name': "Configurateur de produit",
    'js': ['static/js/config.js'],
    'test': ['static/js/config.js'],
    'summary': """
        Permet de configurer un produit""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Martin Allimonier",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product', 'website_sale', 'website'],

    "external_dependencies": {
        'python': ['PIL','io']
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/template_front_v.xml',
        'views/templates_front.xml'
    ],
    # 'application': True,
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}