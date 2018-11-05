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

    name = models.CharField(max_length=255, null=True)
    lang = models.CharField(max_length=255, null=True)
    sort = models.CharField(max_length=255, choices=SCHOOL_SORT, null=True)
    is_partner = models.BooleanField()
    rank = models.IntegerField(null=True)
    grade = models.IntegerField(null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    student_num = models.IntegerField(null=True)
    itn_student_num = models.IntegerField(null=True)
    class_num = models.IntegerField(null=True)
    offered_grade = models.IntegerField(null=True)
    semester = models.CharField(max_length=255, null=True)
    religion = models.CharField(max_length=255, null=True)
    types = models.CharField(max_length=255, choices=SCHOOL_TYPE, null=True)
    setting = models.CharField(max_length=255, choices=SETTING_CHOICE, null=True)
    founded = models.DateField(null=True)
    is_uniform = models.BooleanField()
    is_boarding = models.BooleanField()
    is_communting = models.BooleanField()
    pop_major = models.CharField(max_length=255, null=True)
    rep_major = models.CharField(max_length=255, null=True)
    club_num = models.IntegerField(null=True)
    honor_process = models.CharField(max_length=255, null=True)
    ap_process = models.CharField(max_length=255, null=True)
    ibt = models.IntegerField(null=True)
    sat_avg = models.IntegerField(null=True)
    is_esl = models.BooleanField()
    gpa_request = models.BooleanField()
    sat_request = models.BooleanField()
    program_fee = models.DecimalField(max_digits=10, decimal_places=2)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    boarding_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tenpercent_ratio = models.IntegerField(null=True)
    ent_approve_ratio = models.IntegerField(null=True)
    asian_ratio = models.IntegerField(null=True)
    teacher_student_ratio = models.IntegerField(null=True)
    fulltime_teacher_ratio = models.IntegerField(null=True)
    under_twenty_ratio = models.IntegerField(null=True)
    collge_pass_ratio = models.IntegerField(null=True)
    sat25 = models.IntegerField(null=True)
    sat75 = models.IntegerField(null=True)
    end_ena_deadline = models.DateField(null=True)
    end_ena_noti = models.DateField(null=True)
    application_deadline = models.DateField(null=True)
    files = models.FileField(upload_to="school", null=True)

    def __str__(self):
        return "{}".format(self.name)
