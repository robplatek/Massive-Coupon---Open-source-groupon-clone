# Django settings for massivecoupon project.
import socket, os

DEBUG = False
TEMPLATE_DEBUG = DEBUG



# Site-based configuration parameters
_host = socket.gethostname().lower()
_basedir = os.path.dirname(__file__)

# Site-based configuration variables: basic
DB_SUFFIX = ''
PATH_ADMINMEDIA = os.path.join(_basedir, 'adminmedia')
PATH_ADMINMEDIA = '/django/contrib/admin/media'

PATH_MEDIA = os.path.join(_basedir, 'media')

# Site-based configuration variables: per-site


ADMINS = (
  ('you', 'you@email.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'       # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''          # Or path to database file if using sqlite3.
DATABASE_USER = ''                    # Not used with sqlite3.
DATABASE_PASSWORD = ''                  # Not used with sqlite3.
DATABASE_HOST = 'localhost'                   # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                            # Set to empty string for default. Not used with sqlite3.

SESSION_COOKIE_DOMAIN = '.massivecoupon.com'

GOOGLE_MAPS_API_KEY = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/massivecoupon/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

PHOTOLOGUE_DIR = 'deals'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

FACEBOOK_API_KEY = ''
FACEBOOK_SECRET_KEY = ''
SOCIAL_GENERATE_USERNAME = True


PAYPAL_USER  = ""
PAYPAL_PASSWORD = ""
PAYPAL_SIGNATURE = ""
PAYPAL_DEBUG = True


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'socialregistration.middleware.FacebookMiddleware'
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # this is the default backend, don't forget to include it!
    'massivecoupon.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    # this is what you're adding for using Twitter
#    'socialregistration.auth.TwitterAuth',
    'socialregistration.auth.FacebookAuth', # Facebook
#    'socialregistration.auth.OpenIDAuth', # OpenID
)

ROOT_URLCONF = 'massivecoupon.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/www/massivecoupon/socialregistration/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'massivecoupon',
    'massivecoupon.engine',
    'massivecoupon.countries',
    'massivecoupon.photologue',
    'massivecoupon.tagging',
    'massivecoupon.socialregistration', 
    'massivecoupon.paypalxpress',
#    'debug_toolbar',    
)

LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/"

