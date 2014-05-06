Payment
*******

Django application for an online payment.

For notes:
https://django-dev-and-deploy-using-salt.readthedocs.org/en/latest/app-pay.html
and
https://github.com/pkimber/docs/blob/master/source/paypal.rst

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-pay
  source venv-pay/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

.. note::

  Replace ``your_stripe_publish_key`` and ``your_stripe_secret_key`` with the
  test versions of the *publishable* and *secret* key.

::

  export PAYPAL_RECEIVER_EMAIL="merchant@pkimber.net"
  export STRIPE_PUBLISH_KEY="your_stripe_publish_key"
  export STRIPE_SECRET_KEY="your_stripe_secret_key"

::

  py.test -x && \
      touch temp.db && rm temp.db && \
      django-admin.py syncdb --noinput && \
      django-admin.py migrate --all --noinput && \
      django-admin.py demo_data_login && \
      django-admin.py init_app_pay && \
      django-admin.py demo_data_pay && \
      django-admin.py runserver

Release
=======

https://django-dev-and-deploy-using-salt.readthedocs.org/
