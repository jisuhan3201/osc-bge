from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core import serializers
from osc_bge.users import models as user_models
from osc_bge.bge import models as bge_models
from osc_bge.school import models as school_models
from osc_bge.student import models as student_models

# Create your views here.

class BranchStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/statistics.html', {})


class BranchSecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/secondary.html', {})


class BranchStudentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        try:
            bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
            found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
        except bge_models.BgeBranch.DoesNotExist:
            return HttpResponse('Wrong Branch Id', status=400)

        all_schools = school_models.School.objects.filter(provider_branch=found_branch)
        all_students = student_models.Student.objects.filter(school__in=all_schools)

        return render(request, 'branch/students.html', {
            "all_students":all_students,
        })


class BranchHostsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        try:
            bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
            found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
        except bge_models.BgeBranch.DoesNotExist:
            return HttpResponse('Wrong Branch ID', status=400)

        all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
        for host in all_hosts:
            host.student_length = models.HostStudent.objects.filter(host=host).count()

        return render(request, 'branch/hosts.html', {
            'all_hosts':all_hosts
        })


class BranchResourcesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/resources.html', {})


class HostCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        try:
            bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
            found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
        except bge_models.BgeBranch.DoesNotExist:
            return HttpResponse('Wrong Branch ID', status=400)

        all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
        all_host_coordi = user_models.BgeBranchCoordinator.objects.filter(branch=found_branch, position='host_coordi')
        all_schools = school_models.School.objects.filter(provider_branch=found_branch)
        all_students = student_models.Student.objects.filter(school__in=all_schools, host__isnull=True)

        return render(request, 'branch/host_create.html', {
            'all_hosts':all_hosts,
            'found_branch':found_branch,
            'all_students':all_students,
            'all_host_coordi':all_host_coordi,
        })

    def post(self, request):

        data = request.POST
        try:
            found_host_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('host_coordi')))
        except user_models.BgeBranchCoordinator.DoesNotExist:
            return HttpResponse('Wrong Host coordi id', status=404)
        try:
            found_branch = bge_models.BgeBranch.objects.get(id=int(data.get('provider_branch')))
        except bge_models.BgeBranch.DoesNotExist:
            return HttpResponse('Wrong Bge Branch id', status=404)

        host = models.HostFamily(
            host_coordi=found_host_coordi,
            provider_branch=found_branch,
            name=data.get('name'),
            status=data.get('status'),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get("email"),
            possible_school=data.get("possible_school"),
            occupation=data.get("occupation"),
            employer=data.get("employer"),
            marital_status=data.get("marital_status"),
            children=data.get("children"),
            pets=data.get("pets"),
            student_preference=data.get("student_preference"),
            hosting_capacity=data.get("hosting_capacity"),
            starting_date=data.get("starting_date"),
            last_update_date=data.get("last_update_date"),
            comment=data.get("comment"),
            provider=data.get("provider"),
        )
        host.save()

        if data.getlist('hosting_students'):
            for student in data.getlist('hosting_students'):
                try:
                    found_student = student_models.Student.objects.get(id=int(student))
                except student_models.Student.DoesNotExist:
                    return HttpResponse('Wrong Student Id', status=404)

                host_student = models.HostStudent(
                    host=host,
                    student=found_student,
                )
                host_student.save()

        #Host File save
        #Host photo SAVE

        return HttpResponseRedirect('/branch/hosts')


class HostUpdateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, host_id=None):

        if host_id:

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except bge_models.BgeBranch.DoesNotExist:
                return HttpResponse('Wrong Branch ID', status=400)

            try:
                found_host = models.HostFamily.objects.get(pk=int(host_id))
            except models.HostFamily.DoesNotExist:
                return HttpResponse('Wrong Host id', status=404)

            all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = student_models.Student.objects.filter(school__in=all_schools)

            found_host_students = models.HostStudent.objects.filter(host=found_host)
            host_student_list = []
            for student in found_host_students:
                host_student_list.append(student.student.id)

            found_coordi = user_models.BgeBranchCoordinator.objects.get(host=found_host)
            all_host_coordi = user_models.BgeBranchCoordinator.objects.filter(branch=found_branch, position='host_coordi')

        else:
            return HttpResponse('No Host id', status=400)

        return render(request, 'branch/host_info.html', {
            'all_hosts':all_hosts,
            'found_host':found_host,
            'host_student_list':host_student_list,
            'found_coordi':found_coordi,
            'found_branch':found_branch,
            'all_host_coordi':all_host_coordi,
            'all_students':all_students,
        })

    def post(self, request, host_id=None):

        if host_id:

            data = request.POST

            try:
                found_host = models.HostFamily.objects.get(pk=int(host_id))
            except models.HostFamily.DoesNotExist:
                return HttpResponse('Wrong Host id', status=404)

            try:
                found_host_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('host_coordi')))
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse('Wrong Host coordi id', status=404)
            try:
                found_branch = bge_models.BgeBranch.objects.get(id=int(data.get('provider_branch')))
            except bge_models.BgeBranch.DoesNotExist:
                return HttpResponse('Wrong Bge Branch id', status=404)

            found_host.host_coordi=found_host_coordi
            found_host.provider_branch=found_branch
            found_host.name=data.get('name')
            found_host.status=data.get('status')
            found_host.address=data.get('address')
            found_host.phone=data.get('phone')
            found_host.email=data.get("email")
            found_host.possible_school=data.get("possible_school")
            found_host.occupation=data.get("occupation")
            found_host.employer=data.get("employer")
            found_host.marital_status=data.get("marital_status")
            found_host.children=data.get("children")
            found_host.pets=data.get("pets")
            found_host.student_preference=data.get("student_preference")
            found_host.hosting_capacity=data.get("hosting_capacity")
            found_host.starting_date=data.get("starting_date")
            found_host.last_update_date=data.get("last_update_date")
            found_host.comment=data.get("comment")
            found_host.provider=data.get("provider")
            found_host.save()

            if data.getlist('hosting_students'):

                found_host_students = models.HostStudent.objects.filter(host=found_host)
                found_host_students.delete()

                for student in data.getlist('hosting_students'):
                    try:
                        found_student = student_models.Student.objects.get(id=int(student))
                    except student_models.Student.DoesNotExist:
                        return HttpResponse('Wrong Student Id', status=404)

                    host_student = models.HostStudent(
                        host=found_host,
                        student=found_student,
                    )
                    host_student.save()

            #update photo, files

        else:
            return HttpResponse('No host id', status=400)

        return HttpResponseRedirect('/branch/hosts')



class HostLogsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, host_id=None):

        if host_id:

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except bge_models.BgeBranch.DoesNotExist:
                return HttpResponse('Wrong Branch ID', status=400)

            try:
                found_host = models.HostFamily.objects.get(pk=int(host_id))
            except models.HostFamily.DoesNotExist:
                return HttpResponse('Wrong Host id', status=404)

            all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
            all_branch_logs = models.CommunicationLog.objects.filter(host=found_host).order_by("-created_at")

        else:
            return HttpResponse('No Host id', status=400)

        return render(request, 'branch/host_log.html', {
            'all_hosts':all_hosts,
            'found_host':found_host,
            'all_branch_logs':all_branch_logs,
        })

    def post(self, request, host_id=None):

        data = request.POST

        if host_id:

            try:
                found_host = models.HostFamily.objects.get(pk=int(host_id))
            except models.HostFamily.DoesNotExist:
                return HttpResponse('Wrong Host id', status=404)

            if data.get('log_id'):
                found_log = models.CommunicationLog.objects.get(pk=int(data.get('log_id')))
                found_log.writer=request.user
                found_log.date=data.get('date')
                found_log.category=data.get('category')
                found_log.priority=int(data.get('priority')) if data.get('priority') else None
                found_log.comment=data.get('comment')
                found_log.save()

            else:

                log = models.CommunicationLog(
                    host=found_host,
                    writer=request.user,
                    date=data.get('date'),
                    category=data.get('category'),
                    priority=int(data.get('priority')) if data.get('priority') else None,
                    comment=data.get('comment')
                )
                log.save()

        else:
            return HttpResponse('No host id', status=400)

        return HttpResponseRedirect(request.path_info)


@login_required(login_url='/accounts/login')
def communication_log_get(request, log_id=None):

    if log_id:

        try:
            found_log = models.CommunicationLog.objects.filter(pk=log_id)
        except models.CommunicationLog.DoesNotExist:
            return HttpResponse("Log ID does not exist", status=400)

        data = serializers.serialize("json", found_log)

        return HttpResponse(data, content_type="application/json")

    else:
        return HttpResponse("Log ID IS NULL", statue=400)


class HostReportTestView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/host_report.html', {})
