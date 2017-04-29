from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.
from notifications.signals import notify
from .forms import SendMsgForm
from channels import Group
from channels.sessions import channel_session
import json
from urllib.parse import parse_qs


def NotificationView(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = SendMsgForm(request.POST)
            if form.is_valid():
                recipient = form.cleaned_data['recipient']
                message = form.cleaned_data['message']
                recipient_user = User.objects.filter(username=recipient)[0]
                notify.send(request.user, recipient=recipient_user, verb=message)
                recipient_str = str(recipient)
                Group(recipient_str).send({
                    'text': json.dumps({
                        'actor': str(request.user),
                        'message': message
                    })
                })
                Group('group_b').send({
                    'text': json.dumps({
                        'actor': str(request.user),
                        'message': message + ' in the Group B'
                    })})
                return HttpResponseRedirect('/notification/')
        else:
            form = SendMsgForm()

        queryset = request.user.notifications.unread()

        template_value = {
            'form': form,
            'notifications': queryset
        }

        return render(request, 'notification/index.html', template_value)

    else:
        form = SendMsgForm()
        return render(request, 'notification/index.html', {'form': form})


# Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({'accept': True})
    # Work out user name from path (ignore slashes)
    user = message.content['path'].strip('/')
    # Save user in session and add us to the group
    message.channel_session['user'] = user
    Group('%s' % user).add(message.reply_channel)

    # (Justin) We can use query string to carry subsribed group info on each user
    query_string_dict = parse_qs(message.content['query_string'])
    subcribed_group_list = [k for (k, v) in query_string_dict.items() if v == ['true']]
    for subcribed_group in subcribed_group_list:
        message.channel_session['group'] = subcribed_group
        Group('%s' % subcribed_group).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group('%s' % message.channel_session['user']).send({
        'text': message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group('%s' % message.channel_session['user']).discard(message.reply_channel)