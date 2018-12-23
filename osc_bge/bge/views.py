from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.views import View
from django.contrib.auth import get_user_model
from osc_bge.users import forms as user_forms
from osc_bge.users import models as user_models
from osc_bge.agent import models as agent_models
from osc_bge.form import models as form_models
from osc_bge.school import models as school_models
from osc_bge.branch import models as branch_models
from osc_bge.student import models as student_models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.db.models import Count


@login_required(login_url='/accounts/login/')
def index(request):

    if request.user.is_authenticated:


        if request.user.type == 'bge_admin':
            return redirect('/statistics')

        elif request.user.type == 'bge_team':
            return redirect('/statistics')

        elif request.user.type == 'bge_branch_admin':
            return redirect('/branch/statistics')

        elif request.user.type == "agency_admin":

            return redirect('/agent/statistics')

        elif request.user.type == 'bge_accountant':

            return redirect('/accounting')

        else:
            return redirect('/agent/counsel')


class MypageView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/mypage.html', {})

    def post(self, request):

        if request.FILES.get('image'):
            user_form = user_forms.UserImageForm(request.POST,request.FILES)
            if user_form.is_valid():
                request.user.image = user_form.cleaned_data['image']
                request.user.save()

        if request.POST.get('password'):
            user = authenticate(username=request.user.username, password=request.POST.get('password'))
            if user is not None:
                user.set_password(request.POST.get('new_password'))
                user.save()
            else:
                return HttpResponse('Password Not correct', status=401)

        return HttpResponseRedirect(request.path_info)


class CreateUserView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        if request.user.type == 'bge_admin':

            all_branches = models.BgeBranch.objects.all()
            all_agent_heads = agent_models.AgencyHead.objects.all()
            all_agent_branches = agent_models.Agency.objects.all()

        elif  request.user.type == 'agency_admin':

            all_branches = None
            all_agent_heads = None
            all_agent_branches = agent_models.Agency.objects.filter(head=request.user.agency_head_admin.agency_head)

            return render(request, 'main/create_user.html', {
                'all_branches':all_branches,
                'all_agent_heads':all_agent_heads,
                'all_agent_branches':all_agent_branches,
            })

        else:
            return HttpResponse('Unauthorized User', status=400)


    def post(self, request):

        data = request.POST
        User = get_user_model()

        if request.user.type == 'bge_admin' or request.user.type == 'agency_admin':

            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                address=data.get('address'),
                type=data.get('type')
            )
            user.save()

            if request.FILES.get('image'):
                user_form = user_forms.UserImageForm(request.POST,request.FILES)
                if user_form.is_valid():
                    user.image = user_form.cleaned_data['image']
                    user.save()

            if data.get('type') == 'bge_branch_admin':

                found_branch = models.BgeBranch.objects.get(id=int(data.get('branch')))
                if data.get('branch_user_type') == 'school_coordi':
                    branch_admin = user_models.BgeBranchCoordinator(
                        position='school_coordi',
                        user=user,
                        branch=found_branch,
                    )
                    branch_admin.save()
                elif data.get('branch_user_type') == 'student_coordi':
                    branch_admin = user_models.BgeBranchCoordinator(
                        user=user,
                        branch=found_branch,
                        position='student_coordi',
                    )
                    branch_admin.save()
                elif data.get('branch_user_type') == 'host_coordi':
                    branch_admin = user_models.BgeBranchCoordinator(
                        user=user,
                        branch=found_branch,
                        position='host_coordi',
                    )
                    branch_admin.save()
                else:
                    branch_admin = user_models.BgeBranchAdminUser(
                        user=user,
                        branch=found_branch,
                    )
                    branch_admin.save()

            elif data.get('type') == 'agency_admin':

                found_head = agent_models.AgencyHead.objects.get(id=int(data.get('agent_head')))
                agent_admin = user_models.AgencyHeadAdminUser(
                    user=user,
                    agency_head=found_head
                )
                agent_admin.save()

            elif data.get('type') == 'agency_branch_admin':

                found_agent = agent_models.Agency.objects.get(id=int(data.get('agent_branch')))
                agent_admin = user_models.AgencyAdminUser(
                    user=user,
                    agency=found_agent,
                )
                agent_admin.save()

            elif data.get('type') == 'counselor':

                found_agent = agent_models.Agency.objects.get(id=int(data.get('agent_branch')))
                counselor = user_models.Counselor(
                    user=user,
                    agency=found_agent,
                )
                counselor.save()

        else:
            return HttpResponse('Unauthorized User', status=400)

        return HttpResponseRedirect('/accounts/logout/')


class BgeStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        now = datetime.now()
        year_list = []
        for year in range(2018, now.year+1):
            year_list.append(year)
        year_list = sorted(year_list, reverse=True)

        week_list = []
        for num in range(0, 4):
            start_last_week = datetime.today() - relativedelta(weeks=num)
            end_last_week = datetime.today() - relativedelta(weeks=num+1, days=-1)
            week_list.append([start_last_week, end_last_week])

        day_list = []
        for num in range(0, 7):
            day_list.append(datetime.today() - relativedelta(days=num))

        all_agent_heads = agent_models.AgencyHead.objects.all().annotate(
            inquired_count=Count('agent_branch__counselor__counseling')).order_by('-inquired_count')
        total_inquired = 0
        total_applied = 0
        total_accepted = 0
        total_cancelled = 0
        total_enrolled = 0
        total_accepted_percent = 0
        for head in all_agent_heads:
            inquired = form_models.Counsel.objects.filter(counselor__agency__head=head)
            applied = form_models.Formality.objects.filter(apply_at__isnull=False, counsel__counselor__agency__head=head)
            accepted = form_models.SchoolFormality.objects.filter(
                formality__counsel__counselor__agency__head=head,
                acceptance_date__isnull=False)
            cancelled = form_models.SchoolFormality.objects.filter(
                formality__counsel__counselor__agency__head=head,
                cancel_enrolment_date__isnull=False)
            enrolled = form_models.SchoolFormality.objects.filter(
                formality__counsel__counselor__agency__head=head,
                i20_completed=True)

            if request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                end_date = end_date + relativedelta(months=1)
            elif request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                end_date = end_date + relativedelta(months=1)
            elif request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                end_date = None
            elif request.GET.get('year') and not request.GET.get('start_month') and not request.GET.get('end_month'):
                start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                end_date = start_date + relativedelta(years=1)
            elif not request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                end_date = end_date + relativedelta(months=1)
            elif not request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                end_date = None
            elif not request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                start_date = datetime.strptime(str(now.year) + "-" + str(now.month) + "-01", "%Y-%m-%d")
                end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                end_date = end_date + relativedelta(months=1)
            else:
                start_date = None
                end_date= None

            if start_date:
                inquired = inquired.filter(created_at__gte=start_date)
                applied = applied.filter(apply_at__gte=start_date)
                accepted = accepted.filter(acceptance_date__gte=start_date)
                cancelled = cancelled.filter(cancel_enrolment_date__gte=start_date)
                enrolled = enrolled.filter(i20_received_date__gte=start_date)

            if end_date:
                inquired = inquired.filter(created_at__lt=end_date)
                applied = applied.filter(apply_at__lt=end_date)
                accepted = accepted.filter(acceptance_date__lt=end_date)
                cancelled = cancelled.filter(cancel_enrolment_date__lt=end_date)
                enrolled = enrolled.filter(i20_received_date__lt=end_date)

            program_interested = request.GET.get('program_interested')
            if program_interested:
                inquired = inquired.filter(program_interested=program_interested)
                applied = applied.filter(counsel__program_interested=program_interested)
                accepted = accepted.filter(formality__counsel__program_interested=program_interested)
                cancelled = cancelled.filter(formality__counsel__program_interested=program_interested)
                enrolled = enrolled.filter(formality__counsel__program_interested=program_interested)

            head.inquired = inquired.count()
            head.applied = applied.count()
            head.accepted = accepted.count()
            head.cancelled = cancelled.count()
            head.enrolled = enrolled.count()

            total_inquired += inquired.count()
            total_applied += applied.count()
            total_accepted += accepted.count()
            total_cancelled += cancelled.count()
            total_enrolled += enrolled.count()
            try:
                total_accepted_percent = int(total_accepted * 100 / total_applied)
            except ZeroDivisionError:
                total_accepted_percent = 0

            # Second Part
        new_total_inquired = 0
        new_total_applied = 0
        new_total_accepted = 0
        new_total_cancelled = 0
        new_total_enrolled = 0
        new_total_accepted_percent = 0

        for head in all_agent_heads:

            new_inquired = form_models.Counsel.objects.filter(counselor__agency__head=head)
            new_applied = form_models.Formality.objects.filter(apply_at__isnull=False, counsel__counselor__agency__head=head)
            new_accepted = form_models.SchoolFormality.objects.filter(formality__counsel__counselor__agency__head=head)
            new_cancelled = form_models.SchoolFormality.objects.filter(formality__counsel__counselor__agency__head=head)
            new_enrolled = form_models.SchoolFormality.objects.filter(formality__counsel__counselor__agency__head=head)

            # default 1 week
            if not request.GET.get('new_week') and not request.GET.get('new_day') and not request.GET.get('new_program'):
                new_inquired = new_inquired.filter(
                    created_at__range=(datetime.today() - relativedelta(weeks=1, days=-1), datetime.today()))
                new_applied = new_applied.filter(
                    apply_at__range=(datetime.today() - relativedelta(weeks=1, days=-1), datetime.today()))
                new_accepted = new_accepted.filter(
                    acceptance_date__isnull=False,
                    acceptance_date__range=(datetime.today() - relativedelta(weeks=1, days=-1), datetime.today()))
                new_cancelled = new_cancelled.filter(
                    cancel_enrolment_date__isnull=False,
                    cancel_enrolment_date__range=(datetime.today() - relativedelta(weeks=1, days=-1), datetime.today()))
                new_enrolled = new_enrolled.filter(
                    i20_completed=True,
                    i20_received_date__range=(datetime.today() - relativedelta(weeks=1, days=-1), datetime.today()))

            if request.GET.get('new_week'):
                new_end_date = datetime.strptime(request.GET.get('new_week'), '%Y-%m-%d')
                new_inquired = new_inquired.filter(
                    created_at__range=(new_end_date - relativedelta(weeks=1, days=-1), new_end_date))
                new_applied = new_applied.filter(
                    apply_at__range=(new_end_date - relativedelta(weeks=1, days=-1), new_end_date))
                new_accepted = new_accepted.filter(
                    acceptance_date__isnull=False,
                    acceptance_date__range=(new_end_date - relativedelta(weeks=1, days=-1), new_end_date))
                new_cancelled = new_cancelled.filter(
                    cancel_enrolment_date__isnull=False,
                    cancel_enrolment_date__range=(new_end_date - relativedelta(weeks=1, days=-1), new_end_date))
                new_enrolled = new_enrolled.filter(
                    i20_completed=True,
                    i20_received_date__range=(new_end_date - relativedelta(weeks=1, days=-1), new_end_date))

            if request.GET.get('new_day'):
                new_day = datetime.strptime(request.GET.get('new_day'), '%Y-%m-%d')
                new_inquired = new_inquired.filter(
                    created_at__range=(new_day, new_day + relativedelta(days=1)))
                new_applied = new_applied.filter(
                    apply_at__range=(new_day, new_day + relativedelta(days=1)))
                new_accepted = new_accepted.filter(
                    acceptance_date__isnull=False,
                    acceptance_date__range=(new_day, new_day + relativedelta(days=1)))
                new_cancelled = new_cancelled.filter(
                    cancel_enrolment_date__isnull=False,
                    cancel_enrolment_date__range=(new_day, new_day + relativedelta(days=1)))
                new_enrolled = new_enrolled.filter(
                    i20_completed=True,
                    i20_received_date__range=(new_day, new_day + relativedelta(days=1)))

            new_program_interested = request.GET.get('new_program')
            if new_program_interested:

                new_inquired = new_inquired.filter(program_interested=new_program_interested)
                new_applied = new_applied.filter(counsel__program_interested=new_program_interested)
                new_accepted = new_accepted.filter(formality__counsel__program_interested=new_program_interested)
                new_cancelled = new_cancelled.filter(formality__counsel__program_interested=new_program_interested)
                new_enrolled = new_enrolled.filter(formality__counsel__program_interested=new_program_interested)

            head.new_inquired = new_inquired.count()
            head.new_applied = new_applied.count()
            head.new_accepted = new_accepted.count()
            head.new_cancelled = new_cancelled.count()
            head.new_enrolled = new_enrolled.count()

            new_total_inquired += new_inquired.count()
            new_total_applied += new_applied.count()
            new_total_accepted += new_accepted.count()
            new_total_cancelled += new_cancelled.count()
            new_total_enrolled += new_enrolled.count()
            try:
                new_total_accepted_percent = int(new_total_accepted * 100 / new_total_applied)
            except ZeroDivisionError:
                new_total_accepted_percent = 0

        all_counsel = form_models.Counsel.objects.all()

        if request.GET.get('agent_head'):
            all_counsel = all_counsel.filter(counselor__agency__head__id=int(request.GET.get('agent_head')))

        if request.GET.get('customer_program'):
            all_counsel = all_counsel.filter(program_interested=request.GET.get('customer_program'))

        if request.GET.get('customer_country'):
            all_counsel = all_counsel.filter(student__nationality__iexact=request.GET.get('customer_country'))

        if request.GET.get('customer_search_type') and request.GET.get('search_input'):
            if request.GET.get('customer_search_type') == 'phone':
                all_counsel = all_counsel.filter(student__phone__icontains=request.GET.get('search_input'))
            elif request.GET.get('customer_search_type') == 'email':
                all_counsel = all_counsel.filter(student__email__icontains=request.GET.get('search_input'))
            else:
                all_counsel = all_counsel.filter(student__name__icontains=request.GET.get('search_input'))

        for counsel in all_counsel:
            found_school_formalities = form_models.SchoolFormality.objects.filter(formality__counsel=counsel)
            for school_formality in found_school_formalities:
                if school_formality.acceptance_date:
                    counsel.acceptance_date = school_formality.acceptance_date
                if school_formality.cancel_enrolment_date:
                    counsel.cancel_enrolment_date = school_formality.cancel_enrolment_date
                if school_formality.i20_received_date:
                    counsel.i20_received_date = school_formality.i20_received_date

        paginator = Paginator(all_counsel, 10)
        page = request.GET.get('page')

        try:
            counsels = paginator.get_page(page)
        except PageNotAnInteger:
            counsels = paginator.page(1)
        except EmptyPage:
            counsels = paginator.page(paginator.num_pages)

        return render(request, 'main/statistics.html', {
            'year_list':year_list,
            'week_list':week_list,
            'day_list':day_list,
            'all_agent_heads':all_agent_heads,
            "total_inquired":total_inquired,
            "total_applied":total_applied,
            "total_cancelled":total_cancelled,
            "total_enrolled":total_enrolled,
            "total_accepted":total_accepted,
            "new_total_inquired" : new_total_inquired,
            "new_total_applied" : new_total_applied,
            "new_total_cancelled" : new_total_cancelled,
            "new_total_enrolled" : new_total_enrolled,
            "new_total_accepted" : new_total_accepted,
            "default_start_date": datetime.today() - relativedelta(weeks=1, days=-1),
            "default_end_date":datetime.today(),
            "counsels":counsels,
        })

