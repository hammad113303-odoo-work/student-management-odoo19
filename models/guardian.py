from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StudentGuardian(models.Model):
    _name = "student.guardian"
    _description = "Student Guardian"
    _rec_name = "name"
    _order = "guardian_id"

    name = fields.Char(
        string="Guardian Name",
        required=True,
    )

    relationship = fields.Selection(
        [
            ("father", "Father"),
            ("mother", "Mother"),
            ("guardian", "Guardian"),
            ("uncle", "Uncle"),
            ("aunt", "Aunt"),
            ("brother", "Brother"),
            ("sister", "Sister"),
            ("other", "Other"),
        ],
        string="Relationship",
        required=True,
        )

    phone = fields.Char(
        string="Phone Number",
        required=True,
    )

    email = fields.Char(
        string="Email",
        
    )

    address = fields.Text(
        string="Address",
    )

    student_ids = fields.Many2many(
        "student.student",
        
        string="Students",
    )

    guardian_id = fields.Char(
        string="Guardian ID",
        required=True,
        readonly=True,
        copy=False,
        default="New",
    )

    cnic = fields.Char(
        string="CNIC",
        
    )

    occupation = fields.Char(
        string="Occupation",
    )
    photo = fields.Image(
        string="Photo",
    )
     
    active = fields.Boolean(
        default=True,
    )
    student_count = fields.Integer(
        string="Students",
        compute="_compute_student_count",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("guardian_id", "New") == "New":
                vals["guardian_id"] = self.env["ir.sequence"].next_by_code(
                    "student.guardian"
                ) or "New"

        return super().create(vals_list)
    @api.depends("student_ids")
    def _compute_student_count(self):
         for rec in self:
            rec.student_count = len(rec.student_ids)

    def action_view_students(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "res_model": "student.student",
            "view_mode": "list,form",
            "domain": [("id", "in", self.student_ids.ids)],
        }