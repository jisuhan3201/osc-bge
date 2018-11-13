from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class School(TimeStampedModel):

    SCHOOL_SORT = (
        ('elementary', 'Elementary'),
        ('middle', 'Middle'),
        ('high', 'High'),
        ('college', 'College'),
    )

    SCHOOL_TYPE = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('only_male', 'Only-Male'),
        ('only_female', 'Only-Female'),
        ('Coed', 'Coed'),
    )

    SETTING_CHOICE = (
        ('urban', 'Urban'),
        ('suburban', 'SubUrban'),
    )

    name = models.CharField(max_length=140, null=True)
    lang = models.CharField(max_length=80, null=True)
    sort = models.CharField(max_length=80, choices=SCHOOL_SORT, null=True)
    is_partner = models.BooleanField()
    rank = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True)
    state = models.CharField(max_length=80, null=True, blank=True)
    address = models.CharField(max_length=140, null=True, blank=True)
    student_num = models.IntegerField(null=True, blank=True)
    itn_student_num = models.IntegerField(null=True, blank=True)
    class_num = models.IntegerField(null=True, blank=True)
    offered_grade = models.IntegerField(null=True, blank=True)
    semester = models.CharField(max_length=80, null=True, blank=True)
    religion = models.CharField(max_length=80, null=True, blank=True)
    types = models.CharField(max_length=80, choices=SCHOOL_TYPE, null=True, blank=True)
    setting = models.CharField(max_length=80, choices=SETTING_CHOICE, null=True, blank=True)
    founded = models.DateField(null=True, blank=True)
    is_uniform = models.BooleanField()
    is_boarding = models.BooleanField()
    is_communting = models.BooleanField()
    pop_major = models.CharField(max_length=140, null=True, blank=True)
    rep_major = models.CharField(max_length=140, null=True, blank=True)
    club_num = models.IntegerField(null=True, blank=True)
    honor_process = models.CharField(max_length=140, null=True, blank=True)
    ap_process = models.CharField(max_length=140, null=True, blank=True)
    ibt = models.IntegerField(null=True, blank=True)
    sat_avg = models.IntegerField(null=True, blank=True)
    is_esl = models.BooleanField()
    gpa_request = models.BooleanField()
    sat_request = models.BooleanField()
    program_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    boarding_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tenpercent_ratio = models.IntegerField(null=True, blank=True)
    ent_approve_ratio = models.IntegerField(null=True, blank=True)
    asian_ratio = models.IntegerField(null=True, blank=True)
    teacher_student_ratio = models.IntegerField(null=True, blank=True)
    fulltime_teacher_ratio = models.IntegerField(null=True, blank=True)
    under_twenty_ratio = models.IntegerField(null=True, blank=True)
    college_pass_ratio = models.IntegerField(null=True, blank=True)
    sat25 = models.IntegerField(null=True, blank=True)
    sat75 = models.IntegerField(null=True, blank=True)
    end_ena_deadline = models.DateField(null=True, blank=True)
    end_ena_noti = models.DateField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    files = models.FileField(upload_to="school", null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)
