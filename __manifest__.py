# -*- coding: utf-8 -*-
{
    'name': "Smart Recommender AI",
    'summary': "Predictive recommendation engine for Sales using AI",
    'description': """
        Academic AI Module for Odoo.
        Uses 'Apriori' algorithm to suggest cross-selling opportunities.
    """,
    'author': "Hassan BADIR",
    'website': "https://github.com/8sylla/odoo-ai-recommender",
    'category': 'Sales/Sales',
    'version': '17.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/recommendation_views.xml',
        'views/sale_order_views.xml', 
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,

    'demo': [
        'demo/demo.xml',
    ],
}