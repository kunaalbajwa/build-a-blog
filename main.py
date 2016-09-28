#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

new_post="""

<h1>BUILD A DAMN BLOG!</h1>

<form method ="post" action="/text">
    <label>
        <div>title</div>
        <input type="text" name="title" value="{title}">
        </label>
            <div>text</div>
            <textarea name ="text">{text}</textarea>
        <div class ="error">{error}</div>
         </label>
         <input type="submit">

            </form>

"""
main_page="""
<!page that will show the postings!>
<h1>Hey guys!</h1>
 <form action="/new_post" method="post">
            <input type= "submit" value="New Post Dammit!">

</form>
"""


entry="""
<a href={link}>{title}</a>
<p>{text}</p>
<br>
"""

page_header="""

<!DOCTYPE html>
<html>
<head></head>
<title>Build that Blog</title>

 <body>
"""

page_footer="""

</body>
</html>

"""
#going to need a place to put the permalinks to link to every new post
#have all the posts remain on the main page

class MainHandler(webapp2.RequestHandler):
    def get(self):
        p=Post(title="hey", text="bay")
        p.put()
#^^this is not working
#also I need an error variable
        response=page_header+ main_page
        self.response.write(response)

        blogpost=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5") #OFFSET "+ str(i))
        for q in blogpost:
            response+=entry.format(link=q.key().id(), title=q.title, text=q.text)
        response+=page_footer
#error_title= "you need to write a title"
#error_text="you need to write some text"
        #have a loop that populates all the entries
        #each entry needs to pull from the database
    #main handler for main page

class posts(webapp2.RequestHandler):
    def post(self):
        self.write_form()


    def write_form(self, title="", text="", error=""):
        self.response.write(page_header+ new_post.format(title=title, text=text, error=error)+ page_footer)

class Post(db.Model):
    title= db.StringProperty(required=True)
    text=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)


class submit_post(webapp2.RequestHandler):
    def post(self):
        title=self.request.get("title")
        text=self.request.get("text")
        error=""
        if not title:
            error="Please write a title. "
        if not text:
            error+="Please write text."
        if not error:
            #initialize post here
            p=Post(title=title, text=text)
            p.put()
            #Posts=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        #put info in datatbase, store the title, text and time (to keep the order to organize)
            response=page_header+ main_page
            #this is where the database needs to come in
            link="./"
            blogpost=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5") #OFFSET "+ str(i))
            for q in blogpost:
                response+=entry.format(link=q.key().id(), title=q.title, text=q.text)
            response+=page_footer
            self.response.write(response)
        else:
            self.response.write(page_header+ new_post.format(title=title, text=text, error=error)+ page_footer)

#we need permalinks, redirects, we already knew that.

#def get_posts(limit, offset)
#need to incorporate this one ^^ so we just return 5 of the most recent posts
#has to be written outside of the classes

class ViewPostHandler(webapp2.RequestHandler):
    def get(self,id):
        post=Post.get_by_id(int(id))
        t=jinja_env.get_template("base.html")
        response = t.render(single_post=post.title, page_content=post.text)
        self.response.write(response)

 #navigation links in the base.html

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new_post', posts),
    webapp2.Route('/<id:\d+>', ViewPostHandler),
    ('/text', submit_post)

], debug=True)
