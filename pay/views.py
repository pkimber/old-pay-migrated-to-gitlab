# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging
import stripe

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

#from paypal.standard.forms import PayPalPaymentsForm

from .forms import StripeForm
from .models import Payment


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
            charge = stripe.Charge.create(
                amount=self.object.total_as_pennies(), # amount in pennies, again
                currency=CURRENCY,
                card=token,
                description=self.object.email,
            )
            self.object.set_paid()
            result = super(StripeFormViewMixin, self).form_valid(form)
        except stripe.CardError as e:
            self.object.set_payment_failed()
            # The card has been declined
            logger.error(
                'CardError\n'
                'payment: {}\n'
                'param: {}\n'
                'code: {}\n'
                'http body: {}\n'
                'http status: {}'.format(
                    self.object.pk,
                    e.param,
                    e.code,
                    e.http_body,
                    e.http_status,
                )
            )
            result = HttpResponseRedirect(self.object.url_failure)
        except stripe.StripeError as e:
            self.object.set_payment_failed()
            logger.error(
                'StripeError\n'
                'payment: {}\n'
                'http body: {}\n'
                'http status: {}'.format(
                    self.object.pk,
                    e.http_body,
                    e.http_status,
                )
            )
            result = HttpResponseRedirect(self.object.url_failure)
        return result
