import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from magictea.models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from twilio.rest import Client
account_sid = 'AC9c6d9379cc12a7cf9389e7e839352023'
auth_token = '1c39c107159126f68aa7c73da1381193'

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         settings.EMAIL_MAGIC,
                         [order.email])



    # generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_FILES + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()
    notify = True
    if notify:
        #  send msg to user cell phone (need to find out where that will be stored)
        print("Sending SMS message")
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body="Payment was successful.",
            from_='+19706018455',
            to='+14023506440'
        )
        print(message.date_created)
        print(message.date_sent)
        print(message.status)
        print(message.sid)



def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if request.method == 'POST':
        # mark the order as paid
        order.paid = True
        order.save()
        payment_completed(order.id)
        return redirect('payment:done')

        # if result.is_success:
        #     print("3")
        #     # mark the order as paid
        #     order.paid = True
        #     # store the unique transaction id
        #     order.braintree_id = result.transaction.id
        #     order.save()
        #     payment_completed(order.id)
        #     return redirect('payment:done')
        # else:
        #     print("4")
        #     return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

