from models import Mission, Signin
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

def emd078(request, mission_id):
    return render_to_response(
        'admin/mission/mission/emd078.html',
        {
            'mission': Mission.objects.get(pk=mission_id),
        },
        RequestContext(request, {}),
    )
emd078 = staff_member_required(emd078)
