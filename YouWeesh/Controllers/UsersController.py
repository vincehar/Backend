from collections import Counter

from django.http import Http404
from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from YouWeesh.Models.Address import Address
from YouWeesh.Models.Events import Events
from YouWeesh.Models.FriendsNotifications import FriendsNotifications
from YouWeesh.Models.Level import Level
from YouWeesh.Models.Notifications import Notifications
from YouWeesh.Models.Users import Users
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Models.WeeshMatchingNotifications import WeeshMatchingNotifications
from YouWeesh.Models.WeeshbackNotifications import WeeshbackNotifications
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Serializers.EventSerializer import EventSerializer
from YouWeesh.Serializers.NotificationsSerializer import NotificationsSerializer
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.WishSerializer import WishSerializer
from YouWeesh.Tools.app import App
from YouWeesh.Tools.geolocalisation import geolocalisation

#from rest_framework.authtoken.models import Token
from django.core.files.base import ContentFile
from base64 import b64decode
from datetime import datetime
import json

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny,))
def account(request, _email):
    """
    Get Account information and requests
    :param request:
    :return:
    """
    try:
        connected_user = App.getCurrentUser(request)
        selected_user = Users.objects.get(user__email=_email.lower())
        usersSerializer = UsersSerializer(instance=selected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except selected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(usersSerializer.data)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_favorite_tags(request, _email):
    '''
    Get favorite tags for a user
    :param request:
    :param _email:
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        selected_user = Users.objects.get(user__email=_email)
        lstTags = list()
        lstEvents = Events.objects(Q(creator=selected_user.id) | Q(participants__contains=connected_user.id))
        lstWeesh = Wishes.objects(creator=selected_user.id)

        for ev in lstEvents:
            if len(ev.tags) != 0:
                lstTags.append(ev.tags[0].title.lower())
        for we in lstWeesh:
            if len(we.tags) != 0:
                lstTags.append(we.tags[0].title.lower())

        a = dict(Counter(lstTags).most_common(4))
        print json.dumps(a)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except selected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(json.dumps(a))

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def getNotifications(request):
    try:
        lstNotifs = list()
        connected_user = App.getCurrentUser(request)
        lstNotifs.extend(FriendsNotifications.objects(Q(to_user=connected_user) & Q(is_read=False)))
        lstNotifs.extend(WeeshbackNotifications.objects(Q(to_user=connected_user) & Q(is_read=False)))
        lstNotifs.extend(WeeshMatchingNotifications.objects(Q(to_user=connected_user) & Q(is_read=False)))
        notifs = NotificationsSerializer(instance=lstNotifs, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(notifs.data)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatebackgroundpicture(request):

    try:

        connected_user = App.getCurrentUser(request)
        pictureBase64 = request.data['picture'].encode('utf8')
        picturedata = b64decode(pictureBase64)

        connected_user.preferences.background_picture.replace(ContentFile(picturedata))
        connected_user.save()

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except connected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatepicture(request):

    try:

        connected_user = App.getCurrentUser(request)
        pictureBase64 = request.data['picture'].encode('utf8')
        picturedata = b64decode(pictureBase64)

        connected_user.picture.replace(ContentFile(picturedata))
        connected_user.save()

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except connected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(True)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getNbrFriends(request):
    try:
        connected_user = App.getCurrentUser(request)
        # TODO : Add criteria for relationships
        nbr = len(UsersRelationships.objects(from_user=connected_user.id))
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(nbr)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getFriends(request, _email):
    try:
        users = Users.objects()
        connected_user = Users.objects.get(user__email=_email)
        lstRelationships = UsersRelationships.objects(from_user=connected_user.id)
        lstFriends = list()
        for rl in lstRelationships:
            lstFriends.append(rl.to_user)
        usersSerializer = UsersSerializer(instance=lstFriends, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(usersSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def myNextEvents(request):
    try:
        connected_user = App.getCurrentUser(request)
        #TODO : Select only objects where current user is creator or participant
        lstNextEvents = Events.objects(user_id=connected_user.id)#end_date__lte=datetime.now()) #LTE a changer an SUP
        eventssrz = EventSerializer(instance=lstNextEvents, many=True)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(eventssrz.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshTimeline(request):
    '''
    Get All Weeshes for profile timeline
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        lstweesh = Wishes.objects(Q(creator=connected_user.id) | Q(weeshback__contains=connected_user.id))
        lstWishes = WishSerializer(instance=lstweesh, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(lstWishes.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def eventsTimeline(request):
    '''
    Get All Events for profile timeline
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        lstevents = Events.objects(Q(creator=connected_user.id) | Q(participants__contains=connected_user.id))
        lstev = EventSerializer(instance=lstevents, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(lstev.data)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):

    try:
        _wish_title = request.POST['weesh']
        _idLevel = request.POST['idLevel']

        selectedLevel = Level.objects.get(idLevel=_idLevel)
        connected_user = App.getCurrentUser(request)
        createdWish = connected_user.create_wish(_wish_title, selectedLevel)
        wishSerializer = WishSerializer(instance=createdWish)

        #TODO : Lancer le code suivant en asynchrone
        #1 - rechercher les weeshes similaires avec Tags
        if(len(createdWish.tags) > 0):
            lstMatchingWishes = Wishes.objects(title__icontains=createdWish.tags[0].title)
            geoTool = geolocalisation()
            for aWeesh in lstMatchingWishes:
                if connected_user.user.email != aWeesh.creator.user.email:
                    if geoTool.getDistance(connected_user.current_coordinates, aWeesh.creator.current_coordinates) <= connected_user.preferences.search_distance:
                        isExisting = Notifications.objects(from_user=aWeesh.creator, to_user=connected_user, referenced_object=aWeesh)
                        if len(isExisting) == 0:
                            notif = WeeshMatchingNotifications()
                            notif.referenced_object = aWeesh
                            notif.from_user= aWeesh.creator
                            notif.to_user = connected_user
                            notif.content = aWeesh.creator.user.username + " post a matching Weesh to : "
                            notif.save()

                    if geoTool.getDistance(connected_user.current_coordinates, aWeesh.creator.current_coordinates) <= aWeesh.creator.preferences.search_distance:
                        isExisting = Notifications.objects(from_user=connected_user, to_user=aWeesh.creator, referenced_object=createdWish)
                        if len(isExisting) == 0:
                            notif = WeeshMatchingNotifications()
                            notif.referenced_object = createdWish
                            notif.from_user= connected_user
                            notif.to_user = aWeesh.creator
                            notif.content = connected_user.user.username + " post a matching Weesh to : "
                            notif.save()


    except selectedLevel.DoesNotExist:
        raise Http404('Level is not existing. Check DB')
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(wishSerializer.data)



@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createEvent(request):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    try:
        # 2 - get wish title from form
        eventName = request.data['eventName'].encode('utf8')

        start_date = request.data['startDate'].encode('utf8')
        #end_date = datetime.datetime.strptime(request.POST['endDate'], "%Y/%m/%d %H:%M")

        nbrParticipantsMax = request.data['nbrParticipantsMax'].encode('utf8')
        location = request.data['location'].encode('utf8')
        pvOrPub = request.data['pvOrPub'].encode('utf8')
        _idLevel = request.data['idLevel'].encode('utf8')
        picture = request.data['picture'].encode('utf8')
        description = request.data['description'].encode('utf8')

        picturedata = b64decode(picture)
        oneFile = ContentFile(picturedata)
        selectedLevel = Level.objects.get(idLevel=_idLevel)
        addr= Address()
        addr.city = location
        addr.getorUpdateCoordinates()
        addr.save()

        #TODO:Test si image or not
        App.getCurrentUser(request).create_event(description=description, priv_or_pub=pvOrPub, level=selectedLevel, eventName=eventName, start_date=start_date, end_date=datetime.now(), nbrParticipantsMax=nbrParticipantsMax, address=addr, thumbnail=oneFile)

    except Users.DoesNotExist:
        raise Http404('User id does not exist')
    else:
        return Response()


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatePosition(request):
    """

    :type request: object
    """
    try:
        _lat = request.POST['lat']
        _lng = request.POST['lng']

        connected_user = App.getCurrentUser(request)
        connected_user.update_position(_lat, _lng)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def saveFavoritesSports(request):
    """

    :type request: object
    """
    try:
        connected_user = App.getCurrentUser(request)
        sports = request.POST["favoritessports"].split(";")

        for i, val in enumerate(sports):
            connected_user.preferences.favorites_sports.append(val)

        connected_user.save()

    except connected_user.DoesNotExist:
        return Response(False)
    except Exception:
        return Response(False)
    else:
        return Response(True)



@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def useriscreated(request, email):

    try:
        users = Users.objects.get(user__email=email.lower())
        return Response(True)
    except Exception:
        return Response(False)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allweeshes(request):
    '''
    :return:
    '''
    connected_user = App.getCurrentUser(request)
    if connected_user.preferences.display_weeshes:
        AllWishes = list()
        if connected_user.preferences.selected_network == "PUBLIC":
            AllWishes = Wishes.objects(Q(title__icontains=connected_user.preferences.search_string)).order_by('-creation_date')[0:4]
        if connected_user.preferences.selected_network == "FRIENDS":
            for relationship in getFriends(connected_user):
                for wish in Wishes.objects(Q(creator=relationship.from_user.id) & Q(title__icontains=connected_user.preferences.search_string)).order_by('-creation_date')[0:4]:
                    AllWishes.append(wish)

        lstWishes = WishSerializer(instance=AllWishes, many=True)
        return Response(lstWishes.data)
    else:
        return None

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allEvents(request):
    '''

    :return:
    '''
    connected_user = App.getCurrentUser(request)
    if connected_user.preferences.display_events:
        AllEvents = list()
        if connected_user.preferences.selected_network == "PUBLIC":
            AllEvents = Events.objects(Q(title__icontains=connected_user.preferences.search_string)).order_by('-creation_date')[0:4]
        if connected_user.preferences.selected_network == "friends":
            for relationship in getFriends(connected_user):
                for wish in Events.objects(Q(creator=relationship.from_user.id) & Q(title__icontains=connected_user.preferences.search_string)).order_by('-creation_date')[0:4]:
                    AllEvents.append(wish)

        lstEvents = EventSerializer(instance=AllEvents, many=True)
        return Response(lstEvents.data)
    else:
        return None

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshback(request):
    try:
        connected_user = App.getCurrentUser(request)
        current_wish = Wishes.objects.get(id=request.POST['weesh_id'])
        #Atomic update : allow not to have duplicate !
        current_wish.update(add_to_set__weeshback=connected_user)
        if current_wish.creator.user.email != connected_user.user.email:
            isExisting = Notifications.objects(from_user=connected_user, to_user=current_wish.creator, referenced_object=current_wish)

            if len(isExisting) == 0:
                notif = WeeshbackNotifications()
                notif.referenced_object = current_wish
                notif.from_user= connected_user
                notif.to_user = current_wish.creator
                #TODO : Stock label and message and manage multilang <-> in __init__ of object
                notif.content = connected_user.user.username + " backed you Weesh"
                notif.save()
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except current_wish.DoesNotExist:
        raise Http404('Weesh does not exist')
    return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def unweeshback(request):
    '''
    Unsubscribe a the connected user to a weeshback
    :param request:
    :param _wish_id:
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        current_wish = Wishes.objects.get(id=request.POST['weesh_id'])
        #Atomic update : allow not to have duplicate !
        current_wish.update(pull__weeshback=connected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except current_wish.DoesNotExist:
        raise Http404('Weesh does not exist')
    return Response(True)


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def filter_list(request):
    """
    Define filter for the current user and record it on its preferences
    :param request:
    :return:
    """
    # 1 - record new conf into user preferences

    connected_user = App.getCurrentUser(request)
    try:
        if "eventOk" in request.POST:
            connected_user.preferences.display_events = True
        else:
            connected_user.preferences.display_events = False
        if "weeshOk" in request.POST:
            connected_user.preferences.display_weeshes = True
        else:
            connected_user.preferences.display_weeshes = False

        if "searchedString" in request.POST:
            connected_user.preferences.search_string = request.POST['searchedString']

        connected_user.preferences.selected_network = request.POST['selected_network']
        connected_user.save()
    except Wishes.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return Response(True)

def getUserWithUsername(_username):
    return Users.objects.get(user__username=_username)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def addfriend(request):
    try:
        connected_user = App.getCurrentUser(request)
        friend_user = Users.objects.get(user__email=request.POST['email'])
        connected_user.add_friend(friend_user)

        notif = FriendsNotifications()
        notif.from_user = connected_user
        notif.to_user = friend_user
        notif.content = connected_user.user.username + " added you as a sport mate"
        notif.referenced_object = friend_user
        notif.save()
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return Response(True)


'''
@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def acceptfriend(request, friend_id):
    try:
        connected_user = App.getCurrentUser(request)
        relation = UsersRelationships.objects.get(from_user=friend_id, to_user=connected_user.id)
        relation_symetrical = UsersRelationships(from_user=connected_user.id, to_user=friend_id, accepted=True)
        relation.accepted = True
        relation_symetrical.save()
        relation.save()
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def unfriend(request, _user_id):
    try:
        connected_user = App.getCurrentUser(request)
        relation = UsersRelationships.objects.get(from_user=connected_user.id, to_user=_user_id)
        relation_symetrical = UsersRelationships.objects.get(to_user=connected_user.id, from_user=_user_id)
        relation_symetrical.delete()
        relation.delete()
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')
'''