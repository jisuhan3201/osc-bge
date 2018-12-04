from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from osc_bge.agent import models as agent_models


@login_required(login_url='/accounts/login/')
def index(request):

    if request.user.is_authenticated:

        if request.user.type == 'bge_admin':
            return redirect('/statistics')

        elif request.user.type == 'bge_team':
            return redirect('/team-statistics')

        elif request.user.type == 'bge_branch_admin':
            return redirect('/branch/statistics')

        elif request.user.type == "agency_admin":

            return redirect('/agent/statistics')

        else:
            return redirect('/agent/counsel')


class BgeStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/statistics.html', {})


class BranchesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/branches.html', {})


class AgentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        all_agents = agent_models.AgencyHead.objects.all()

        return render(request, 'main/agents.html', {
            'all_agents':all_agents,
        })


class AgentsCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        all_agents = agent_models.AgencyHead.objects.all()

        return render(request, 'main/agent_info_create.html', {
            'all_agents':all_agents,
        })

    def post(self, request):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        data = request.POST

        agent = agent_models.AgencyHead(
            name=data.get('name'),
            location=data.get('location'),
            number_branches=data.get('number_branches'),
            capacity_students = data.get('capacity_students'),
            commission=data.get('commission'),
            promotion=data.get('promotion'),
            others=data.get('others'),
            comment=data.get('comment'),
        )
        agent.save()

        if data.getlist('program'):
            for program in data.getlist('program'):
                agency_program = agent_models.AgencyProgram(
                    head=agent,
                    program=program
                )
                agency_program.save()

        return HttpResponseRedirect('/agents')


class AgentsUpdateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, agent_id=None):

        # Agent Update
        if agent_id:

            try:
                found_agent = agent_models.AgencyHead.objects.get(pk=agent_id)
            except agent_models.AgencyHead.DoesNotExist:
                return HttpResponse("Wrong Agent ID", status=400)

            all_agents = agent_models.AgencyHead.objects.all()
            agent_programs = agent_models.AgencyProgram.objects.filter(head=found_agent)
            program_list = []
            if agent_programs:
                for program in agent_programs:
                    program_list.append(program.program)

            contact_infos = agent_models.AgencyHeadContactInfo.objects.filter(agent=found_agent)
            if contact_infos:
                contact_infos_count = contact_infos.count()
                rest_contact_infos = 3 - contact_infos_count
                rest_contact_range = range(1, rest_contact_infos+1)
            else:
                rest_contact_range = range(1, 4)
                contact_infos_count = 0

        else:
            return HttpResponse("Wrong id", status=400)

        return render(request, 'main/agent_info.html', {
            "found_agent":found_agent,
            'all_agents':all_agents,
            'program_list':program_list,
            'contact_infos':contact_infos,
            'contact_infos_count':contact_infos_count,
            'rest_contact_range':rest_contact_range,
        })

    def post(self, request, agent_id=None):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        data = request.POST

        if agent_id:

            if data.get('type') == 'agent_information':

                try:
                    found_agent = agent_models.AgencyHead.objects.get(pk=agent_id)
                except agent_models.AgencyHead.DoesNotExist:
                    return HttpResponse("Wrong Agent ID", status=400)

                found_agent.name = data.get('name')
                found_agent.contracted_date = data.get('contracted_date')
                found_agent.location = data.get('location')
                found_agent.number_branches = data.get('number_branches')
                found_agent.capacity_students = data.get('capacity_students')
                found_agent.commission = data.get('commission')
                found_agent.promotion = data.get('promotion')
                found_agent.others = data.get('others')
                found_agent.comment = data.get('comment')
                found_agent.save()

                if data.getlist('program'):
                    found_programs = agent_models.AgencyProgram.objects.filter(head=found_agent)
                    found_programs.delete()
                    for program in data.getlist('program'):
                        agent_program = agent_models.AgencyProgram(
                            head=found_agent,
                            program=program
                        )
                        agent_program.save()

            if data.get('type') == 'contact_information':

                try:
                    found_agent = agent_models.AgencyHead.objects.get(pk=agent_id)
                except agent_models.AgencyHead.DoesNotExist:
                    return HttpResponse("Wrong Agent ID", status=400)

                if data.getlist('info_id'):
                    print(data)
                    for num in data.getlist('info_id'):
                        try:
                            found_info = agent_models.AgencyHeadContactInfo.objects.get(pk=int(num))
                        except agent_models.AgencyHeadContactInfo.DoesNotExist:
                            return HttpResponse('Wrong id', status=400)

                        found_info.name = data.get('name'+str(num))
                        found_info.contracted_date = data.get('contracted_date'+str(num))
                        found_info.phone = data.get('phone'+str(num))
                        found_info.email = data.get('email' + str(num))
                        found_info.skype = data.get('skype'+str(num))
                        found_info.wechat = data.get('wechat'+str(num))
                        found_info.location = data.get('location'+str(num))
                        found_info.level = data.get('level'+str(num))
                        found_info.image = data.get('image'+str(num))
                        found_info.save()

                if data.get('fname1'):
                    contact_info = agent_models.AgencyHeadContactInfo(
                        agent=found_agent,
                        name=data.get('fname1'),
                        contracted_date=data.get('fcontracted_date1'),
                        phone=data.get('fphone1'),
                        email=data.get('femail1'),
                        skype=data.get('fskype1'),
                        wechat=data.get('fwechat1'),
                        location=data.get('flocation1'),
                        level=data.get('flevel1'),
                        image=data.get('fimage1'),
                    )
                    contact_info.save()
                if data.get('fname2'):
                    contact_info = agent_models.AgencyHeadContactInfo(
                        agent=found_agent,
                        name=data.get('fname2'),
                        contracted_date=data.get('fcontracted_date2'),
                        phone=data.get('fphone2'),
                        email=data.get('femail2'),
                        skype=data.get('fskype2'),
                        wechat=data.get('fwechat2'),
                        location=data.get('flocation2'),
                        level=data.get('flevel2'),
                        image=data.get('fimage2'),
                    )
                    contact_info.save()
                if data.get('fname3'):
                    contact_info = agent_models.AgencyHeadContactInfo(
                        agent=found_agent,
                        name=data.get('fname3'),
                        contracted_date=data.get('fcontracted_date3'),
                        phone=data.get('fphone3'),
                        email=data.get('femail3'),
                        skype=data.get('fskype3'),
                        wechat=data.get('fwechat3'),
                        location=data.get('flocation3'),
                        level=data.get('flevel3'),
                        image=data.get('fimage3'),
                    )
                    contact_info.save()

        else:
            return HttpResponse("Id not found", status=400)

        return HttpResponseRedirect('/agents')


@login_required(login_url='/accounts/login/')
def delete_contact_info(request, agent_id=None, contact_id=None):

    if contact_id and agent_id:

        try:
            found_contact_info = agent_models.AgencyHeadContactInfo.objects.get(pk=contact_id)
        except agent_models.AgencyHeadContactInfo.DoesNotExist:
            return HttpResponse(status=400)

        found_contact_info.delete()

    else:
        return HttpResponse(status=400)

    return HttpResponseRedirect("/agents/info/"+str(agent_id))





class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/secondary.html', {})


class BgeTeamStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'team/statistics.html', {})


class BgeCollegeView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'school/colleges.html', {})

class BgeAccountingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/accounting.html', {})
