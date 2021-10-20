from .utils import assert_journy


class UserIdentified(object):
    def __init__(self, user_id: str or None, email: str or None):
        assert_journy(user_id or email, "User id and email can not both be empty")

        if user_id:
            assert_journy(isinstance(user_id, str), "The user id is not a string.")
        if email:
            assert_journy(isinstance(email, str), "The email is not a string.")

        self.user_id = user_id
        self.email = email

    def format_identification(self):
        identification = {}
        if self.email:
            identification["email"] = self.email
        if self.user_id:
            identification["userId"] = self.user_id
        return identification

    @staticmethod
    def by_user_id(user_id: str):
        assert_journy(user_id, "User id can not be empty!")
        return UserIdentified(user_id, None)

    @staticmethod
    def by_email(email: str):
        assert_journy(email, "Email can not be empty!")
        return UserIdentified(None, email)

    def __str__(self):
        return f"UserIdentified({self.user_id}, {self.email})"

    def __repr__(self):
        return self.__str__()
