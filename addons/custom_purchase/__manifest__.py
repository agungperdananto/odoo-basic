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
        'views/custom_purchase_tree_view.xml',
        'views/custom_purchase_form_view.xml',
        'views/custom_purchase_kanban_view.xml'

        ],
    'installlable': True,
    'license': 'OEEL-1'
    }