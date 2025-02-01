{
    'name': 'Nati Report Invoice Line',
    'version': '1.0',
    'summary': 'Module to view and report invoice and refund lines for customers',
    'description': """
        This module provides a custom view to display and report invoice lines and refund lines associated with customers. 
        It aims to help users easily track and manage their financial documents related to customer transactions.
    """,
    'author': "Mali, MuhlhelITS",
    'website': "http://muhlhel.com",
    'license': 'OPL-1',
    'price': 1200.00,
    'currency': 'USD',
    'category': 'Accounting',
    'depends': ['base', 'account', 'web','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_invoice_lines_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    
}