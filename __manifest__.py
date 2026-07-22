{
    'name': 'Student Management',
    'version': '19.0.1.0.0',
    'summary': 'Student Management System',
    'description': 'A simple Student Management module for learning Odoo.',
    'author': 'Hammad Ali',
    'website': '',
    'category': 'Services/Education',
    'depends': ['base'],
    'data': [
        'security/student_security.xml',
        'security/ir.model.access.csv',

        'data/student_sequence.xml',
        'data/teacher_sequence.xml',
        'data/guardian_sequence.xml',


        'views/student_views.xml',
        'views/student_class_views.xml',
        'views/teacher_views.xml',
        'views/guardian_views.xml',

        

        
        'reports/student_report.xml',
        'reports/report_action.xml',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}