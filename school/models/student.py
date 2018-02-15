from odoo import fields, models, api, exceptions
from datetime import date
import datetime
from odoo.exceptions import ValidationError, Warning


class Student(models.Model):
    _name = "school.student"
    _description = "this is student model"
    _rec_name = "name"
    enrollment_no = fields.Char(string="number", default=lambda self: self.env['ir.sequence'].get('student.student'))
    name = fields.Char(string="name")
    name_title = fields.Char(related="name")
    address = fields.Char(string="address")
    born = fields.Date(string="dob")
    gender = fields.Selection([(1, 'male'), (2, 'female'), (3, 'transgender')], default=1)
    photo = fields.Binary(string="photo")
    aadhar_doc = fields.Binary(string="aadhar document")
    aadhar = fields.Char('aadhar_doc')
    isobc = fields.Selection([(1, 'yes'), (2, 'no')], string="Are you in obc?", default=2)
    uploadobc = fields.Binary(string="certi")
    email = fields.Char(string="email id")
    mobile_no = fields.Char(string="mobile no", digit=(10, 0), required=True)
    school_id = fields.Many2one('school.school', string='school id')
    student_school_id = fields.Char(string="student's school code")

    @api.onchange('school_id')
    def onchange_school_code(self):
        self.student_school_id = self.school_id.school_code

    # @api.multi
    # def calculate_age(self):
    #    if self.age:
    #         today=date.today()
    #         print(type(self.born),":::::::::::::::::::::::::::::::::::::::")
    #         born = datetime.date(int(self.born[0:4]), int(self.born[5:7]), int(self.born[9:]))
    #         timedelta=today-born
    #         self.age=(timedelta.days)/365
    #    else:
    #        self.age=0




    @api.multi
    def calculate_age(self):
        if self.born:
            today = date.today()
            print(type(self.born), ":::::::::::::::::::::::::::::::::::::::")
            born = datetime.date(int(self.born[0:4]), int(self.born[5:7]), int(self.born[9:]))
            timedelta = today - born
            self.age = (timedelta.days) / 365
        else:
            self.age = 0

    @api.onchange('gender')
    def onchande_gender(self):

        rec = {}
        if self.gender == 3:
            rec['warning'] = {
                'title': 'rushi\'s warning',
                'message': 'your not eligible to get admission'
            }
        return rec

    @api.onchange('student_age')
    def onchange_student_age(self):
        if self.student_age < 18:
            raise Warning("you are beow 18")

    teacher_ids = fields.Many2many('school.teacher', 'student_teacher_relation_table', 'stud_id', 'teach_id')
    student_standard = fields.Many2one('school.standard', string="student ")
    type = fields.Selection(related="student_standard.type")
    admission_date = fields.Datetime(string="date and time")
    subject_ids = fields.Many2many('school.subject', 'standard', string="subject")
    student_scholarship = fields.Many2one("student.scholarship", string="student scholarship")
    age = fields.Integer(string='Age', compute="calculate_age")
    student_age = fields.Integer(string="Student Age")
    evenodd = fields.Selection([('1', 'even'), ('2', 'odd')], default='1')
    semester = fields.Many2one('school.evenodd', 'semester')

    @api.onchange('evenodd')
    def onchange_evenodd(self):

        res = {}

        print "hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeEEEEEEE:::::::::::::::::::::::::::"

        res['domain'] = {'semester': [('evenodd', '=', self.semester.iseven)]}
        print res
        return res

    @api.constrains('age')
    def age_validation(self):
        if self.age < 3:
            raise ValidationError("not valid age")

    @api.multi
    def calculate_total(self):
        total = 0
        for rec in self.obtained_marks:
            total += rec.obtained
        self.total_marks = total

    @api.multi
    def calculate_percentage(self):

        total = 0
        count = 0
        for rec1 in self:  # here rec1 is just used for tree view to avoid singleton error
            if rec1.obtained_marks:
                for rec in rec1.obtained_marks:
                    total += rec.obtained
                    count += rec.total
                rec1.percentage = (total * 100 / count)
            else:
                rec1.percentage = 0

    select = fields.Reference(
        selection=[("student.scholarship", "scholarship"), ("school.teacher", "tecaher"), ('school.school', "school")],
        string="reference")
    expense_val = fields.Many2one('res.currency', 'currency')
    expense = fields.Monetary(currency_field="expense_val", string="fees")
    obtained_marks = fields.One2many('marks', 'stud_id', 'obtainde marks')
    total_marks = fields.Integer(string="total marks", compute="calculate_total")
    percentage = fields.Integer(compute='calculate_percentage')


class marks(models.Model):
    _name = "marks"
    _rec_name = "obtained"
    total = fields.Integer()
    obtained = fields.Integer()
    subject_name = fields.Many2one('school.subject', string="subject name")
    stud_id = fields.Many2one('school.student', "student id")


class evenodd(models.Model):
    _name = 'school.evenodd'

    iseven = fields.Selection([('1', 'even'), ('2', 'odd')], default='1')
    semester = fields.Selection([('1', '1'), ('2', '2')])
