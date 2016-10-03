import tornado.ioloop
import tornado.web
from tornado.web import url
from tornado.web import StaticFileHandler
from peewee import SqliteDatabase
from time import strftime
from flask_peewee.utils import slugify

from models import *


class PeeweeRequestHandler(tornado.web.RequestHandler):
    """Basic request handler to subclass from"""

    def initialize(self, database):
        self.database = database
        self.database.connect()

    def on_finish(self):
        if not self.database.is_closed:
            self.database.close()


class MainHandler(PeeweeRequestHandler):

    def get(self):
        self.render("index.html")


class PostIndexHandler(PeeweeRequestHandler):
    """Show an index poage with blog posts"""

    def get(self):
        try:
            posts = Post.select()
            # TODO: paginate
        except Post.DoesNotExist:
            posts = None
        self.render("post_index.html", posts=posts)


class PostHandler(PeeweeRequestHandler):
    """Handler for serving single posts"""

    def get(self, *args, **kwargs):
        if type(args[0]) is not int:
            slug = args[0].strip('/')
            post = Post.select().where(Post.slug == slug).get()
        else:
            post_id = int(args[0])
            posts = Post.select().where(Post.id == post_id).get()
        if post:
            self.render("post_detail.html", post=post)
        else:
            self.set_status(404, 'Post not found.')

    def post(self, *args, **kwargs):
        # TODO: insert post into DB
        pass


class CreateHandler(PeeweeRequestHandler):
    """Handler for creating posts"""

    def get(self):
        self.render("post_create.html")

    def post(self):
        # TODO: authentication
        id = self.get_argument("id", None)
        author_id = 1 # TODO: get author id from authentication
        title = self.get_argument("inputTitle", None)
        text = self.get_argument("inputText", None)
        date_created = datetime.datetime.now()

        if id is None:
            # create post
            try:
                post = Post.create(author_id=author_id, title=title, text=text, date_created=date_created,
                                   slug=slugify(title))
                post.save()
                # TODO: set flash message
                self.redirect("/")
            except Exception as e:
                print(e)
                self.write("Something went wrong!")
        else:
            # update
            pass

settings = {
    'static_path': 'static',
    'template_path': './templates/'
}

app = tornado.web.Application([
    url(r"/", MainHandler, dict(database=db)),
    url(r"/posts", PostIndexHandler, dict(database=db), name="post_index"),
    url(r"/post/create", CreateHandler, dict(database=db), name="post_create"),
    # url(r"/post/([0-9]+)", PostHandler, dict(database=db), name="post_view"),
    url(r"/post/(.*)", PostHandler, dict(database=db), name="post_view"),
    url(r"/(.*)", StaticFileHandler, {"path": "./static"})
],
    **settings)


if __name__ == "__main__":
    port = 8888
    app.listen(port)
    print("Listening on port %s" % port)
    tornado.ioloop.IOLoop.current().start()