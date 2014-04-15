# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import stripe

from django.conf import settings

#from paypal.standard.forms import PayPalPaymentsForm

from .forms import StripeForm
from .models import Payment


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


class StripeFormMixin(object):

    form_class = StripeForm
    model = Payment

    def get_context_data(self, **kwargs):
        context = super(StripeFormMixin, self).get_context_data(**kwargs)
        context.update(dict(
            currency='GBP',
            description=self.object.description,
            email=self.object.email,
            key=settings.STRIPE_PUBLISH_KEY,
            name=settings.STRIPE_CAPTION,
            total=self.object.total_as_pennies(),
        ))
        return context

    def form_valid(self, form):
        # Create the charge on Stripe's servers - this will charge the user's card
        token = form.cleaned_data['stripeToken']
        # Set your secret key: remember to change this to your live secret key
        # in production.  See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount=1000, # amount in cents, again
                currency="GBP",
                card=token,
                description="payinguser@example.com"
            )
        except stripe.CardError as e:
            # The card has been declined
            pass
        return super(StripeFormMixin, self).form_valid(form)
