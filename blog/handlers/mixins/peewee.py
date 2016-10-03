import tornado.web


class PeeweeMixin(tornado.web.RequestHandler):
    """Add peewee DB setup to a request handler"""

    def initialize(self, database):
        self.database = database
        self.database.connect()

    def on_finish(self):
        if not self.database.is_closed:
            self.database.close()