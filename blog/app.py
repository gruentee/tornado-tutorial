import tornado.web
from flask_peewee.utils import slugify
from tornado.web import StaticFileHandler
from tornado.web import url

from blog.handlers.mixins.peewee import PeeweeMixin
from blog.handlers.mixins.message import FlashMixin
from models import *
from blog.util.flash_message import Flash


class MainHandler(PeeweeMixin):

    def get(self):
        self.redirect("/posts")


class PostIndexHandler(PeeweeMixin, FlashMixin):
    """Show an index poage with blog posts"""

    def get(self):
        message = None
        try:
            posts = Post.select()
            # TODO: paginate
        except Post.DoesNotExist:
            posts = None
        self.render("post_index.html", posts=posts)


class PostHandler(PeeweeMixin):
    """Handler for serving single posts"""

    def get(self, *args, **kwargs):
        if type(args[0]) is not int:
            slug = args[0].strip('/')
            post = Post.select().where(Post.slug == slug).get()
        else:
            post_id = int(args[0])
            post = Post.select().where(Post.id == post_id).get()
        if post:
            self.render("post_detail.html", post=post)
        else:
            self.set_status(404, 'Post not found.')


class CreateHandler(PeeweeMixin, FlashMixin):
    """Handler for creating and editing posts"""

    def get(self, post_id):
        # post_id = self.get_argument("id", None)
        # TODO: param validation
        post = Post.select().where(Post.id == post_id).get()
        if self.has_flash('success'):
            flash = self.get_flash('success')
            self.render("post_create.html", post=post, message=flash.message, message_type='success')
        else:
            self.render("post_create.html", post=post)

    def post(self):
        # TODO: authentication
        # TODO: authorization
        post_id = self.get_argument("postId", None)
        author_id = 1 # TODO: get author id from authentication
        title = self.get_argument("inputTitle", None)
        text = self.get_argument("inputText", None)
        date_created = datetime.datetime.now()
        # TODO: validation
        try:
            # create
            post = Post(author_id=author_id, title=title, text=text, date_created=date_created,
                        slug=slugify(title))
            # update
            if post_id is not None:
                post = Post(id=post_id, author_id=author_id, title=title, text=text, date_created=date_created,
                            slug=slugify(title))
            post.save()
            flash = Flash("Post erfolgreich gespeichert!")
            self.set_flash(flash, 'success')
            self.redirect(self.reverse_url('post_edit', post_id))
        except Exception as e:
            self.write("Something went wrong!")
            print(e)


settings = {
    'static_path': 'static',
    'template_path': './templates/'
}

app = tornado.web.Application([
    url(r"/", MainHandler, dict(database=db), 'home'),
    url(r"/posts", PostIndexHandler, dict(database=db), name="post_index"),
    url(r"/post/create", CreateHandler, dict(database=db), name="post_create"),
    url(r"/post/([0-9]+)/edit", CreateHandler, dict(database=db), name="post_edit"),
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