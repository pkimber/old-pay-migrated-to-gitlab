# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging
import stripe

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

#from paypal.standard.forms import PayPalPaymentsForm

from .forms import StripeForm
from .models import (
    Payment,
    StripeCustomer,
)


CURRENCY = 'GBP'
PAYMENT_PK = 'payment_pk'

logger = logging.getLogger(__name__)

#class PayPalFormView(LoginRequiredMixin, BaseMixin, FormView):
#
#    form_class = PayPalPaymentsForm
#    template_name = 'pay/paypal.html'
#
#    def get_initial(self):
#        return dict(
#            business=settings.PAYPAL_RECEIVER_EMAIL,
#            amount='10.01',
#            currency_code='GBP',
#            item_name='Cycle Routes around Hatherleigh',
#            invoice='0001',
#            notify_url="https://www.example.com" + reverse('paypal-ipn'),
#            return_url="https://www.example.com/your-return-location/",
#            cancel_return="https://www.example.com/your-cancel-location/",
#        )


class StripeFormViewMixin(object):

    form_class = StripeForm
    model = Payment

    def _check_perm(self):
        payment_pk = self.request.session.get(PAYMENT_PK, None)
        if payment_pk:
            if not payment_pk == self.object.pk:
                logger.critical(
                    'payment check: invalid {} != {}'.format(
                        payment_pk, self.object.pk,
                ))
                raise PermissionDenied('Valid payment check fail.')
        else:
            logger.critical('payment check: invalid')
            raise PermissionDenied('Valid payment check failed.')

    def _init_stripe_customer(self, email, token):
        """Make sure a stripe customer is created and update card (token)."""
        result = None
        try:
            c = StripeCustomer.objects.get(email=email)
            self._stripe_customer_update(c.customer_id, token)
            result = c.customer_id
        except StripeCustomer.DoesNotExist:
            customer = self._stripe_customer_create(email, token)
            c = StripeCustomer(**dict(
                email=email,
                customer_id=customer.id,
            ))
            c.save()
            result = c.customer_id
        return result

    def _log_card_error(self, payment_pk):
        logger.error(
            'CardError\n'
            'payment: {}\n'
            'param: {}\n'
            'code: {}\n'
            'http body: {}\n'
            'http status: {}'.format(
                payment_pk,
                e.param,
                e.code,
                e.http_body,
                e.http_status,
            )
        )

    def _log_stripe_error(self, e, message):
        logger.error(
            'StripeError\n'
            '{}\n'
            'http body: {}\n'
            'http status: {}'.format(
                message,
                e.http_body,
                e.http_status,
            )
        )

    def _stripe_customer_create(self, email, token):
        """Use the Stripe API to create/update a customer."""
        try:
            return stripe.Customer.create(
                card=token,
                email=email,
            )
        except stripe.StripeError as e:
            self._log_stripe_error(e, 'create - email: {}'.format(email))

    def _stripe_customer_update(self, customer_id, token):
        """Use the Stripe API to create/update a customer."""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            customer.card = token
            customer.save()
        except stripe.StripeError as e:
            self._log_stripe_error(e, 'update - id: {}'.format(customer_id))

    def get_context_data(self, **kwargs):
        context = super(StripeFormViewMixin, self).get_context_data(**kwargs)
        self._check_perm()
        self.object.check_can_pay()
        context.update(dict(
            currency=CURRENCY,
            description=self.object.description,
            email=self.object.email,
            key=settings.STRIPE_PUBLISH_KEY,
            name=settings.STRIPE_CAPTION,
            total=self.object.total_as_pennies(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Create the charge on Stripe's servers - this will charge the user's card
        token = form.cleaned_data['stripeToken']
        self.object.save_token(token)
        # Set your secret key: remember to change this to your live secret key
        # in production.  See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            customer_id = self._init_stripe_customer(self.object.email, token)
            charge = stripe.Charge.create(
                amount=self.object.total_as_pennies(), # amount in pennies, again
                currency=CURRENCY,
                customer=customer_id,
                description=self.object.description,
            )
            self.object.set_paid()
            result = super(StripeFormViewMixin, self).form_valid(form)
        except stripe.CardError as e:
            self.object.set_payment_failed()
            self._log_card_error(e, self.object.pk)
            result = HttpResponseRedirect(self.object.url_failure)
        except stripe.StripeError as e:
            self.object.set_payment_failed()
            self._log_stripe_error(e, 'payment: {}'.format(self.object.pk))
            result = HttpResponseRedirect(self.object.url_failure)
        return result
