class CaseUserException(Exception):
    pass


class NotLoggedInException(CaseUserException):
    pass


class UnAuthorized(CaseUserException):
    pass


class BadRequest(CaseUserException):
    pass