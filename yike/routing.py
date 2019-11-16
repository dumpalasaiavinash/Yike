from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from chatbox.consumer import msgConsumer
from formCreation.consumer import formsaveConsumer

application = ProtocolTypeRouter({
    'websocket':SessionMiddlewareStack(
        URLRouter(
                    [
                        path('chat/chat/',msgConsumer),
                        path('form/add/',formsaveConsumer),
                    ]
                )
    )
})