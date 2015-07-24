import re

def get_param(request, param, options, default=None):
	'''
	Finds value of param in Django request.GET.
	If value is in list options, returns value.
	If param is signed and value is in options, returns sign, value
	Otherwise returns default.
	'''
	v = request.GET.get(param)

	if v in options:
		return v

	return default


