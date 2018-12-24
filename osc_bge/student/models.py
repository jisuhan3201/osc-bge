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
        ('graduated', 'Graduated'),
        ('terminated', 'Terminated'),
    )

    agency_admin = models.ForeignKey(user_models.AgencyAdminUser, on_delete=models.SET_NULL, null=True)
    counselor = models.ForeignKey(user_models.Counselor, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True, related_name='students')
    parent_info = models.ForeignKey(ParentInfo, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images/students/', blank=True)
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
    manager_confirm_date = models.DateField(null=True, blank=True)
    school_year = models.CharField(max_length=80, null=True, blank=True)
    grade = models.CharField(max_length=80, null=True, blank=True)
    send_to_agent_date = models.DateField(null=True, blank=True)
    college_plan = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    target_gpa = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    eng_skill = models.TextField(null=True, blank=True)
    quater_gpa = models.CharField(max_length=80, null=True, blank=True)
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


class StudentAcademicRecord(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='academic_record')
    subject_number = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=80, null=True, blank=True)
    level = models.CharField(max_length=80, null=True, blank=True)
    target = models.CharField(max_length=80, null=True, blank=True)
    current = models.CharField(max_length=80, null=True, blank=True)
    current_grade = models.CharField(max_length=80, null=True, blank=True)


class StudentToeflHistory(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='toefl')
    toefl_date = models.DateField(null=True, blank=True)
    reading = models.CharField(max_length=80, null=True, blank=True)
    listening = models.CharField(max_length=80, null=True, blank=True)
    speaking = models.CharField(max_length=80, null=True, blank=True)
    writing = models.CharField(max_length=80, null=True, blank=True)
    total = models.CharField(max_length=80, null=True, blank=True)
    target = models.CharField(max_length=80, null=True, blank=True)
    next_test_date = models.CharField(max_length=80, null=True, blank=True)


class StudentSatHistory(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='sat')
    sat_date = models.DateField(null=True, blank=True)
    eb_reading_writing = models.CharField(max_length=80, null=True, blank=True)
    math = models.CharField(max_length=80, null=True, blank=True)
    total = models.CharField(max_length=80, null=True, blank=True)
    target = models.CharField(max_length=80, null=True, blank=True)
    next_test_date = models.CharField(max_length=80, null=True, blank=True)


class StudentActHistory(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='act')
    act_date = models.DateField(null=True, blank=True)
    eng = models.CharField(max_length=80, null=True, blank=True)
    math = models.CharField(max_length=80, null=True, blank=True)
    reading = models.CharField(max_length=80, null=True, blank=True)
    science = models.CharField(max_length=80, null=True, blank=True)
    cp_score = models.CharField(max_length=80, null=True, blank=True)
    target = models.CharField(max_length=80, null=True, blank=True)
    next_test_date = models.CharField(max_length=80, null=True, blank=True)


class StudentCommunicationLog(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=80, null=True, blank=True)
    priority = models.CharField(max_length=80, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class StudentAccounting(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='accounting')
    description = models.TextField(null=True, blank=True)
    expense = models.IntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    payment = models.IntegerField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)
