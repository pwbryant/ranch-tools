from .base import *

NOTEBOOK_ARGUMENTS = [
    '--ip',
    '0.0.0.0',
    '--port',
    '8888',
    '--allow-root',
    '--no-browser'
]
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']
