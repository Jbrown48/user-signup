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
#
import webapp2
import cgi
import re

html_form ='''
<body>
    <h1>Signup</h1>
    <form method="post">
    <table>
        <tr>
            <td class='label'>
            Username
            </td>
            <td>
                <input type='text' name='username' value='%(username)s'/>
            </td>
            <td class='error'>
            %(username_error)s
            </td>
        </tr>

        <tr>
            <td class='label'>
            Password
            </td>
            <td>
                <input type='text' name='password' value=''/>
            </td>
            <td class='error'>
            %(password_error)s
            </td>
        </tr>

        <tr>
            <td class='label'>
            Verify Password
            </td>
            <td>
                <input type='text' name='verify' value=''/>
            </td>
            <td class='error'>
            %(verify_error)s
            </td>
        </tr>

        <tr>
            <td class='label'>
            Email (optional)
            </td>
            <td>
                <input type='text' name='email' value='%(email)s'/>
            </td>
            <td class='error'>
            %(email_error)s
            </td>
        </tr>
    </table>

        <button>Submit</button>
    </form>
</body>
'''


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error="", password_error="", verify_error="", username="", email="",email_error=""):
        self.response.write(html_form % {"username_error": username_error,
                                        "password_error": password_error,
                                        "verify_error": verify_error,
                                         "username": username,
                                         "email": email,
                                         "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        username_error = ""
        verify_error = ""
        email_error = ""
        password_error=""
        error = False

        if not valid_username(username):
            username_error = "Please enter a valid username."
            error = True

        if not valid_password(password):
            password_error = "Please enter a valid password."
            error = True

        if not verify == password:
            verify_error = "Passwords do not match."
            error = True

        if not valid_email(email):
            email_error = "Invalid Email"
            error = True

        if error == True:
            self.write_form(username_error, password_error, verify_error, username, email, email_error)

        else:
            self.redirect('/Welcome?username={}'.format(username))

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("<strong>Welcome, " + username + "!</strong>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', WelcomeHandler)
], debug=True)
