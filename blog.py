import webapp2
import os
import jinja2
import logging
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class BlogData(db.Model):
    blogTitle = db.StringProperty(required=True)
    blogDescription = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add = True)

class BlogHandler(Handler):

    def get(self):
        logging.info("Inside get method of BlogHandler")
        self.render("blogform.html")

    def post(self):
        logging.info("Inside Post method of BlogHandler")
        blogTitle = self.request.get("title");
        blogDescription = self.request.get("blogtext");
        errorMap = {}
        if not blogTitle:
            errorMap['blogTitle'] = "Please Provide the Blog Title"
        if not blogDescription:
            errorMap['blogDescription'] = "Please Provide the Blog Decsription"
        if blogTitle and blogDescription:
            blogData = BlogData(blogTitle=blogTitle,blogDescription=blogDescription)
            blogData.put()
            blogId = str(blogData.key().id());
            self.redirect('/blog/'+blogId)
        else:
            logging.info("Error While Submitting the Form %s",errorMap)
            self.render('blogform.html',error=errorMap)



class GetAllBlog(Handler):
    def get(self):
        blogAllData = db.GqlQuery("SELECT * FROM  BlogData ORDER BY created desc")
        logging.info(blogAllData)
        self.render("index.html",blogAllData=blogAllData)

class GetBlogbyId(Handler):
    """docstring for ClassName"""
    def get(self, blogId):
        logging.info("Inside Get method of GetBlogbyId")
        #blogData = db.GqlQuery("SELECT * FROM  BlogData where blogId="+blogId)
        blogData = BlogData.get_by_id(int(blogId))
        blogAllData = []
        blogAllData.append(blogData)
        logging.info(blogAllData)
        self.render("index.html",blogAllData=blogAllData)


app = webapp2.WSGIApplication([
('/blog', GetAllBlog),('/blog/newpost', BlogHandler),(r'/blog/(\d+)',GetBlogbyId)
], debug=True)