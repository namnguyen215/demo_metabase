from django.http import HttpResponse
from django.shortcuts import render
import jwt
from django.contrib.auth.decorators import login_required
import time

METABASE_SITE_URL = "localhost:3000"
METABASE_SECRET_KEY = "185fa7b5f2e4d8780702551333726c9a17665859d6fef2ca6d32731a4c253117"

def get_token(payload):
    return jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256").decode('utf8')

def index(request):
    return render(request,
                  'user_stats/index.html',
                  {})

def signed_public_dashboard(request):
    payload = {
    "resource": {"dashboard": 1},
    "params": {
        
    },
    "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=true&refresh=1"

    return render(request,
                  'user_stats/signed_public_dashboard.html',
                  {'iframeUrl': iframeUrl})
@login_required
def signed_chart(request, user_id):
    payload = {
        "resource": {"question": 2},
        "params": {
            "person_id": user_id
        }
    }

    iframeUrl = METABASE_SITE_URL + "/embed/question/" + get_token(payload) + "#bordered=true"

    if request.user.is_superuser:
        # always show admins user stats
        return render(request,
                      'user_stats/signed_chart.html',
                      {'iframeUrl': iframeUrl})
    elif request.user.id == user_id:
        return render(request,
                      'user_stats/signed_chart.html',
                      {'iframeUrl': iframeUrl})
    else:
        return HttpResponse("You're not allowed to look at user %s." % user_id)

@login_required
def signed_dashboard(request, user_id):
    payload = {
        "resource": {"dashboard": 2},
        "params": {
            "id": user_id
        }
    }

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=true"

    if request.user.is_superuser:
        # always show admins user stats
        return render(request,
                      'user_stats/signed_dashboard.html',
                      {'iframeUrl': iframeUrl})
    elif request.user.id == user_id:
        return render(request,
                      'user_stats/signed_dashboard.html',
                      {'iframeUrl': iframeUrl})
    else:
        return HttpResponse("You're not allowed to look at user %s." % user_id)


