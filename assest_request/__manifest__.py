{
    'name': 'Asset Request',
    'version': '18.0',
    'summary': 'Asset Requests',
    'description': """
      
    """,
    'author': 'Muhammed Jasim KA',
    'depends': ['base', 'contacts', 'mail', 'hr'],
    'data': [
        'security/asset_request_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/asset_request_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
