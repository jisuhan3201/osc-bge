from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from . import models, forms
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
from django.db.models import Q


# Create your views here.

class BranchStatisticsView(LoginRequiredMixin, View):
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

        now = datetime.datetime.now()
        year_list = []
        for year in range(2018, now.year+1):
            year_list.append(year)
        year_list = sorted(year_list, reverse=True)


        all_schools = school_models.School.objects.filter(provider_branch=found_branch)
        all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)

        today = datetime.date.today()
        next_month = today + relativedelta.relativedelta(months=1)

        # end_date = datetime.date(next_month.year, next_month.month, 1) - relativedelta.relativedelta(days=1)

        applied_students = form_models.Counsel.objects.filter(
            student__status='registered', formality__school_formality__school__in=all_schools)

        confirmed_students = form_models.SchoolFormality.objects.filter(
            school__in=all_schools)

        default_start_date = datetime.date(today.year, today.month, 1)

        start_date = datetime.date(today.year, today.month, 1)

        applied_students = applied_students.filter(
            formality__created_at__gte=start_date)

        confirmed_students = confirmed_students.filter(
            acceptance_date__gte=start_date).order_by('-acceptance_date')

        found_branch.school_count = school_models.School.objects.filter(provider_branch=found_branch)
        found_branch.active_host = models.HostFamily.objects.filter(provider_branch=found_branch, status='active')
        found_branch.inactive_host = models.HostFamily.objects.filter(provider_branch=found_branch, status='inactive')
        found_branch.prospective_host = models.HostFamily.objects.filter(provider_branch=found_branch, status='prospective')
        found_branch.current_students = student_models.Student.objects.filter(school__in=all_schools).exclude(status__in=['transferred', 'graduated', 'terminated'])
        #found_branch.complaints = (models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts).count() +
        #    student_models.StudentCommunicationLog.objects.filter(category='complaints', student__school__in=all_schools).count())
        found_branch.complaints = (
            models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts).count())

        if request.GET.get('form_type'):

            month_value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            if not request.GET.get('year'):
                start_year = str(datetime.today().year)
                end_year = str(datetime.today().year)
            else:
                start_year = request.GET.get('year')
                end_year = request.GET.get('year')

            if not request.GET.get('start_month') and not request.GET.get('end_month'):
                start_month = 'Sep'
                end_month = 'Aug'
            elif not request.GET.get('start_month'):
                end_month = request.GET.get('end_month')
                start_month = end_month
            elif not request.GET.get('end_month'):
                start_month = request.GET.get('start_month')
                end_month = start_month
            else:
                start_month = request.GET.get('start_month')
                end_month = request.GET.get('end_month')

            start_year_num = int(start_year)
            end_year_num = int(end_year)
            start_month_num = month_value[month_name.index(start_month)]
            end_month_num = month_value[month_name.index(end_month)]

            if 1 <= start_month_num <= 8:
                if 9 <= end_month_num <= 12:
                    end_month_num = start_month_num
                else:
                    if start_month_num > end_month_num:
                        end_month_num = start_month_num

                start_year_num += 1
                end_year_num += 1

            else:
                if 1 <= end_month_num <= 8:
                    end_year_num += 1
                else:
                    if start_month_num > end_month_num:
                        end_month_num = start_month_num

            start_month = month_name[month_value.index(start_month_num)]
            end_month = month_name[month_value.index(end_month_num)]

            start_date = datetime.datetime.strptime(str(start_year_num) + "-" + start_month + "-01", "%Y-%b-%d")
            end_date = datetime.datetime.strptime(str(end_year_num) + "-" + end_month + "-01", "%Y-%b-%d")
            end_date = end_date + relativedelta.relativedelta(months=1)

            if request.GET.get('form_type') == 'applied_form':
                applied_students = form_models.Counsel.objects.filter(
                    student__status='registered', formality__school_formality__school__in=all_schools)

                applied_students = applied_students.filter(
                    formality__created_at__gte=start_date)

                if end_date:
                    applied_students = applied_students.filter(
                        formality__created_at__lt=end_date)

            elif request.GET.get('form_type') == 'confirmed_form':

                confirmed_students = form_models.SchoolFormality.objects.filter(
                    school__in=all_schools)

                confirmed_students = confirmed_students.filter(
                    acceptance_date__gte=start_date).order_by('-acceptance_date')

                if end_date:
                    confirmed_students = confirmed_students.filter(
                        acceptance_date__lt=end_date).order_by('-acceptance_date')

            else:
                found_branch.school_count = found_branch.school_count.all () #filter(created_at__gte=start_date)
                found_branch.active_host = found_branch.active_host.filter(created_at__gte=start_date)
                found_branch.inactive_host = found_branch.inactive_host.filter(created_at__gte=start_date)
                found_branch.prospective_host = found_branch.prospective_host.filter(created_at__gte=start_date)
                found_branch.current_students = found_branch.current_students.filter(created_at__gte=start_date)
                #found_branch.complaints = (models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts, created_at__gte=start_date).count() +
                #    student_models.StudentCommunicationLog.objects.filter(category='complaints', student__school__in=all_schools, created_at__gte=start_date).count())
                found_branch.complaints = (
                    models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts,
                                                           created_at__gte=start_date).count())


                if end_date:
                    found_branch.school_count = found_branch.school_count.all() #filter(created_at__lt=end_date)
                    found_branch.active_host = found_branch.active_host.filter(created_at__lt=end_date)
                    found_branch.inactive_host = found_branch.inactive_host.filter(created_at__lt=end_date)
                    found_branch.prospective_host = found_branch.prospective_host.filter(created_at__lt=end_date)
                    found_branch.current_students = found_branch.current_students.all() #filter(created_at__lt=end_date)
                    #found_branch.complaints = (models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts, created_at__gte=start_date, created_at__lt=end_date).count() +
                    #    student_models.StudentCommunicationLog.objects.filter(category='complaints', student__school__in=all_schools, created_at__gte=start_date, created_at__lt=end_date).count())
                    found_branch.complaints = (
                        models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts,
                                                               created_at__gte=start_date,
                                                               created_at__lt=end_date).count())

        found_branch.school_count = found_branch.school_count.count()
        found_branch.active_host = found_branch.active_host.count()
        found_branch.inactive_host = found_branch.inactive_host.count()
        found_branch.prospective_host = found_branch.prospective_host.count()
        found_branch.current_students = found_branch.current_students.count()

        return render(request, 'branch/statistics.html', {
            'default_start_date':default_start_date,
            'applied_students':applied_students,
            'confirmed_students':confirmed_students,
            'found_branch':found_branch,
            'year_list':year_list,
        })

