from rest_framework.exceptions import ValidationError


class IncorrectAuthorReview(ValidationError):
    """Exception raised when user tries to add
    more than one review to title"""


class IncorrectTitleInYear(ValidationError):
    """Exception raised when user tries to add incorrect year value"""
