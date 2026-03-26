from marshmallow import fields,Schema,validate


#USER APIs
class SignupSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1,max=20))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class ChangeSchema(Schema):
    oldpassword = fields.Str(required=True, validate=validate.Length(min=6))
    newpassword = fields.Str(required=True, validate=validate.Length(min=6))


class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    completed = fields.Bool(required=False)

class GeneralSchema(Schema):
    pass

class AdminSchema(Schema):
    asignee_id = fields.Int(required=True)
class TaskDetailViewSchema(Schema):
    task_id = fields.Int(required=True)

class TaskUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    completed = fields.Bool(required=False)

class TaskDeleteSchema(Schema):
    task_id = fields.Int(required=True)