import re
from django.utils.html import strip_spaces_between_tags
from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta

RE_MULTISPACE = re.compile(r'\s{2,}')
RE_SPACETAG1 = re.compile(r'>\s')
RE_SPACETAG2 = re.compile(r'\s<')
RE_NEWLINE = re.compile(r'\n')


class MinifyHTMLMiddleware(object):
    """
    Class that mininize the HTML code in the templates
    """

    def process_response(self, request, response):
        """
        Method that minimize the HTML code first the spaces between tags are
        stripped, then the newlines are converted to singles spaces, and
        finally the multispaces are converted to a single space

        Arguments:
        - `request`:
        - `response`: content of the pages that are minized if the type of
                      content in the response is text/html
        """

        if settings.DEBUG:
            return response

        if 'text/html' in response['Content-Type'] and settings.COMPRESS_HTML:
            response.content = strip_spaces_between_tags(
                response.content.strip())
            response.content = RE_NEWLINE.sub(" ", response.content)
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_SPACETAG1.sub(">", response.content)
            response.content = RE_SPACETAG2.sub("<", response.content)
        return response


class AutoLogoutMiddleware(object):
    """
    Class to Auto Logout an user after some minutes, the amount of minutes
    when a user is auto logout is stored in the variable AUTO_LOGOUT_DELAY
    in settings.py
    """

    def process_request(self, request):
        """
        Check the time elapsed since last action of the user
        """
        if not request.user.is_authenticated():
            # Can't log out if not logged in
            return

        try:
            time_elapsed = datetime.now() - request.session['last_touch']
            time_in_seconds = timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0)
            if (time_elapsed > time_in_seconds):
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()
