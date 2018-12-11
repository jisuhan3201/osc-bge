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
from osc_bge.agent import models as agent_models
from osc_bge.form import models as form_models
import datetime
from dateutil import relativedelta

# Create your views here.

class BranchStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):


        return render(request, 'branch/statistics.html', {
        })


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
        except:
            found_branch=None

        if not found_branch:
            try:
                bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                return HttpResponse('Not Branch Admin or Branch coordi', status=400)

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
        except:
            found_branch=None

        if not found_branch:
            try:
                bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                return HttpResponse('Not Branch Admin or Branch coordi', status=400)

        all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
        for host in all_hosts:

            host.student_length = models.HostStudent.objects.filter(host=host).count()

        return render(request, 'branch/hosts.html', {
            'all_hosts':all_hosts
        })

    def post(self, request):

        data = request.POST

        if data.get('student_id'):

            try:
                found_student = student_models.Student.objects.get(id=int(data.get('student_id')))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            found_host_student = models.HostStudent.objects.get(student=found_student)
            found_host_student.next_year_plan = data.get('next_year_plan')
            found_host_student.communication_log = data.get('communication_log')
            found_host_student.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect(request.path_info)

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
        except:
            found_branch=None

        if not found_branch:
            try:
                bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                return HttpResponse('Not Branch Admin or Branch coordi', status=400)

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
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

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
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

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


class HostStudentReportView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, student_id=None):

        if student_id:

            try:
                found_student = student_models.Student.objects.get(id=int(student_id))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            try:
                found_host = models.HostStudent.objects.get(student=found_student)
            except models.HostStudent.DoesNotExist:
                return HttpResponse(status=400)

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)
            all_reports = models.HostStudentReport.objects.filter(
                student=found_student, host=found_host.host).order_by('-created_at')


            due_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'branch/host_report.html', {
            'found_student':found_student,
            'found_host':found_host,
            'all_hosts':all_hosts,
            'all_reports':all_reports,
            'due_date':due_date
        })

    def post(self, request, student_id=None):

        data = request.POST

        if student_id:

            try:
                found_student = student_models.Student.objects.get(id=int(student_id))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            try:
                found_host = models.HostStudent.objects.get(student=found_student)
            except models.HostStudent.DoesNotExist:
                return HttpResponse(status=400)

            try:
                found_host_coordi = user_models.BgeBranchCoordinator.objects.get(user=request.user)
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse('Permission wrong / Not a host coordi', status=400)

            host_report = models.HostStudentReport(
                host_coordi=found_host_coordi,
                host=found_host.host,
                student=found_student,
                description=data.get('description'),
                rate=data.get('rate'),
                improvement=data.get('improvement'),
                cultural_fluency=data.get('cultural_fluency'),
                house_rule_attitude=data.get('house_rule_attitude'),
                responsibility=data.get('responsibility'),
                communication=data.get('communication'),
                sleeping_habits=data.get('sleeping_habits'),
                school_attendance=data.get('school_attendance'),
                comment=data.get('comment'),
                status=data.get('status'),
                due_date=data.get('due_date'),
            )
            host_report.save()

            if data.get('status') == 'complete':
                host_report.submitted_date = datetime.date.today()
                host_report.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect(request.path_info)


class HostStudentReportUpdateView(LoginRequiredMixin, View):

    def get(self, request, report_id=None):

        if report_id:

            try:
                found_report = models.HostStudentReport.objects.get(id=int(report_id))
            except models.HostStudent.DoesNotExist:
                return HttpResponse(status=400)

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)

        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'branch/host_update_report.html', {
            'found_report':found_report,
            'all_hosts':all_hosts,
        })

    def post(self, request, report_id=None):

        data = request.POST

        if report_id:

            try:
                found_report = models.HostStudentReport.objects.get(id=int(report_id))
            except models.HostStudent.DoesNotExist:
                return HttpResponse(status=400)

            if found_report.host_coordi.user != request.user:
                return HttpResponse("You are not the host coordi..", status=401)

            found_report.description=data.get('description')
            found_report.rate=data.get('rate')
            found_report.improvement=data.get('improvement')
            found_report.cultural_fluency=data.get('cultural_fluency')
            found_report.house_rule_attitude=data.get('house_rule_attitude')
            found_report.responsibility=data.get('responsibility')
            found_report.communication=data.get('communication')
            found_report.sleeping_habits=data.get('sleeping_habits')
            found_report.school_attendance=data.get('school_attendance')
            found_report.comment=data.get('comment')
            found_report.status=data.get('status')

            if data.get('status') == 'complete':
                found_report.submitted_date = datetime.date.today()

            found_report.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect("/branch/host/report/"+str(found_report.student.id))
