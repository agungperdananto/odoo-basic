{
    'name': 'Modul Custom Purchase',
    'version': '1.0.1',
    'category': 'purchase',
    'summary': 'purchase custom module',
    'description': '''
                Purchase Custom module for learning.
                And testing
        ''',
    'website': '',
    'author': 'Agung Perdananto',
    'depends': ['web', 'base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_purchase_view.xml',
        'views/custom_purchase_kanban_view.xml'

        ],
    'installlable': True,
    'license': 'OEEL-1'
    }