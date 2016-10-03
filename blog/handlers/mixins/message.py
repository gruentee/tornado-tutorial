import re
import pickle
from tornado.escape import to_unicode
from tornado import web, escape
from tornado.web import RequestHandler

class FlashMixin(RequestHandler):
    """
    Extends Tornado's RequestHandler by adding flash functionality.

    (c) Bahman Movaqar http://www.bahmanm.com
    """

    def _cookie_name(self, key):
        return key + '_flash_cookie' # change this to store/retrieve flash
                                    # cookies under a different name

    def _get_flash_cookie(self, key):
        return self.get_cookie(self._cookie_name(key))

    def has_flash(self, key):
        """
        Returns true if a flash cookie exists with a given key (string);
        false otherwise.
        """
        return self._get_flash_cookie(key) is not None

    def get_flash(self, key):
        """
        Returns the flash cookie under a given key after converting the
        cookie data into a Flash object.
        """
        if not self.has_flash(key):
            return None
        flash = escape.url_unescape(self._get_flash_cookie(key))
        try:
            flash_data = pickle.loads(flash)
            self.clear_cookie(self._cookie_name(key))
            return flash_data
        except:
            return None

    def set_flash(self, flash, key='error'):
        """
        Stores a Flash object as a flash cookie under a given key.
        """
        flash = pickle.dumps(flash)
        self.set_cookie(self._cookie_name(key), escape.url_escape(flash))