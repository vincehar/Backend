from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from YouWeesh.Serializers.EventSerializer import EventSerializer
from YouWeesh.Tools.app import App
from YouWeesh.Models.Events import Events
from mongoengine.queryset import DoesNotExist


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getEventById(request, _event_id):

    event = Events.objects.get(id=_event_id)
    eventSerializer = EventSerializer(instance=event)
    return Response(eventSerializer.data)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def addParticipant(request):
    event = Events.objects.get(id=request.POST['eventId'])
    connected_user = App.getCurrentUser(request)
    if connected_user not in event.participants:
        event.add_participant(connected_user)
    return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def deleteParticipant(request):
    event = Events.objects.get(id=request.POST['eventId'])
    connected_user = App.getCurrentUser(request)
    if connected_user in event.participants:
         event.update(pull__participants=connected_user)
    return Response(True)