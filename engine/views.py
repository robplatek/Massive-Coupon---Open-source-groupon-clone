import os.path
import time, datetime, calendar, random
import logging
from urllib import quote, unquote, urlencode
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from engine.forms import *
from engine.models import *
import math
import pdb
import uuid

from paypalxpress.driver import PayPal
from paypalxpress.models import PayPalResponse

def user_signup(request):
  cities = City.objects.all()

  if request.method == 'POST': # If the form has been submitted...
    form = SignupForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data

      user = User()
      user.username = cd.get('email')  #str(uuid.uuid4())[:30]
      user.first_name = cd.get('full_name')
      user.email = cd.get('email')
      user.save()
      user.set_password( cd.get('password') )
      user.save()

      user = authenticate(username=user.username, password=cd.get('password'))
      if user is not None:
        if user.is_active:
          login(request, user)
          # Redirect to a success page.
        else:
          pass
          # Return a 'disabled account' error message
      else:
        # Return an 'invalid login' error message.
        pass

      return HttpResponseRedirect('/')


  else:
    initial_data = {}
    form = SignupForm(initial=initial_data)

  return render_to_response('user_signup.html', {
                'form' : form,
                'cities' : cities,
              }, context_instance=RequestContext( request ) )


def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')


def user_login(request):
  cities = City.objects.all()

  if request.method == 'POST': # If the form has been submitted...
    form = LoginForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data

      login(request, form.user)

      return HttpResponseRedirect('/')


  else:
    initial_data = {}
    form = LoginForm(initial=initial_data)

  return render_to_response('user_login.html', {
                'form' : form,
                'cities' : cities,
              }, context_instance=RequestContext( request ) )





def terms(request):
  cities = City.objects.all()
  return render_to_response('terms.html', {
                  'cities' : cities,
              }, context_instance=RequestContext( request ) )

def faq(request):
  cities = City.objects.all()
  return render_to_response('faq.html', {
                  'cities' : cities,
              }, context_instance=RequestContext( request ) )

def howitworks(request):
  cities = City.objects.all()
  return render_to_response('howitworks.html', {
                  'cities' : cities,
              }, context_instance=RequestContext( request ) )

def aboutus(request):
  cities = City.objects.all()
  return render_to_response('aboutus.html', {
                  'cities' : cities,
              }, context_instance=RequestContext( request ) )


def contactus(request):
  cities = City.objects.all()
  return render_to_response('contactus.html', {
                  'cities' : cities,
              }, context_instance=RequestContext( request ) )



def city_subscribe(request, city_slug):
  try:
    city = City.objects.get(slug=city_slug)
  except:
    return HttpResponseRedirect('/deals/groupon-clone/')


  if request.method == 'POST': # If the form has been submitted...
    form = EmailSubForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data

      esub = EmailSubscribe()
      esub.email = cd.get('email')
      ecity = City.objects.get(id = int(cd.get('city')))
      esub.city = ecity
      esub.save()

      user_msg = "Thanks for subscribing!"
      user_msg = quote(user_msg)
      return HttpResponseRedirect('/?user_msg=' + user_msg)

      # set some sort of message and redirect back to deals

  else:
    initial_data = { 'city': city.id }
    form = EmailSubForm(initial=initial_data)

  cities = City.objects.all()

  return render_to_response('email_subscribe.html', {
                'city' : city,
                'form' : form,
                'cities' : cities,
              }, context_instance=RequestContext( request ) )


@login_required
def profile(request):
  cities = City.objects.all()
  coupons = Coupon.objects.filter(user = request.user, status=STATUS_ACTIVE)

#@login_required  # unlock to make fb work!!
def index(request):

  try:
    user_msg = request.GET.get('user_msg', None)
  except:
    user_msg = None

  if user_msg:
    return HttpResponseRedirect('/deals/groupon-clone/?user_msg=' + user_msg )
  else:
    return HttpResponseRedirect('/deals/groupon-clone/' )


#  return render_to_response('index.html', {
#             #   'now' : now,
#              }, context_instance=RequestContext( request ) )



