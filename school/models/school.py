
from odoo import models,fields
import datetime


class School(models.Model):
    _name = "school.school"
    _description = "school_management_system"

    id=fields.Integer( default=lambda self: self.env['ir.sequence'].get('teacher.sequence'))
    school_id=fields.Integer(string="school id")
    logo=fields.Binary(string="logo")
    name=fields.Char(string="name")
    address=fields.Char(string="address")
    name_title = fields.Char(related="name")
    address_title=fields.Char(related="address")
    about_us=fields.Html(string="about us")
    school_code=fields.Char(string="school code", size=4,copy=False)
    teacher_ids=fields.One2many('school.teacher','school_id',string='teachers')
    priority=fields.Selection([('0','very bad'),('1','bad'),('2','average'),('3','good'),('4','very good'),('5','excellent')])
    department_ids=fields.Many2many('school.department','school_dept_rel','school_id','dept_id')
    email=fields.Char(string="email id")
    website=fields.Char(string="web site")



class Teacher(models.Model):
    _name = "school.teacher"
    _description = "this is teacher model"
    name=fields.Char(string="name")
    name_title=fields.Char(related="name")
    age=fields.Integer(string='Age')
    gender=fields.Selection([(1,'male'),(2,'female')],default=1)
    photo=fields.Binary(string="photo")
    school_id=fields.Many2one('school.school',string="school id")
    dept_id=fields.Many2one('school.department',string="department id")
    job_position=fields.Selection([(1,'assistant professor'),(2,'head of department'),(3,'lab assistant'),(4,'principal')])

class standard(models.Model):
    _name = "school.standard"
    _description = "no of standards in school"
    _rec_name="standard"
    standard=fields.Integer(string="standard")
    type=fields.Selection([('primary','primary'),('secondary','secondary'),('higher secondary','higher secondary')])




class subject(models.Model):
    _name = "school.subject"
    _description = "subject of student"
    _rec_name = "subject"
    subject=fields.Char(string="subject name")
    standard=fields.Many2one('school.standard',string="standard")
    type=fields.Selection(related="standard.type")
    marks=fields.Float()



class Department(models.Model):
    _name="school.department"
    _description="department of school"
    name=fields.Char(string="department name")
    code=fields.Char(string="code" ,size=4)