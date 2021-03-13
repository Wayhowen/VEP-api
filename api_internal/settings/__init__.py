import importlib
import os

module = importlib.import_module(os.environ.get('SETTINGS_MODULE'))

if '__all__' in module.__dict__:
    names = module.__dict__['__all__']
else:
    names = [x for x in module.__dict__ if not x.startswith('_')]

globals().update({name: getattr(module, name) for name in names})

from tasks.celeryapp import app as celery_app
__all__ = ['celery_app']