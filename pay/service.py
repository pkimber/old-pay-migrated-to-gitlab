# -*- encoding: utf-8 -*-
from django.conf import settings

from mail.models import MailTemplate


# slug for the email template
PAYMENT_CARD_REFRESH = 'payment_card_refresh'
PAYMENT_LATER = 'payment_later'
PAYMENT_THANKYOU = 'payment_thankyou'


def process_payment_plan():
    """Check payment plans to see if any payments are due.

    - Don't send an email if the course has ended
    - Ignore courses started before 1st September 2014
    - Use the 'ContactTemplate' table to make sure an email is sent once only
      to a contact.
    - Use the 'CourseTemplate' table to make sure an email is sent once only
      per course.

    TODO We can't take the payment from within a transaction, so perhaps we
    need a lock flag e.g. pending, requested payment, payment received.  We
    check for pending payments, if it is due, then mark the line as requested.
    When the payment is due, then mark the payment as received.  If a payment
    is requested, but not received, the record will be *locked* and will need
    to be released somehow.  The record will probably require manual resolution
    by a person.

    """
    count = 0
    start_date = date(2014, 8, 31)
    courses = MemberCourse.objects.courses().filter(enrol_date__gt=start_date)
    for c in courses:
        # don't send an email if the course has ended.
        if not c.has_ended:
            # send the email (if it hasn't been sent already)
            count = count + _send(c)
    if count:
        process_mail.delay()
    return count


def init_app_pay():
    """For the description, check 'mail_template_context' in 'pay.models'."""
    MailTemplate.objects.init_mail_template(
        PAYMENT_LATER,
        'Thank you for your application',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ description }} transaction detail.\n"
            "{{ total }} total value of the transaction."
        ),
        False,
        settings.MAIL_TEMPLATE_TYPE,
        subject='Thank you for your application',
        description="We will contact you to arrange payment.",
    )
    MailTemplate.objects.init_mail_template(
        PAYMENT_THANKYOU,
        'Thank you for your payment',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ description }} transaction detail.\n"
            "{{ total }} total value of the transaction."
        ),
        False,
        settings.MAIL_TEMPLATE_TYPE,
        subject='Thank you for your payment',
        description="We will send you the course materials.",
    )
