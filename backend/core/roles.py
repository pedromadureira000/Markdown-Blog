from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        "make_post": True,
        "delete_post": True,
        "update_post": True,
        "comment_on_post": True,
        "create_guest": True,
        "create_member": True,
        "delete_user": True,
        "get_users": True,
    }


class Guest(AbstractUserRole):
    available_permissions = {
        "comment_on_post": True,
    }


class Member(AbstractUserRole):
    available_permissions = {
        "make_post": True,
        "delete_post": True,
        "update_post": True,
        "comment_on_post": True,
    }