@login_required(login_url='/accounts/login/')
def chart_bge_statistics(request):

    all_agents = agent_models.AgencyHead.objects.all()

    data_list = []
    for head in all_agents:
        data = {}

        today = date.today()
        acceptance_list = []
        for number in range(0, 12):

            sd = today - relativedelta(months=number)
            ed = today - relativedelta(months=number-1)

            past_start_date = date(sd.year, sd.month, 1)
            past_end_date = date(ed.year, ed.month, 1) - relativedelta(days=1)

            acceptance_count = form_models.SchoolFormality.objects.filter(
                acceptance_date__range=(past_start_date, past_end_date),
                formality__counsel__counselor__agency__head=head
            ).count()
            acceptance_list.append(acceptance_count)

        acceptance_list.reverse()
        data.update({
            "agent": head.name,
            "data":acceptance_list
        })
        data_list.append(data)

    month_list = []
    for num in range(0, 12):

        month = datetime.today() - relativedelta(months=num)
        month = month.strftime("%Y %b")
        month_list.append(month)

    month_list.reverse()

    result = {
        'months':month_list,
        'data':data_list,
    }
    return JsonResponse(result, safe=False)


class BranchesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        now = datetime.now()
        year_list = []
        for year in range(2018, now.year+1):
            year_list.append(year)
        year_list = sorted(year_list, reverse=True)

        all_branches = models.BgeBranch.objects.all()
        for branch in all_branches:

            partner_school = school_models.School.objects.filter(provider_branch=branch)

            branch_hosts = branch_models.HostFamily.objects.filter(
                provider_branch=branch)
            active_hosts = branch_hosts.filter(status='active')
            inactive_hosts = branch_hosts.filter(status='inactive')
            prospective_hosts = branch_hosts.filter(status='prospective')

            current_student = student_models.Student.objects.filter(school__provider_branch=branch)
            student_complaints = branch_models.CommunicationLog.objects.filter(
                host__provider_branch=branch, category='Complaints')

            if request.GET.get('year') or request.GET.get('start_month') or request.GET.get('end_month'):

                if request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                    end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = None
                elif request.GET.get('year') and not request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                    end_date = start_date + relativedelta(years=1)
                elif not request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif not request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = None
                elif not request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + str(now.month) + "-01", "%Y-%m-%d")
                    end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                else:
                    start_date = None
                    end_date= None

                if start_date:
                    partner_school = partner_school.filter(created_at__gte=start_date)
                    active_hosts = active_hosts.filter(created_at__gte=start_date)
                    inactive_hosts = inactive_hosts.filter(created_at__gte=start_date)
                    prospective_hosts = prospective_hosts.filter(created_at__gte=start_date)
                    current_student = current_student.filter(created_at__gte=start_date)
                    student_complaints = student_complaints.filter(created_at__gte=start_date)

                if end_date:
                    partner_school = partner_school.filter(created_at__lt=end_date)
                    active_hosts = active_hosts.filter(created_at__lt=end_date)
                    inactive_hosts = inactive_hosts.filter(created_at__lt=end_date)
                    prospective_hosts = prospective_hosts.filter(created_at__lt=end_date)
                    current_student = current_student.filter(created_at__lt=end_date)
                    student_complaints = student_complaints.filter(created_at__lt=end_date)

            branch.partner_school = partner_school.count()
            branch.active_hosts = active_hosts.count()
            branch.inactive_hosts = inactive_hosts.count()
            branch.prospective_hosts = prospective_hosts.count()
            branch.current_student = current_student.count()
            branch.student_complaints = student_complaints.count()

        return render(request, 'main/branches.html', {
            'all_branches':all_branches,
            'year_list':year_list,
        })

