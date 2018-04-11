from voluptuous import Required, Schema


user_schema = Schema({
    Required('username'): str,
    Required('password'): str,
    Required('superuser'): bool,
    Required('full_name'): str,
    Required('email'): str
})
