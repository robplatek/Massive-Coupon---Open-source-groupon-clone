#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def iso_flag(iso, flag_path=u''):
	"""
	Returns a full path to the ISO 3166-1 alpha-2 country code flag image.
	
	Example usage::
		
		{{ user_profile.country.iso|iso_flag }}
		
		{{ user_profile.country.iso|iso_flag:"appmedia/flags/%s.png" }}
	
	"""
	from countries.utils.isoflag import iso_flag
	return iso_flag(iso, flag_path)
iso_flag = stringfilter(iso_flag)

# Syntax: register.filter(name of filter, callback)
register.filter('iso_flag', iso_flag)
