from odoo import models, fields, api


class Teacher(models.Model):
    _name = "student.teacher"
    _description = "Teacher"
    _rec_name = "name"
    _order = "teacher_id"

    teacher_id = fields.Char(
        string="Teacher ID",
        required=True,
        readonly=True,
        copy=False,
        default="New"
    )

    name = fields.Char(
        string="Teacher Name",
        required=True
    )

    email = fields.Char(
        string="Email"
    )

    phone = fields.Char(
        string="Phone"
    )

    qualification = fields.Char(
        string="Qualification"
    )

    experience = fields.Integer(
        string="Experience (Years)"
    )

    joining_date = fields.Date(
        string="Joining Date"
    )

    active = fields.Boolean(
        default=True
    )

    photo = fields.Image(
        string="Photo"
    )
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("teacher_id", "New") == "New":
                vals["teacher_id"] = self.env["ir.sequence"].next_by_code(
                    "student.teacher"
                ) or "New"

        return super().create(vals_list)