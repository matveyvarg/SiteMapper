from os import getenv
configuration = {
    'HOST': getenv('HOST', ''),
    'PORT': getenv('PORT', ''),
    'debug': False
}