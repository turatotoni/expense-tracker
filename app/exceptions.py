class AppError(Exception):
    """Osnovna klasa za poslovne greške."""


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class InvalidInputError(AppError):
    pass

class UnauthorizedError(AppError):
    pass