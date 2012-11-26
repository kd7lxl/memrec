from models import Mission, Signin
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def emd078(request, mission_id):
    mission = Mission.objects.get(pk=mission_id)
    return render_to_response(
        'admin/mission/mission/emd078.html',
        {
            'mission': mission,
            'pad': xrange(mission.signin_set.count() + 1, 30 + 1),
        },
        RequestContext(request, {}),
    )
emd078 = staff_member_required(emd078)
