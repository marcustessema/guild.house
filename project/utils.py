# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import binascii
import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.utils.text import slugify


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


def tsv_to_dict(dump):
    """ Make a sensible k,v dict from imported tsv.

    No validation is done here, just simple conversion."""
    try:
        rows = [items for items in dump.split("\r\n")]
        header_row = rows[0].split("\t")
        list_row_dicts = []
        for item in rows[1:]:
            row_dict = dict(list(zip(header_row, item.split("\t"))))
            list_row_dicts.append(row_dict)
        return list_row_dicts
    except:
        raise Exception("""Failed to convert dump to dict.

All that is required is a copy and paste from a spreadsheet.""")


def generate_unique_slug(text, queryset, slug_field='slug', iteration=0):

    slug = slugify(text)
    if not slug:
        slug = '-'

    if iteration > 0:
        slug = '{0}-{1}'.format(iteration, slug)
    slug = slug[:50]

    try:
        queryset.get(**{slug_field: slug})
    except ObjectDoesNotExist:
        return slug
    else:
        iteration += 1
        return generate_unique_slug(text, queryset=queryset,
                                    slug_field=slug_field, iteration=iteration)


def generate_unique_hex(length=3, check=None, queryset=None):
    code = binascii.hexlify(os.urandom(length)).decode('UTF-8')
    if check:
        if code != check:
            return code
        else:
            generate_unique_hex(check=code)
    if queryset:
        if not queryset.filter(code=code):
            return code
        else:
            generate_unique_hex(queryset=queryset)
    return code