def deal_checkout_complete(request, slug, quantity):

  user_msg = ""
  quantity = int(quantity)

  try:
    deal = Deal.objects.get(slug=slug)
  except:
    return Http404()

  token = request.GET.get('token', None)
  payerid = request.GET.get('PayerID', None)

  if token and payerid:

    # TODO: i have no idea how many they bought!
    p = PayPal()
    rc = p.DoExpressCheckoutPayment("CAD", quantity * deal.deal_price, token, payerid, PAYMENTACTION="Authorization")

    if rc:  # payment is looking good

      response = PayPalResponse()
      response.fill_from_response(p.GetPaymentResponse())
      response.status = PayPalResponse.get_default_status()
      response.save()

      num_sold = deal.num_sold()

      # check if it's sold out!
      if num_sold > deal.max_available:
        pass
        #setup form error
        # Sold out!


      for i in range(quantity):
        coupon = Coupon()
        coupon.user = request.user
        coupon.deal = deal

        coupon.status = STATUS_ONHOLD

        coupon.save()
        num_sold = num_sold + 1

        # update the deal object 
        if not deal.is_deal_on and num_sold >= deal.tipping_point:
          deal.tipped_at = datetime.datetime.now()
          deal.is_deal_on = True
          deal.save()


      user_msg = 'Thanks for purchasing a Massive Coupon! It will arrive in your profile within 24 hours'
      return HttpResponseRedirect('/deals/groupon-clone/?user_msg=' + user_msg )
    else:
      return Http404()

  else:
    return Http404()


def deal_checkout(request, slug):

  user_msg = ""

  try:
    deal = Deal.objects.get(slug=slug)
  except:
    return HttpResponseRedirect('/')
 

  must_login_error = False
  must_login_email = None

  if request.method == 'POST': # If the form has been submitted...
    form = DealCheckoutForm(request.POST)

    # before we do anything, check if this user has an account and isn't logged in
    if not request.user.is_authenticated():
      try:
        user = User.objects.get(email=request.POST['email'])
        must_login_error = True
        must_login_email = request.POST['email']
        form = DealCheckoutForm(initial={})
        user_msg = 'An account already exists for ' + user.email  + '. Please sign in first.'
      except:
        pass

    else:
      user = request.user

    if not must_login_error and form.is_valid():
      cd = form.cleaned_data

      if not request.user.is_authenticated():
        # User in NOT Logged IN and doesn't exist
        # setup a new user
        user = User()
        user.username = cd.get('email')  #str(uuid.uuid4())[:30]
        user.first_name = cd.get('full_name')
        user.email = cd.get('email')
        user.save()
        user.set_password( cd.get('password') )
        user.save()


        user = authenticate(username=user.username, password=cd.get('password'))
        if user is not None:
          if user.is_active:
            login(request, user)
            # Redirect to a success page.
          else:
            pass
            # Return a 'disabled account' error message
        else:
          # Return an 'invalid login' error message.
          pass

      quantity = int(cd.get('quantity'))
      total_price = quantity * deal.deal_price

      p = PayPal()
      rc = p.SetExpressCheckout(total_price, "CAD", "http://www.massivecoupon.com/deals/" + deal.slug + "/" + str(quantity) + "/checkout/complete/", "http://www.massivecoupon.com/", PAYMENTACTION="Authorization")

      if rc:
        token = p.api_response['TOKEN'][0]
        return HttpResponseRedirect( p.paypal_url() )
      else:
        return HttpResponseRedirect('/checkout/error') 
 



  else:
    initial_data = {}
    form = DealCheckoutForm(initial=initial_data)

  cities = City.objects.all()

  return render_to_response('deal_checkout.html', {
                'form' : form,
                'deal' : deal,
                'user_msg' : user_msg,
                'must_login_error' : must_login_error,
                'must_login_email' : must_login_email,
                'cities' : cities,
              }, context_instance=RequestContext( request ) )

def deal_detail(request, slug=None):

  try:
    user_msg = request.GET.get('user_msg', None)
  except:
    user_msg = None

  if slug == None:
    deal = Deal.objects.all()[0]
  else:
    deal = Deal.objects.get(slug=slug)

  if not deal.is_expired(): 
    countdown_time = deal.date_published.strftime("%Y,%m,%d") #+ ' 11:59 PM'
  else:
    countdown_time = -1

  cities = City.objects.all()

  return render_to_response('deal_detail.html', {
             #   'now' : now,
                'user_msg' : user_msg,
                'deal' : deal,
                'countdown_time' : countdown_time,
                'cities' : cities,
              }, context_instance=RequestContext( request ) )


