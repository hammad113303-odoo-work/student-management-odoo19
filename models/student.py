from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = "student.student"
    _description = "Student"
    _rec_name = "name"
    _order = "student_id desc"

    _sql_constraints = [
        (
            "unique_email",
            "unique(email)",
            "Email already exists!",
        ),
    ]

    # ==========================================================
    # Basic Information
    # ==========================================================
    guardian_ids = fields.Many2many(
        "student.guardian",
        string="Guardians",
    )
    class_id = fields.Many2one(
    "student.class",
    string="Class",
    ondelete="set null",
    )
    student_id = fields.Char(
        string="Student ID",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )

    name = fields.Char(
        string="Student Name",
        required=True,
    )

    age = fields.Integer(
        string="Age",
    )

    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
    )

    email = fields.Char(
        string="Email",
    )

    admission_date = fields.Date(
        string="Admission Date",
    )

    active = fields.Boolean(
        default=True,
    )

    photo = fields.Image(
        string="Photo",
    )

    notes = fields.Text(
        string="Notes",
    )

    # ==========================================================
    # Academic
    # ==========================================================

    marks = fields.Float(
        string="Marks",
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

    subject_ids = fields.One2many(
        "student.subject",
        "student_id",
        string="Subjects",
    )

    subject_count = fields.Integer(
        string="Subjects",
        compute="_compute_subject_count",
    )

    # ==========================================================
    # Status
    # ==========================================================

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("admitted", "Admitted"),
            ("graduated", "Graduated"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # ==========================================================
    # Create
    # ==========================================================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("student_id", "New") == "New":
                vals["student_id"] = self.env["ir.sequence"].next_by_code(
                    "student.student"
                ) or "New"

        return super().create(vals_list)

    # ==========================================================
    # Computes
    # ==========================================================

    @api.depends("marks")
    def _compute_result(self):
        for rec in self:
            rec.result = "pass" if rec.marks >= 50 else "fail"

    @api.depends("subject_ids")
    def _compute_subject_count(self):
        for rec in self:
            rec.subject_count = len(rec.subject_ids)

    # ==========================================================
    # Buttons
    # ==========================================================

    def action_admit(self):
        self.state = "admitted"

    def action_graduate(self):
        self.state = "graduated"

    def action_reset(self):
        self.state = "draft"

    def action_view_subjects(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Subjects",
            "res_model": "student.subject",
            "view_mode": "list,form",
            "domain": [("student_id", "=", self.id)],
            "context": {
                "default_student_id": self.id,
            },
        }

    # ==========================================================
    # Constraints
    # ==========================================================

    @api.constrains("marks")
    def _check_marks(self):
        for rec in self:
            if rec.marks < 0 or rec.marks > 100:
                raise ValidationError(
                    "Marks must be between 0 and 100."
                )

    @api.constrains("age")
    def _check_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError(
                    "Age must be greater than 0."
                )

    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            if rec.email and "@" not in rec.email:
                raise ValidationError(
                    "Please enter a valid email address."
                )

    @api.constrains("name")
    def _check_name(self):
        for rec in self:
            if not rec.name or not rec.name.strip():
                raise ValidationError(
                    "Student name cannot be empty."
                )

    # ==========================================================
    # Display Name
    # ==========================================================

    def name_get(self):
        result = []

        for rec in self:
            result.append(
                (
                    rec.id,
                    f"{rec.student_id} - {rec.name}",
                )
            )

        return result