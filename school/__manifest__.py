{
    'name':'School Management',
    'version':'1.0',
    'category':'Education',
    'summary':'school management system',
    'description':"""
    
    this module is used to mange school resources
    """,
    'depends':['base'],
    'data':['view/school_view.xml',
            'view/student_view.xml',
            'view/teacher_view.xml',
            'view/scholarship_view.xml',
            'view/subject_view.xml',
            'view/department_view.xml',
            'data/student_sequence.xml'],
    'installable':True,
    'auto_install':False,
    'application':True

}
