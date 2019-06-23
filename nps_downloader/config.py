"""
Configures access to the NPS API and where to store results
"""


def data_dir() -> str:
    """The directory where result data is written to"""
    return '/tmp/nps'


def first_date() -> str:
    """The first day for which data is downloaded"""
    return '2015-01-01'


def access_token() -> str:
    """The access token of the system user as part of the header ('Authorization'), example:
    {
        'Authorization': 'Token 123456789',
        'Content-Type': 'application/json'
    }
    """
    return 'Token 123456789'
