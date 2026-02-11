{
    'name': 'Sale Order Report Visibility',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Demonstrate conditional report visibility in Odoo 18',
    'depends': ['sale'],
    'data': [
        'reports/sale_order_report.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
