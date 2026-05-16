class ApplicationError(Exception):
    status_code = 400


class NotFoundError(ApplicationError):
    status_code = 404


class ConflictError(ApplicationError):
    status_code = 409


class ForbiddenError(ApplicationError):
    status_code = 403


class ValidationError(ApplicationError):
    status_code = 400
