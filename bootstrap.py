'''
Tornadoweb bootstrapper.
'''

import sys
sys.dont_write_bytecode = True
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.dirname(__file__))
USER = os.getlogin()

REQ = os.path.join(ROOT, 'requires')
REQ_INIT = os.path.join(REQ, '__init__.py')

UTILS = os.path.join(ROOT, 'utils')
UTILS_INIT = os.path.join(UTILS, '__init__.py')
UTILS_SERV = os.path.join(UTILS, 'server.py')
UTILS_DECOR = os.path.join(UTILS, 'decorators.py')

SETTINGS = os.path.join(REQ, 'settings.py')

CORE = os.path.join(ROOT, 'core')
CORE_INIT = os.path.join(CORE, '__init__.py')
CORE_URLS = os.path.join(CORE, 'urls.py')
CORE_HANDLERS = os.path.join(CORE, 'handlers.py')

README = os.path.join(ROOT, 'readme.md')

HAS_REQ = 'requires' in os.listdir(ROOT)
HAS_CORE = 'core' in os.listdir(ROOT)
HAS_UTILS = 'utils' in os.listdir(ROOT)

HAS_APP = lambda app: app in os.listdir(ROOT)
APP_INIT = lambda app: os.path.join(os.path.join(ROOT, app), '__init__.py')
APP_HANDLER = lambda app: os.path.join(os.path.join(ROOT, app), 'handlers.py')
APP_URLS = lambda app: os.path.join(os.path.join(ROOT, app), 'urls.py')


try:
    HAS_SETTINGS = 'settings.py' in os.listdir(REQ)
except OSError:
    HAS_SETTINGS = False


def gen_docstring(open_string=False):
    '''
    Generate docstring.
    '''

    doc = '''"""
Created on {0}

@author: {1}

'''.format(datetime.now().strftime('%B %d %Y'), USER)

    if not open_string:
        doc += '"""'

    return doc


def gen_base_imports():
    '''
    Generate basic imports.
    '''

    doc = '''
import sys
sys.dont_write_bytecode = True

from tornado.web import Application, os, StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

'''
    return doc


def gen_settings():
    '''
    Generate settings.
    '''

    doc = '''
GEN_PATH = lambda path: os.path.join(os.getcwd(), path)

SETTINGS = {
    'APPS': ['core'],  # Add your apps to this list
    'cookie': '',  # Specify the cookie variable name
    'login_url': '',  # Login path for the application
    'template_path': '',  # Absolute template path for the application.
    'static_path': '',  # Absolute static file path for the application.
    'debug': True  # Retain debug True for development.
}

URLS = [('/src/(.*?)$', StaticFileHandler,
         {'path': SETTINGS['static_path']})]

'''

    return doc


def gen_app_loader():
    '''
    Generate app loader.
    '''

    doc = '''
if SETTINGS['APPS']:
    for app in SETTINGS['APPS']:
        sys.path.append(os.path.join(os.getcwd(), app))
        _urls = __import__(app)
        URLS.extend(_urls.URLS)

'''

    return doc


def gen_app():
    '''
    Generate application object invocation.
    '''

    doc = '''
APP = Application(URLS, **SETTINGS)
SERVER = HTTPServer(APP)
LOOP = IOLoop.instance()
PORT = 8888


if __name__ == '__main__':
    pass
'''

    return doc


def gen_settings_str():
    '''
    Generate settings module for application.
    '''

    settings_str = ''
    settings_str += gen_docstring()
    settings_str += '''
# pylint: disable=W0142
'''
    settings_str += gen_base_imports()
    settings_str += gen_settings()
    settings_str += gen_app_loader()
    settings_str += gen_app()

    return settings_str


def gen_req_package():
    '''
    Generate package structure for requires.
    '''

    doc = '''
"""
Requires for app
"""
import sys
sys.dont_write_bytecode = True
import requires.settings
from requires.settings import SERVER, LOOP, PORT

__all__ = ['SERVER', 'LOOP', 'PORT']

if __name__ == '__main__':
    pass
'''

    return doc


