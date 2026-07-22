from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentSubject(models.Model):
    _name = "student.subject"
    _description = "Student Subject"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Subject Name",
        required=True,
    )

    code = fields.Char(
        string="Subject Code",
        required=True,
    )

    credit_hours = fields.Integer(
        string="Credit Hours",
        default=3,
    )

    teacher = fields.Char(
        string="Teacher",
    )

    marks = fields.Float(
        string="Marks",
    )

    active = fields.Boolean(
        default=True,
    )

    student_id = fields.Many2one(
        "student.student",
        string="Student",
        required=True,
        ondelete="cascade",
    )

    result = fields.Selection(
        [
            ("pass", "Pass"),
            ("fail", "Fail"),
        ],
        string="Result",
        compute="_compute_result",
        store=True,
    )

    _sql_constraints = [
        (
            "unique_subject_code",
            "unique(code)",
            "Subject Code must be unique!",
        ),
    ]

    @api.depends("marks")
    def _compute_result(self):
        for rec in self:
            rec.result = "pass" if rec.marks >= 50 else "fail"

    @api.constrains("marks")
    def _check_marks(self):
        for rec in self:
            if rec.marks < 0 or rec.marks > 100:
                raise ValidationError(
                    "Marks must be between 0 and 100."
                )

    @api.constrains("credit_hours")
    def _check_credit_hours(self):
        for rec in self:
            if rec.credit_hours <= 0:
                raise ValidationError(
                    "Credit Hours must be greater than zero."
                )

    def name_get(self):
        result = []
        for rec in self:
            display = f"[{rec.code}] {rec.name}"
            result.append((rec.id, display))
        return result