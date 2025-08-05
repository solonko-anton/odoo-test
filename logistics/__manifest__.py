{
    'name': 'Logistics',
    'depends': ['base', 'contacts', 'sale', 'sale_management'],
    'author': 'Anton',
    'category': 'Services',
    'description': "aabababab",
    'data': [
        'views/partner_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/vehicle_views.xml',
        'views/route_views.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True
}