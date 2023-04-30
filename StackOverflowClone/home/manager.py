# Multi-db support based on http://www.eflorenzano.com/blog/post/easy-multi-database-support-django/
# TODO: is there a way to use the traceback module based on an exception variable?

import logging
import sys
import traceback as traceback_mod
import warnings

from django.utils.encoding import smart_text

from home.models import ErrorBase


def create_from_exception(self, url=None, exception=None, traceback=None, **kwargs):
    if not exception:
        exc_type, exc_value, traceback = sys.exc_info()
    elif not traceback:
        warnings.warn(
            "Using just the ``exception`` argument is deprecated, send ``traceback`` in addition.",
            DeprecationWarning,
        )
        exc_type, exc_value, traceback = sys.exc_info()
    else:
        exc_type = exception.__class__
        exc_value = exception

    def to_unicode(f):
        if isinstance(f, dict):
            nf = dict()
            for k, v in f.items():
                nf[str(k)] = to_unicode(v)
            f = nf
        elif isinstance(f, (list, tuple)):
            f = [to_unicode(f) for f in f]
        else:
            try:
                f = smart_text(f)
            except (UnicodeEncodeError, UnicodeDecodeError):
                f = "(Error decoding value)"
        return f

    tb_message = "\n".join(
        traceback_mod.format_exception(exc_type, exc_value, traceback)
    )

    kwargs.setdefault("message", to_unicode(exc_value))
    level = logging.ERROR
    if kwargs.get("level"):
        level = kwargs["level"]

    ErrorBase.objects.create(
        class_name=exc_type.__name__,
        message=to_unicode(exc_value),
        traceback=tb_message,
        level=level,
    )


def create_from_text(message, class_name=None, level=40, traceback=None):
    ErrorBase.objects.create(
        class_name=class_name, message=message, traceback=traceback, level=level
    )
