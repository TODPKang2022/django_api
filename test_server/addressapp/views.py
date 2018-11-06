from django.shortcuts import render
import datetime
import os
import urllib.parse
import json
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from .models import Person
from ast import literal_eval
from rest_framework.response import Response
from rest_framework import views,generics
from rest_framework.permissions import AllowAny



from django.conf import settings
import logging


def main(request):
    context = {}
    if request.method == 'POST':
        post_data = request.POST
        data = {}
        data['name'] = post_data.get('name', None)
        data['email'] = post_data.get('email', None)
        print('post_here')
        if data:
            return redirect('%s?%s' % (reverse('addressesapp.views.main'),
                                       urllib.parse.urlencode({'q': data})))
    elif request.method == 'GET':
        get_data = request.GET
        data = get_data.get('q', None)
        if not data:
            return render_to_response(
                'addressesapp/home.html', context)
        data = literal_eval(get_data.get('q', None))
        print(data)

        if not data['name'] and not data['email']:
            return render_to_response(
                'addressesapp/home.html', context)

        # add person to emails address book or update
        if Person.objects.filter(name=data['name']).exists():
            p = Person.objects.get(name=data['name'])
            p.mail = data['email']
            p.save()
        else:
            p = Person()
            p.name = data['name']
            p.mail = data['email']
            p.save()

        # restart page
        return render_to_response(
            'addressesapp/home.html', context)


def addressesbook(request):
    context = {}
    logging.debug('address book')
    get_data = request.GET
    letter = get_data.get('letter', None)
    if letter:
        contacts = Person.objects.filter(name__iregex=r"(^|\s)%s" % letter)
    else:
        contacts = Person.objects.all()
    # sorted alphabetically
    contacts = sort_lower(contacts, "name")  # contacts.order_by("name")
    context['contacts'] = contacts
    alphabetstring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    context['alphabet'] = [l for l in alphabetstring]
    return render_to_response(
        'addressesapp/book.html', context)


def sort_lower(lst, key_name):
    return sorted(lst, key=lambda item: getattr(item, key_name).lower())


def delete_person(request, name):
    if Person.objects.filter(name=name).exists():
        p = Person.objects.get(name=name)
        p.delete()

    context = {}
    contacts = Person.objects.all()
    # sorted alphabetically
    contacts = sort_lower(contacts, "name")  # contacts.order_by("name")
    context['contacts'] = contacts
    return render_to_response(
        'addressesapp/book.html', context)


def get_contacts(request):
    logging.debug('here')
    print('here')
    if request.method == 'GET':
        get_data = request.GET
        data = get_data.get('term', '')
        print('get contacts:', data)
        if data == 'data_test':
            print('response_test')
            # return render_to_response(
            #     'addressesapp/nopersonfound.html', {})
            return Response({'data_return':'success'})
        else:
            return redirect('%s?%s' % (reverse('addressesapp.views.addressesbook'),
                                       urllib.parse.urlencode({'letter': data})))


def notfound(request):
    context = {}
    return render_to_response(
        'addressesapp/nopersonfound.html', context)


class PageCounts(views.APIView):
    permission_classes = (AllowAny,)

    def get(self ,*args, **kwargs):
        print('here')
        query = self.request.query_params.get
        print('query :', query)
        #searchid = self.kwargs['term']
        #print('get contacts:', searchid)
        # reviewpages = Page.objects.filter(searchterm=searchid).filter(review=True)
        # npos = len([p for p in reviewpages if p.sentiment == 1])
        # nneg = len(reviewpages) - npos
        print('get_test')
        return Response({'npos': query('term'), 'nneg': 2})

