#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def iso_flag(iso, flag_path=u''):
	"""
	Returns a full path to the ISO 3166-1 alpha-2 country code flag image.
	
	``flag_path`` is given in the form
	``'<path relative to media root>/%s.gif'``
	and is appended to ``settings.MEDIA_URL`` 
	
	if a valid flag_path is not given trys to use 
	``settings.COUNTRIES_FLAG_PATH``
	defaults to ``'flags/%s.gif'``
	
	"""
	if not settings.MEDIA_URL:
		return u''
	deafult = u'-'
	if not iso:
		iso = deafult
	else:
		iso = iso.lower().strip()
	try:
		flag_name = flag_path % iso
	except (ValueError, TypeError):
		flag_path = getattr(settings, 'COUNTRIES_FLAG_PATH', u'flags/%s.gif')
		try:
			flag_name = flag_path % iso
		except (ValueError, TypeError):
			return u''
	return u''.join((settings.MEDIA_URL, flag_name))