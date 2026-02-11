{
    'name': 'POS Custom M2O Field',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        # 'models/pos_order.xml', # To install the new field in the database
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'many2one_pos/static/src/js/models.js',
            'many2one_pos/static/src/js/CustomMany2oneComponent.js',
            'many2one_pos/static/src/xml/PartnerButton.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
}