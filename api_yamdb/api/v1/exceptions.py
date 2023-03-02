from rest_framework.exceptions import NotFound, ValidationError


class TitleOrReviewNotFound(NotFound):
    """Exception raised when Title or Review ID url did not match any object"""


class IncorrectAuthorReview(ValidationError):
    """Exception raised when user tries to add
    more than one review to title"""


class IncorrectTitleInYear(ValidationError):
    """Exception raised when user tries to add incorrect year value"""