@login_required(login_url='/accounts/login/')
def chart_branch_statistics(request):

    all_branches = models.BgeBranch.objects.all()

    data_list = []
    for branch in all_branches:

        branch_data = []

        partner_school = school_models.School.objects.filter(provider_branch=branch).count()
        branch_hosts = branch_models.HostFamily.objects.filter(
            provider_branch=branch)
        active_hosts = branch_hosts.filter(status='active').count()
        inactive_hosts = branch_hosts.filter(status='inactive').count()
        prospective_hosts = branch_hosts.filter(status='prospective').count()
        current_student = student_models.Student.objects.filter(school__provider_branch=branch).count()
        student_complaints = branch_models.CommunicationLog.objects.filter(
            host__provider_branch=branch, category='Complaints').count()

        branch_data.append(partner_school)
        branch_data.append(active_hosts)
        branch_data.append(inactive_hosts)
        branch_data.append(prospective_hosts)
        branch_data.append(current_student)
        branch_data.append(student_complaints)

        data_list.append({
            'branch':branch.name,
            'data':branch_data,
        })

    return JsonResponse(data_list, safe=False)

class BranchesStatisticView(LoginRequiredMixin,View):
    login_url = '/accounts/login/'

    def get(self, request, branch_id=None):

        if branch_id:

            try:
                found_branch = models.BgeBranch.objects.get(id=int(branch_id))
            except models.BgeBranch.DoesNotExist:
                return HttpResponse('Wrong branch id', status=400)

            now = datetime.now()
            year_list = []
            for year in range(2018, now.year+1):
                year_list.append(year)
            year_list = sorted(year_list, reverse=True)


            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_hosts = branch_models.HostFamily.objects.filter(provider_branch=found_branch)

            today = date.today()
            next_month = today + relativedelta(months=1)

            # end_date = datetime.date(next_month.year, next_month.month, 1) - relativedelta.relativedelta(days=1)

            applied_students = form_models.Counsel.objects.filter(
                student__status='registered', formality__school_formality__school__in=all_schools)

            confirmed_students = form_models.SchoolFormality.objects.filter(
                school__in=all_schools)

            default_start_date = date(today.year, today.month, 1)

            start_date = date(today.year, today.month, 1)

            applied_students = applied_students.filter(
                formality__created_at__gte=start_date)

            confirmed_students = confirmed_students.filter(
                acceptance_date__gte=start_date).order_by('-acceptance_date')

            found_branch.school_count = school_models.School.objects.filter(provider_branch=found_branch)
            found_branch.active_host = branch_models.HostFamily.objects.filter(provider_branch=found_branch, status='active')
            found_branch.inactive_host = branch_models.HostFamily.objects.filter(provider_branch=found_branch, status='inactive')
            found_branch.prospective_host = branch_models.HostFamily.objects.filter(provider_branch=found_branch, status='prospective')
            found_branch.current_students = student_models.Student.objects.filter(school__in=all_schools)
            found_branch.complaints = branch_models.CommunicationLog.objects.filter(category='complaints', host__in=all_hosts)

            if request.GET.get('form_type'):

                if request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                    end_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = None
                elif request.GET.get('year') and not request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(request.GET.get('year') + "-" + "01" + "-01", "%Y-%m-%d")
                    end_date = start_date + relativedelta(years=1)
                elif not request.GET.get('year') and request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                elif not request.GET.get('year') and request.GET.get('start_month') and not request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + request.GET.get('start_month') + "-01", "%Y-%b-%d")
                    end_date = None
                elif not request.GET.get('year') and not request.GET.get('start_month') and request.GET.get('end_month'):
                    start_date = datetime.strptime(str(now.year) + "-" + str(now.month) + "-01", "%Y-%m-%d")
                    end_date = datetime.strptime(str(now.year) + "-" + request.GET.get('end_month') + "-01", "%Y-%b-%d")
                    end_date = end_date + relativedelta(months=1)
                else:
                    end_date= None


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
                    found_branch.school_count = found_branch.school_count.filter(created_at__gte=start_date)
                    found_branch.active_host = found_branch.active_host.filter(created_at__gte=start_date)
                    found_branch.inactive_host = found_branch.inactive_host.filter(created_at__gte=start_date)
                    found_branch.prospective_host = found_branch.prospective_host.filter(created_at__gte=start_date)
                    found_branch.current_students = found_branch.current_students.filter(created_at__gte=start_date)
                    found_branch.complaints = found_branch.complaints.filter(created_at__gte=start_date)

                    if end_date:
                        found_branch.school_count = found_branch.school_count.filter(created_at__lt=end_date)
                        found_branch.active_host = found_branch.active_host.filter(created_at__lt=end_date)
                        found_branch.inactive_host = found_branch.inactive_host.filter(created_at__lt=end_date)
                        found_branch.prospective_host = found_branch.prospective_host.filter(created_at__lt=end_date)
                        found_branch.current_students = found_branch.current_students.filter(created_at__lt=end_date)
                        found_branch.complaints = found_branch.complaints.filter(created_at__lt=end_date)

            found_branch.school_count = found_branch.school_count.count()
            found_branch.active_host = found_branch.active_host.count()
            found_branch.inactive_host = found_branch.inactive_host.count()
            found_branch.prospective_host = found_branch.prospective_host.count()
            found_branch.current_students = found_branch.current_students.count()
            found_branch.complaints = found_branch.complaints.count()


            return render(request, 'branch/statistics.html', {
                'default_start_date':default_start_date,
                'applied_students':applied_students,
                'confirmed_students':confirmed_students,
                'found_branch':found_branch,
                'year_list':year_list,
            })

        else:
            return HttpResponse('No branch id', status=400)


class AgentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        all_agents = agent_models.AgencyHead.objects.all()
        total_inquired = 0
        total_enrolled = 0
        for head in all_agents:
            inquired = form_models.Counsel.objects.filter(counselor__agency__head=head)
            enrolled = form_models.SchoolFormality.objects.filter(
                formality__counsel__counselor__agency__head=head,
                i20_completed=True)

            head.inquired = inquired.count()
            head.enrolled = enrolled.count()

            total_inquired += inquired.count()
            total_enrolled += enrolled.count()

        all_agent_branches = agent_models.Agency.objects.all()
        all_communication_logs = agent_models.AgentRelationshipHistory.objects.all().order_by('-created_at')
        if request.GET.get('agent_head'):
            all_communication_logs = all_communication_logs.filter(head__id=int(request.GET.get('agent_head')))

        paginator = Paginator(all_communication_logs, 10)
        page = request.GET.get('page')

        try:
            logs = paginator.get_page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        return render(request, 'main/agents.html', {
            'all_agents':all_agents,
            'all_agent_branches':all_agent_branches,
            'total_inquired':total_inquired,
            'total_enrolled':total_enrolled,
            'logs':logs,
        })

@login_required(login_url='/accounts/login/')
def chart_agent_statistics(request):

    all_agents = agent_models.AgencyHead.objects.all()

    data_list = []
    for head in all_agents:
        data = {}

        today = date.today()
        inquired_list = []
        enrolled_list = []
        for number in range(0, 5):

            sd = today - relativedelta(years=number)
            ed = today - relativedelta(years=number-1)

            past_start_date = date(sd.year, 1, 1)
            past_end_date = date(ed.year, 1, 1) - relativedelta(days=1)

            inquired_count = form_models.Counsel.objects.filter(
                counseling_date__range=(past_start_date, past_end_date),
                counselor__agency__head=head
            ).count()

            enrolled_count = form_models.SchoolFormality.objects.filter(
                formality__counsel__counselor__agency__head=head,
                i20_completed=True,
                i20_received_date__range=(past_start_date, past_end_date),
            ).count()

            inquired_list.append(inquired_count)
            enrolled_list.append(enrolled_count)

        inquired_list.reverse()
        enrolled_list.reverse()

        data_list.append({
            "agent": str(head.name) + " Inquired",
            "data":inquired_list
        })

        data_list.append({
            "agent": str(head.name) + " Enrolled",
            "data":enrolled_list,
        })


    year_list = []
    for num in range(0, 5):

        year = datetime.today() - relativedelta(years=num)
        year = year.strftime("%Y")
        year_list.append(year)

    year_list.reverse()

    result = {
        'years':year_list,
        'data':data_list,
    }

    return JsonResponse(result, safe=False)

class AgentsCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        all_agents = agent_models.AgencyHead.objects.all()
        all_agent_branches = agent_models.Agency.objects.all()

        return render(request, 'main/agent_info_create.html', {
            'all_agents':all_agents,
            'all_agent_branches':all_agent_branches,
        })

    def post(self, request):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        data = request.POST

        if data.get('agent_type') == 'head':

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

        elif data.get('agent_type') == 'branch':

            try:
                found_head = agent_models.AgencyHead.objects.get(id=int(data.get('agent_head')))
            except agent_models.AgencyHead.DoesNotExist:
                return HttpResponse('Wrong head id', status=400)

            agent = agent_models.Agency(
                head=found_head,
                name=data.get('name'),
                location=data.get('location'),
                capacity_students = data.get('capacity_students'),
                commission=data.get('commission'),
                promotion=data.get('promotion'),
                others=data.get('others'),
                comment=data.get('comment'),
            )
            agent.save()

            if data.getlist('program'):
                for program in data.getlist('program'):
                    agency_program = agent_models.AgencyBranchProgram(
                        branch=agent,
                        program=program
                    )
                    agency_program.save()

        else:
            return HttpResponse("Something goes wrong..", status=400)

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

            relationship_histories = agent_models.AgentRelationshipHistory.objects.filter(head=found_agent)

            # Secondary Program
            now = datetime.now()
            year_list = []
            for year in range(now.year-4, now.year+1):
                year_list.append(year)
            year_list = sorted(year_list, reverse=True)

            all_students = student_models.Student.objects.filter(counselor__agency__head=found_agent)

            secondary_data = []
            camp_data = []
            college_other_data = []
            for year in year_list:
                next_year = year+1
                year = datetime.strptime(str(year) + '-01' + '-01', "%Y-%m-%d")
                next_year = datetime.strptime(str(next_year) + '-01' + '-01', "%Y-%m-%d")
                data = {}
                term_fall = all_students.filter(school__type='secondary', school__term='fall', created_at__gte=year, created_at__lt=next_year).exclude(status='terminated').count()
                term_spring = all_students.filter(school__type='secondary', school__term='spring', created_at__gte=year, created_at__lt=next_year).exclude(status='terminated').count()
                total_new_students = all_students.filter(school__type='secondary', created_at__gte=year, created_at__lt=next_year).exclude(status='terminated').count()
                terminated_students = all_students.filter(school__type='secondary', created_at__gte=year, created_at__lt=next_year, status='terminated').count()
                total_students = all_students.filter(school__type='secondary', created_at__lt=next_year).exclude(status='terminated').count()

                data.update({
                    'period':year,
                    'term_fall':term_fall,
                    'term_spring':term_spring,
                    'total_new_students':total_new_students,
                    'terminated_students':terminated_students,
                    'total_students':total_students
                })
                secondary_data.append(data)

                camp_dict = {}
                camp_count = all_students.filter(counsel__program_interested='camp', created_at__gte=year, created_at__lt=next_year).exclude(status='terminated').count()
                camp_dict.update({'period':year, "camp_count":camp_count})
                camp_data.append(camp_dict)

                college_other_dict = {}
                college_count = all_students.filter(
                    counsel__program_interested='college',
                    created_at__gte=year,
                    created_at__lt=next_year).exclude(status='terminated').count()
                other_count = all_students.filter(
                    counsel__program_interested='not_specified',
                    created_at__gte=year,
                    created_at__lt=next_year).exclude(status='terminated').count()
                college_other_dict.update({'period':year, "college_count":college_count, "other_count":other_count})
                college_other_data.append(college_other_dict)

        else:
            return HttpResponse("Wrong id", status=400)

        return render(request, 'main/agent_info.html', {
            "found_agent":found_agent,
            'all_agents':all_agents,
            'program_list':program_list,
            'contact_infos':contact_infos,
            'contact_infos_count':contact_infos_count,
            'rest_contact_range':rest_contact_range,
            'relationship_histories':relationship_histories,
            'secondary_data':secondary_data,
            'camp_data':camp_data,
            'college_other_data':college_other_data,
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

            elif data.get('type') == 'contact_information':

                try:
                    found_agent = agent_models.AgencyHead.objects.get(pk=agent_id)
                except agent_models.AgencyHead.DoesNotExist:
                    return HttpResponse("Wrong Agent ID", status=400)

                if data.getlist('info_id'):

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

            elif data.get('type') == 'relationship_history':

                if data.get('relationship_history_id'):

                    try:
                        found_history = agent_models.AgentRelationshipHistory.objects.get(id=int(data.get('relationship_history_id')))
                    except agent_models.AgentRelationshipHistory.DoesNotExist:
                        return HttpResponse('Wrong history id', status=400)

                    user = request.user.first_name + request.user.last_name
                    found_history.writer=user
                    found_history.name=data.get('name')
                    found_history.date=data.get('date')
                    found_history.location=data.get('location')
                    found_history.category=data.get('category')
                    found_history.priority=int(data.get('priority'))
                    found_history.comment=data.get('comment')
                    found_history.save()

                    return HttpResponseRedirect(request.path_info)
                else:
                    try:
                        found_agent = agent_models.AgencyHead.objects.get(pk=agent_id)
                    except agent_models.AgencyHead.DoesNotExist:
                        return HttpResponse("Wrong Agent ID", status=400)
                    user = request.user.first_name + request.user.last_name
                    history = agent_models.AgentRelationshipHistory(
                        head=found_agent,
                        writer=user,
                        name=data.get('name'),
                        date=data.get('date'),
                        location=data.get('location'),
                        category=data.get('category'),
                        priority=int(data.get('priority')),
                        comment=data.get('comment'),
                    )
                    history.save()

                    return HttpResponseRedirect(request.path_info)

        else:
            return HttpResponse("Id not found", status=400)

        return HttpResponseRedirect('/agents')


@login_required(login_url='/accounts/login/')
def agent_history_get(request, history_id=None):

    if history_id:
        try:
            found_history = agent_models.AgentRelationshipHistory.objects.filter(id=int(history_id))
        except agent_models.AgentRelationshipHistory.DoesNotExist:
            return HttpResponse('Wrong history id', status=400)

        data = serializers.serialize("json", found_history)
        return HttpResponse(data, content_type="application/json")

    else:
        return HttpResponse('No history id', status=400)

class AgentsBranchUpdateView(LoginRequiredMixin, View):

    def get(self, request, agent_id=None):

        if agent_id:

            try:
                found_agent_branch = agent_models.Agency.objects.get(pk=agent_id)
            except agent_models.Agency.DoesNotExist:
                return HttpResponse("Wrong Agent ID", status=400)

            all_agents = agent_models.AgencyHead.objects.all()
            all_agent_branches = agent_models.Agency.objects.all()

            agent_branch_programs = agent_models.AgencyBranchProgram.objects.filter(branch=found_agent_branch)
            program_list = []
            if agent_branch_programs:
                for program in agent_branch_programs:
                    program_list.append(program.program)

        else:
            return HttpResponse("Wrong id", status=400)

        return render(request, 'main/agent_branch_info.html', {
            "found_agent_branch":found_agent_branch,
            'all_agents':all_agents,
            'all_agent_branches':all_agent_branches,
            'program_list':program_list,
        })

    def post(self, request, agent_id=None):

        if not request.user.type == 'bge_admin' or request.user.type == 'bge_team' or request.user.type == 'bge_branch_admin':
            return HttpResponse("You don't have permissions", status=400)

        data = request.POST

        if agent_id:

            try:
                found_agent_branch = agent_models.Agency.objects.get(pk=agent_id)
            except agent_models.Agency.DoesNotExist:
                return HttpResponse("Wrong Agent Branch ID", status=400)

            try:
                found_head = agent_models.AgencyHead.objects.get(pk=int(data.get('agent_head')))
            except agent_models.AgencyHead.DoesNotExist:
                return HttpResponse('Wrong Head Id', status=400)

            found_agent_branch.location = data.get('location')
            found_agent_branch.head = found_head
            found_agent_branch.capacity_students = data.get('capacity_students')
            found_agent_branch.commission = data.get('commission')
            found_agent_branch.promotion = data.get('promotion')
            found_agent_branch.others = data.get('others')
            found_agent_branch.comment = data.get('comment')
            found_agent_branch.save()

            if data.getlist('program'):
                found_programs = agent_models.AgencyBranchProgram.objects.filter(branch=found_agent_branch)
                found_programs.delete()
                for program in data.getlist('program'):
                    agent_program = agent_models.AgencyBranchProgram(
                        branch=found_agent_branch,
                        program=program
                    )
                    agent_program.save()

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


class AccountingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        all_students = student_models.Student.objects.filter(status='registered')
        all_branches = models.BgeBranch.objects.all()
        overdue_students = all_students.filter(accounting__balance__lt=0).distinct()

        return render(request, 'main/accounting.html', {
            'all_students':all_students,
            'all_branches':all_branches,
            'overdue_students':overdue_students,
        })

class AccountingStudentView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, student_id):

        if student_id:

            all_students = student_models.Student.objects.filter(status='registered')
            all_branches = models.BgeBranch.objects.all()
            overdue_students = all_students.filter(accounting__balance__lt=0).distinct()
            found_student = student_models.Student.objects.get(id=int(student_id))

        else:
            return HttpResponse('No Student id', status=400)

        return render(request, 'main/accounting.html', {
            'all_students':all_students,
            'all_branches':all_branches,
            'overdue_students':overdue_students,
            'found_student':found_student,
        })

    def post(self, request, student_id=None):

        data = request.POST

        if student_id:

            found_student = student_models.Student.objects.get(id=int(student_id))
            accounting = student_models.StudentAccounting(
                student=found_student,
                description=data.get('description'),
                expense=data.get('expense'),
                due_date=data.get('due_date'),
                payment=int(data.get('payment')) if data.get('payment') else None,
                paid_date=data.get('paid_date'),
                balance=int(data.get('balance')) if data.get('balance') else None,
            )
            accounting.save()

            if accounting.expense and accounting.payment:
                accounting.balance = int(accounting.payment) - int(accounting.expense)
                accounting.save()

            accounting_form = forms.AccountingForm(request.POST, request.FILES)
            if accounting_form.is_valid():
                accounting.invoice = accounting_form.cleaned_data['invoice']
                accounting.save()

            if data.get('delete_invoice'):
                found_accounting = student_models.StudentAccounting.objects.get(id=int(data.get('delete_invoice')))
                found_accounting.delete()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect(request.path_info)
