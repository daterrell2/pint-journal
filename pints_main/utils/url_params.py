import re

def get_param(request, param, options, default=None):
    v = request.GET.get(param)

    if v in options:
        return v

    return default


