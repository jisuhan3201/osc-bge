from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.school import models as school_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class ParentInfo(TimeStampedModel):

    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(null=True, max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    wechat = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Student(TimeStampedModel):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    STATUS_CHOICES = (
        ('unregistered', 'Unregistered'),
        ('registered', 'Registered'),
        ('transferred', 'Transferred'),
        ('terminated', 'Terminated'),
    )

    agency_admin = models.ForeignKey(user_models.AgencyAdminUser, on_delete=models.SET_NULL, null=True)
    counselor = models.ForeignKey(user_models.Counselor, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    parent_info = models.ForeignKey(ParentInfo, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    phone = models.CharField(null=True, max_length=140, blank=True)
    email = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=140, null=True, blank=True)
    wechat = models.CharField(null=True, max_length=140, blank=True)
    status = models.CharField(null=True, max_length=80, blank=True, default='unregistered', choices=STATUS_CHOICES)
    nationality = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class StudentHistory(TimeStampedModel):

    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True, related_name='student_history')
    current_grade = models.CharField(max_length=80, null=True, blank=True)
    current_school = models.CharField(max_length=140, null=True, blank=True)
    apply_grade = models.CharField(null=True, max_length=80, blank=True)
    eng_level = models.CharField(max_length=140, null=True, blank=True)
    toefl = models.CharField(max_length=80, null=True, blank=True)
    toefljr = models.CharField(max_length=80, null=True, blank=True)
    gpa = models.CharField(max_length=80, null=True, blank=True)
    sat = models.CharField(max_length=80, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.student, self.gpa)


class StudentReport(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='report')
    counselor = models.ForeignKey(user_models.Counselor, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    reported_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)


class CurrentStudentReview(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    student = models.CharField(max_length=80, null=True, blank=True)
    grade = models.CharField(max_length=80, null=True, blank=True)
    homecity = models.CharField(max_length=80, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class GraduateStudentReview(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    student = models.CharField(max_length=80, null=True, blank=True)
    attended = models.CharField(max_length=80, null=True, blank=True)
    init_eng = models.CharField(max_length=80, null=True, blank=True)
    gpa_china = models.CharField(max_length=80, null=True, blank=True)
    toefl = models.CharField(max_length=80, null=True, blank=True)
    gpa = models.CharField(max_length=80, null=True, blank=True)
    sat_act = models.CharField(max_length=80, null=True, blank=True)
    activities = models.CharField(max_length=80, null=True, blank=True)
    college = models.CharField(max_length=80, null=True, blank=True)
    major = models.CharField(max_length=80, null=True, blank=True)


class StudentMonthlyReport(TimeStampedModel):

    STATUS_CHOICES = (
        ('incomplete', 'Incomplete'),
        ('submitted', 'Submitted'),
        ('manager_confirmed', 'Manager Confirmed'),
        ('send_to_agent', 'Send to Agent'),
        ('agent_confirmed', 'Agent Confirmed'),
    )

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='monthly_report')
    counseling_date = models.CharField(max_length=80, null=True, blank=True)
    manager_confirm_date = models.CharField(max_length=80, null=True, blank=True)
    school_year = models.CharField(max_length=80, null=True, blank=True)
    grade = models.CharField(max_length=80, null=True, blank=True)
    send_to_agent_date = models.CharField(max_length=80, null=True, blank=True)
    college_plan = models.TextField(null=True, blank=True)
    eng9h_lv = models.CharField(max_length=80, null=True, blank=True)
    eng9h_tg = models.CharField(max_length=80, null=True, blank=True)
    eng9h_current = models.CharField(max_length=80, null=True, blank=True)
    precal_lv = models.CharField(max_length=80, null=True, blank=True)
    precal_tg = models.CharField(max_length=80, null=True, blank=True)
    precal_current = models.CharField(max_length=80, null=True, blank=True)
    bioh_lv = models.CharField(max_length=80, null=True, blank=True)
    bioh_tg = models.CharField(max_length=80, null=True, blank=True)
    bioh_current = models.CharField(max_length=80, null=True, blank=True)
    chemh_lv = models.CharField(max_length=80, null=True, blank=True)
    chemh_tg = models.CharField(max_length=80, null=True, blank=True)
    chemh_current = models.CharField(max_length=80, null=True, blank=True)
    geo_lv = models.CharField(max_length=80, null=True, blank=True)
    geo_tg = models.CharField(max_length=80, null=True, blank=True)
    geo_current = models.CharField(max_length=80, null=True, blank=True)
    cs_lv = models.CharField(max_length=80, null=True, blank=True)
    cs_tg = models.CharField(max_length=80, null=True, blank=True)
    cs_current = models.CharField(max_length=80, null=True, blank=True)
    sp_lv = models.CharField(max_length=80, null=True, blank=True)
    sp_tg = models.CharField(max_length=80, null=True, blank=True)
    sp_current = models.CharField(max_length=80, null=True, blank=True)
    orch_lv = models.CharField(max_length=80, null=True, blank=True)
    orch_tg = models.CharField(max_length=80, null=True, blank=True)
    orch_current = models.CharField(max_length=80, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    target_gpa = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    eng_skill = models.TextField(null=True, blank=True)
    toefl = models.CharField(max_length=80, null=True, blank=True)
    toefl_reading = models.CharField(max_length=80, null=True, blank=True)
    toefl_listening = models.CharField(max_length=80, null=True, blank=True)
    toefl_speaking = models.CharField(max_length=80, null=True, blank=True)
    toefl_writing = models.CharField(max_length=80, null=True, blank=True)
    toefl_total = models.CharField(max_length=80, null=True, blank=True)
    toefl_target = models.CharField(max_length=80, null=True, blank=True)
    toefl_next_test_date = models.CharField(max_length=80, null=True, blank=True)
    sat = models.CharField(max_length=80, null=True, blank=True)
    sat_evb_reading_writing = models.CharField(max_length=80, null=True, blank=True)
    sat_math = models.CharField(max_length=80, null=True, blank=True)
    sat_total = models.CharField(max_length=80, null=True, blank=True)
    sat_target = models.CharField(max_length=80, null=True, blank=True)
    sat_next_test_date = models.CharField(max_length=80, null=True, blank=True)
    act = models.CharField(max_length=80, null=True, blank=True)
    act_eng = models.CharField(max_length=80, null=True, blank=True)
    act_math = models.CharField(max_length=80, null=True, blank=True)
    act_reading = models.CharField(max_length=80, null=True, blank=True)
    act_sci = models.CharField(max_length=80, null=True, blank=True)
    act_composition_score = models.CharField(max_length=80, null=True, blank=True)
    act_target = models.CharField(max_length=80, null=True, blank=True)
    act_next_test_date = models.CharField(max_length=80, null=True, blank=True)
    ap_tests = models.TextField(null=True, blank=True)
    sat_subjects_tests = models.TextField(null=True, blank=True)
    test_prep = models.TextField(null=True, blank=True)
    activities = models.TextField(null=True, blank=True)
    community_services = models.TextField(null=True, blank=True)
    agenda = models.TextField(null=True, blank=True)
    comment2 = models.TextField(null=True, blank=True)
    objective_assignment = models.TextField(null=True, blank=True)
    payment_desc = models.CharField(max_length=255, null=True, blank=True)
    payment_expense = models.CharField(max_length=80, null=True, blank=True)
    payment_due_date = models.CharField(max_length=80, null=True, blank=True)
    payment_payment = models.CharField(max_length=80, null=True, blank=True)
    payment_paid_date = models.CharField(max_length=80, null=True, blank=True)
    payment_balance = models.CharField(max_length=80, null=True, blank=True)
    payment_invoice = models.CharField(max_length=80, null=True, blank=True)
    submit_date = models.DateField(null=True, blank=True)
    agent_confirmed = models.DateField(null=True, blank=True)
    report_to_parent = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=80, null=True, blank=True, choices=STATUS_CHOICES)

    def  __str__(self):
        return "{}".format(self.student)


class StudentCommunicationLog(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=80, null=True, blank=True)
    priority = models.CharField(max_length=80, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
