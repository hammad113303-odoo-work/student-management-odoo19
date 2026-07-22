from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentClass(models.Model):
    _name = "student.class"
    _description = "Student Class"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Class Name",
        required=True,
    )

    section = fields.Char(
        string="Section",
    )

    teacher_id = fields.Many2one(
        "student.teacher",
        string="Class Teacher",
        required = True
    )

    room_no = fields.Char(
        string="Room Number",
    )

    capacity = fields.Integer(
        string="Capacity",
        default=30,
    )

    timing = fields.Selection(
        [
            ("morning", "Morning"),
            ("evening", "Evening"),
        ],
        string="Class Timing",
        default="morning",
    )

    academic_year = fields.Char(
        string="Academic Year",
    )

    active = fields.Boolean(
        default=True,
    )

    student_ids = fields.One2many(
        "student.student",
        "class_id",
        string="Students",
    )

    student_count = fields.Integer(
        string="Students",
        compute="_compute_student_count",
    )

    _sql_constraints = [
        (
            "unique_class_section",
            "unique(name, section)",
            "Class and Section must be unique!",
        ),
    ]

    @api.depends("student_ids")
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    @api.constrains("capacity")
    def _check_capacity(self):
        for rec in self:
            if rec.capacity <= 0:
                raise ValidationError(
                    "Capacity must be greater than zero."
                )