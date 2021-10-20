from .utils import assert_journy


class AccountIdentified(object):
    def __init__(self, account_id: str or None, domain: str or None):
        assert_journy(
            account_id or domain, "Account id and domain can not both be empty"
        )

        if account_id:
            assert_journy(
                isinstance(account_id, str), "The account id is not a string."
            )
        if domain:
            assert_journy(isinstance(domain, str), "The domain is not a string.")

        self.account_id = account_id
        self.domain = domain

    def format_identification(self):
        identification = {}
        if self.domain:
            identification["domain"] = self.domain
        if self.account_id:
            identification["accountId"] = self.account_id
        return identification

    @staticmethod
    def by_account_id(account_id: str):
        assert_journy(account_id, "Account id can not be empty!")
        return AccountIdentified(account_id, None)

    @staticmethod
    def by_domain(domain: str):
        assert_journy(domain, "Domain can not be empty!")
        return AccountIdentified(None, domain)

    def __str__(self):
        return f"AccountIdentified({self.account_id}, {self.domain})"

    def __repr__(self):
        return self.__str__()