def gen_core_app():
    '''
    Generate package structure for core app.
    '''

    doc = '''
"""
Core app.
"""
import sys
sys.dont_write_bytecode = True
import core.urls
from core.urls import URLS

__all__ = ['URLS']

if __name__ == '__main__':
    pass
'''

    return doc


def gen_user_app(user_app_name):
    '''
    Generate package structure for user app.
    '''

    doc = '''
"""
%s app.
"""
import sys
sys.dont_write_bytecode = True
import core.urls
from core.urls import URLS

__all__ = ['URLS']

if __name__ == '__main__':
    pass
''' % (user_app_name)

    return doc


def gen_utils_init():
    '''
    Generate package structure for requires.
    '''

    doc = '''
"""
Utils package
"""
import sys
sys.dont_write_bytecode = True
from utils.server import Handler

__all__ = ['Handler']

if __name__ == '__main__':
    pass
'''

    return doc


def gen_utils_server():
    '''
    Generate package structure for utils.
    '''

    doc = '''
# pylint: disable=R0904
"""
Utils.
"""
import sys
sys.dont_write_bytecode = True
from tornado.web import RequestHandler


class Handler(RequestHandler):
    """
    Base request handler overridden with required decorators and data
    members.
    """

    # Add required handler members.
    def __init__(self, *args, **kwargs):
        """
        Handler init.
        """
        super(Handler, self).__init__(*args, **kwargs)

    # Add decorators here
    def get(self, *args, **kwargs):
        """
        HTTP GET Request handler method.
        """
        pass

    # Add decorators here
    def post(self, *args, **kwargs):
        """
        HTTP POST Request handler method.
        """
        pass


__all__ = ['Handler']


if __name__ == '__main__':
    pass
'''

    return doc


def gen_utils_decorators():
    '''
    Generate decorator module structure for utils.
    '''

    doc = '''
# pylint: disable=R0904
"""
Utils.
"""
import sys
sys.dont_write_bytecode = True
from functools import wraps


def is_authenticated(method):
    """
    Basic authenticated check decorator.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper method for is_authenticated decorator.
        """

        #  Add decorator flow.

        return method(self, *args, **kwargs)

    return wrapper


__all__ = ['is_authenticated']


if __name__ == '__main__':
    pass
'''

    return doc


def gen_core_urls():
    '''
    Generate urlmap for core app.
    '''

    doc = gen_docstring(open_string=True)

    doc += '''URL map for core app.
"""

from core.handlers import Main
'''

    doc += '''
URLS = [('/$', Main)]

__all__ = ['URLS']


if __name__ == '__main__':
    pass
'''

    return doc


def gen_app_urls(user_app_name):
    '''
    Generate urlmap for core app.
    '''

    doc = gen_docstring(open_string=True)

    doc += '''URL map for %s app.
"""

from core.handlers import Main
''' % (user_app_name)

    doc += '''
URLS = [()]  # Fill up app specific urlmap

__all__ = ['URLS']


if __name__ == '__main__':
    pass
'''

    return doc


def gen_core_handlers():
    '''
    Generate base handler for core app.
    '''

    doc = '''
# pylint: disable=R0904

"""
Core handlers
"""
import sys
sys.dont_write_bytecode = True
from utils.server import Handler
# from tornado.template import Loader  # Template loader


class Main(Handler):
    """
    Main request handler for core app.
    """

    def __init__(self, *args, **kwargs):
        """
        Main request handler init.
        """
        super(Main, self).__init__(*args, **kwargs)
        self.template_file = 'index.html'

    def get(self, *args, **kwargs):
        """
        HTTP GET Request handler method for Main handler.
        """

        # Template loader and generator flow. Setup a template path
        # in settings, template file in init and load the template as
        # below.

        # template = Loader(self.settings['template_path'])
        # template = template.load(self.template_file)
        # self.write(template.generate())

        super(Main, self).get(*args, **kwargs)
        self.write("Bootstrapped for TornadoWeb")

    def post(self, *args, **kwargs):
        """
        HTTP POST Request handler method for Main handler.
        """
        pass


__all__ = ['Main']


if __name__ == '__main__':
    pass
'''

    return doc


