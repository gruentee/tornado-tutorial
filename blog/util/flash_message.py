"""(c) Bahman Movaqar, http://www.bahmanm.com/blogs/python-tornado-flash"""


class Flash(object):
    """
    A flash message along with optional (form) data.
    """

    def __init__(self, message, data=None):
        """
        'message': A string.
        'data': Can be anything.
        """
        self.message = message
        self.data = data
