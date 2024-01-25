{
    'name': 'Modul Custom Purchase',
    'version': '1.0.1',
    'category': 'purchase',
    'summary': 'purchase custom module',
    'description': '''
                Purchase Custom module for learning
        ''',
    'website': '',
    'author': 'agung p',
    'depends': ['web', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_view.xml',
        'views/purchase_menuitem.xml',
        'views/purchase_action.xml',

        ],
    'installlable': True,
    'license': 'OEEL-1'
    }