def gen_app_handlers(user_app_name):
    '''
    Generate base handler for user app.
    '''

    doc = '''
# pylint: disable=R0904

"""
%s app handlers
"""
import sys
sys.dont_write_bytecode = True
from utils.server import Handler
from tornado.template import Loader


class Main(Handler):
    """
    Main request handler for %s app.
    """

__all__ = []


if __name__ == '__main__':
    pass
''' % (user_app_name)

    return doc


def gen_readme():
    '''
    Generate a readme file for Bootstrapped setup.
    '''

    doc = '''
=== README for Tornastrap ===

Applications are self contained as packages and are added to the
 SETTINGS which would take care of adding apps to the path at runtime.

'''

    return doc


def gen_main():
    '''
    Generate main.py for app.
    '''

    doc = gen_docstring()

    doc += '''
import sys
sys.dont_write_bytecode = True

from requires import LOOP, SERVER, PORT
from socket import error as SockErr


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            try:
                S_PORT = int(sys.argv[1])
            except TypeError:
                S_PORT = PORT
                print "Non numeric port. Starting on {0}".format(PORT)
        else:
            S_PORT = PORT
        SERVER.bind(S_PORT)
        SERVER.start()
        print "Started on http://0.0.0.0:{0}".format(S_PORT)
        LOOP.start()
    except KeyboardInterrupt:
        pass
    except SockErr:
        sys.exit("Another program using the port. Please try again")
'''

    return doc


if __name__ == '__main__':

    app_name = None

    if '--app' in sys.argv and len(sys.argv) >= 3 and sys.argv[1] == '--app':
        app_name = sys.argv[2]

    # App structure generation
    if app_name:
        if not 'main.py' in os.listdir(ROOT):
            sys.exit('App generation works only inside bootstrapped env.')
        else:
            if not HAS_APP(app_name):
                os.mkdir(app_name)
            print "Generating application ~ %s..." % app_name
            with open(APP_INIT(app_name), 'w') as aifile:
                aifile.write(gen_user_app(app_name))
            print "Generting url map for app ~ %s..." % app_name
            with open(APP_URLS(app_name), 'w') as aufile:
                aufile.write(gen_app_urls(app_name))
            print "Generating handlers for app ~ %s..." % app_name
            with open(APP_HANDLER(app_name), 'w') as ahfile:
                ahfile.write(gen_app_handlers(app_name))
            print "Completed generating app ~ %s" % app_name

    # Bootstrap stack generation flow
    elif '--stack' in sys.argv and len(
            sys.argv) >= 2 and sys.argv[1] == '--stack':
        if not HAS_REQ:
            os.mkdir('requires')
        else:
            pass

        if not HAS_CORE:
            os.mkdir('core')
        else:
            pass

        if not HAS_UTILS:
            os.mkdir('utils')
        else:
            pass

        print "Generating requirements package..."
        with open(REQ_INIT, 'w') as rifile:
            rifile.write(gen_req_package())
        print "Generating settings module..."
        with open(SETTINGS, 'w') as sfile:
            sfile.write(gen_settings_str())
        print "Completed generating requirements package"

        print "Generating utils package..."
        with open(UTILS_INIT, 'w') as uifile:
            uifile.write(gen_utils_init())
        print "Generating server module..."
        with open(UTILS_SERV, 'w') as usfile:
            usfile.write(gen_utils_server())
        print "Generating decorators module..."
        with open(UTILS_DECOR, 'w') as udfile:
            udfile.write(gen_utils_decorators())
        print "Completed generating utils package"

        print "Generating core app package..."
        with open(CORE_INIT, 'w') as cifile:
            cifile.write(gen_core_app())
        print "Generting url map for core package..."
        with open(CORE_URLS, 'w') as cufile:
            cufile.write(gen_core_urls())
        print "Generating handlers for core app..."
        with open(CORE_HANDLERS, 'w') as chfile:
            chfile.write(gen_core_handlers())
        print "Completed generating core app package"

        print "Generating main.py for bootstrap..."
        with open('main.py', 'w') as mfile:
            mfile.write(gen_main())

        print "Generating readme markdown..."
        with open(README, 'w') as rfile:
            rfile.write(gen_readme())
        print "Completed bootstrapping. Start the server with main.py"
    else:
        sys.exit('Invalid parameters')
