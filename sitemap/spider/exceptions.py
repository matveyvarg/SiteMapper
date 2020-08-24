class NoDomainException(Exception):
    """
    If domain wasn't passed, and started_urls are empty
    """
    pass


class GettingPageException(Exception):
    """
    If status of page is not 200
    """
    pass


class PossibleSPAException(Exception):
    """
    If page contains no links, try to use selenium
    """
    pass
