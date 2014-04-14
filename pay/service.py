# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from pay.models import Product
from pay.tests.model_maker import make_product


def init_product(slug, title, description, price):
    """Create a new product - if it doesn't exist."""
    slug = slugify(slug)
    try:
        result = Product.objects.get(slug=slug)
        # If the product exists - don't update it!!!
        # The user might have set a new price or description!!
    except Product.DoesNotExist:
        if not description:
            description = ''
        result = make_product(slug, title, price, description=description)
        print('make_product("{}")'.format(title))
    return result
