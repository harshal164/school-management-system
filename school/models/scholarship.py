from odoo import fields,models


class scholarship(models.Model):
    _name = "student.scholarship"
    _description = "this is used for student details who applies for scholarship"
    _rec_name = "name"


    name=fields.Many2one('school.student',string="name",ondelete="set null")
    enrollment_no=fields.Char(related="name.enrollment_no",string="enrollment no")





    address=fields.Char(related="name.address",string="address",store=True)
    age=fields.Integer(related="name.age",string='Age')
    gender=fields.Selection(related="name.gender")

    email=fields.Char(related="name.email",string="email id")
    mobile_no=fields.Char(related="name.mobile_no",string="mobile no")