@login_required(login_url='/accounts/login/')
def branch_chart_statistics(request):

    if request.GET.get('branch_id'):
        found_branch = bge_models.BgeBranch.objects.get(id=int(request.GET.get('branch_id')))
    else:
        return HttpResponse(status=400)

    all_schools = school_models.School.objects.filter(provider_branch=found_branch)
    all_hosts = models.HostFamily.objects.filter(provider_branch=found_branch)

    today = datetime.date.today()
    month_list = []
    data = []
    chart_type = request.GET.get('chart_type')

    for number in range(0, 12):

        month = datetime.datetime.today() - relativedelta.relativedelta(months=number)
        month = month.strftime("%Y %b")
        month_list.append(month)
        sd = today - relativedelta.relativedelta(months=number, day=1)
        ed = today - relativedelta.relativedelta(months=number-1, day=1)

        if chart_type:

            if chart_type == 'partner':
                schools = all_schools.filter(
                    created_at__lt=ed
                ).count()
                data.append(schools)
                chart_name = 'Partner Schools'

            elif chart_type == 'active_host':
                hosts = models.HostFamily.objects.filter(
                    provider_branch=found_branch,
                    status="active",
                    created_at__lt=ed).count()
                data.append(hosts)
                chart_name = 'Active Host Families'

            elif chart_type == 'inactive_host':
                hosts = models.HostFamily.objects.filter(
                    provider_branch=found_branch,
                    status="inactive",
                    created_at__lt=ed).count()
                data.append(hosts)
                chart_name = 'Inactive Host Families'

            elif chart_type == 'prospective_host':
                hosts = models.HostFamily.objects.filter(
                    provider_branch=found_branch,
                    status="prospective",
                    created_at__lt=ed).count()
                data.append(hosts)
                chart_name = 'Prospective Host Families'

            elif chart_type == 'student_complaints':
                #complaints = (models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts, created_at__range=(sd,ed)).count() +
                #    student_models.StudentCommunicationLog.objects.filter(category='complaints', student__school__in=all_schools, created_at__range=(sd,ed)).count())
                complaints = (models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts,
                                                                     created_at__lt=ed).count())
                data.append(complaints)
                chart_name = 'Complaints'

            else:
                current_students = student_models.Student.objects.filter(
                    school__in=all_schools,
                    created_at__lt=ed,
                ).exclude(status__in=['transferred', 'graduated', 'terminated']).count()
                data.append(current_students)
                chart_name = 'Secondary School Monthly Current Students Information'

        else:
            current_students = student_models.Student.objects.filter(
                school__in=all_schools,
                created_at__lt=ed,
            ).exclude(status__in=['transferred', 'graduated', 'terminated']).count()
            data.append(current_students)
            chart_name = 'Secondary School Monthly Current Students Information'

    month_list.reverse()
    data.reverse()

    result = {
        'months':month_list,
        'chart_name':chart_name,
        'data':data,
    }

    return JsonResponse(result, safe=False)


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

        first_date = datetime.date.today().replace(day=1)
        next_month = first_date + relativedelta.relativedelta(months=1)

        for student in all_students:

            try:
                found_report = student_models.StudentMonthlyReport.objects.filter(student=student).latest('updated_at')
                student.student_report = found_report
                student.num_of_logs = student_models.StudentCommunicationLog.objects.filter(student=student, updated_at__range=(first_date, next_month)).count()
            except student_models.StudentMonthlyReport.DoesNotExist:
                continue

        last_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

        return render(request, 'branch/students.html', {
            "all_students":all_students,
            'last_date':last_date,
        })

    def post(self, request):

        data = request.POST

        if data.get('student_id'):

            try:
                found_student = student_models.Student.objects.get(id=int(data.get('student_id')))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            found_student.status = data.get('status')
            found_student.save()

        else:
            return HttpResponse('No Student Id', status=400)

        return HttpResponseRedirect(request.path_info)


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

        data = request.GET

        category = data.get("category")
        middle_category = data.get("middle_category")
        small_category = data.get("small_category")
        title = data.get("title")

        if category is '' and middle_category is '' and small_category is '' and title is '':
            all_resources = models.BgeResource.objects.all().order_by('-created_at')
        else:
            all_resources = models.BgeResource.objects.filter(Q(category=category) |
                                                              Q(middle_category=middle_category) |
                                                              Q(small_category=small_category) |
                                                              Q(title=title)).order_by('-created_at')

        return render(request, 'branch/resources.html', {
            'all_resources':all_resources,
            'user_type':request.user.type,
        })


    def post(self, request):

        data = request.POST

        if request.user.type == 'bge_branch_admin':
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
        else:
            found_branch=None

        if data.get('delete_file'):

            found_resource = models.BgeResource.objects.get(id=int(data.get('delete_file')))
            found_resource.delete()

            return HttpResponseRedirect(request.path_info)

        resource = models.BgeResource(
            branch=found_branch,
            writer=request.user,
            category=data.get('category') if data.get('category') else None,
            middle_category=data.get('middle_category') if data.get('middle_category') else None,
            small_category=data.get('small_category') if data.get('small_category') else None,
            title=data.get('title') if data.get('title') else None,
        )
        resource.save()

        resource_form = forms.BgeResourceForm(request.POST,request.FILES)
        if resource_form.is_valid():
            resource.file = resource_form.cleaned_data['file']
            resource.save()

        return HttpResponseRedirect(request.path_info)

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

            if request.FILES.getlist('photo'):
                host_form = forms.HostStudentPhotoForm(request.POST, request.FILES)
                if host_form.is_valid():
                    for photo in request.FILES.getlist('photo'):

                        report_photo = models.ReportPhoto()
                        report_photo.report = host_report
                        report_photo.photo = photo
                        report_photo.save()

            if request.FILES.getlist('file'):
                host_form = forms.HostStudentFileForm(request.POST, request.FILES)
                if host_form.is_valid():
                    for file in request.FILES.getlist('file'):

                        report_file = models.ReportFile()
                        report_file.report = host_report
                        report_file.file = file
                        report_file.save()

            if data.get('status') == 'complete':
                host_report.submitted_date = datetime.date.today()
                host_report.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect("/branch/host/report/update/"+str(host_report.id))


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

            if request.FILES.getlist('photo'):
                host_form = forms.HostStudentPhotoForm(request.POST, request.FILES)
                if host_form.is_valid():
                    for photo in request.FILES.getlist('photo'):

                        report_photo = models.ReportPhoto()
                        report_photo.report = found_report
                        report_photo.photo = photo
                        report_photo.save()

            if request.FILES.getlist('file'):
                host_form = forms.HostStudentFileForm(request.POST, request.FILES)
                if host_form.is_valid():
                    for file in request.FILES.getlist('file'):

                        report_file = models.ReportFile()
                        report_file.report = found_report
                        report_file.file = file
                        report_file.save()

            if data.getlist('delete_photo'):
                for num in data.getlist('delete_photo'):
                    found_photo = models.ReportPhoto.objects.get(id=int(num))
                    found_photo.delete()

            if data.getlist('delete_file'):
                for num in data.getlist('delete_file'):
                    found_file = models.ReportFile.objects.get(id=int(num))
                    found_file.delete()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect(request.path_info)
