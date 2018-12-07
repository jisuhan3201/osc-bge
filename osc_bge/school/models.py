from django.db import models
from osc_bge.bge import models as bge_models
from osc_bge.users import models as user_models
import os
import datetime



# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

# def set_filename_format(now, instance, filename):
#
#     return "{schoolname}".format(
#         schoolname=instance.name,
#         )
#
# def school_directory_path(instance, filename):
#     """
#     image upload directory setting e.g)
#     school/{year}/{month}/{day}/{schoolname}/{filename}
#     images/2016/7/12/schoolname/schoolname-2016-07-12-158859.png
#     """
#     now = datetime.datetime.now()
#     path = "school/{schoolname}/{filename}".format(
#         schoolname=instance.name,
#         filename=set_filename_format(now, instance, filename),
#     )
#     return path


class School(TimeStampedModel):

    TYPE_CHOICES = (
        ('secondary', 'Secondary'),
        ('college', 'Collge'),
    )
    TERM_CHOICES = (
        ('fall', 'Fall'),
        ('spring', 'Spring')
    )
    COUNTRY_CHOICES = (
        ('us', 'US'),
        ('ca', 'CA'),
        ('uk', 'UK'),
        ('au', 'AU'),
        ('nz', 'NZ'),
    )
    PROVIDER_CHOICES = (
        ('bge', 'BGE'),
        ('other_providers', 'Other-Provider'),
    )

    name = models.CharField(max_length=80, null=True)
    type = models.CharField(max_length=80, null=True, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='schools', null=True, blank=True)
    partnership = models.IntegerField(null=True, blank=True)
    provider = models.CharField(max_length=80, null=True, blank=True, choices=PROVIDER_CHOICES)
    provider_branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True, related_name="schools")
    admission_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name='admission_coordi')
    school_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name='school_coordi')
    term = models.CharField(max_length=80, null=True, blank=True, choices=TERM_CHOICES)
    transfer = models.BooleanField(default=False)
    country = models.CharField(max_length=80, null=True, choices=COUNTRY_CHOICES)
    address = models.CharField(max_length=140, null=True, blank=True)
    area_description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=140, null=True, blank=True)
    web_url = models.CharField(max_length=140, null=True, blank=True)
    founded = models.CharField(max_length=80, null=True, blank=True)
    religion = models.CharField(max_length=80, null=True, blank=True)
    number_students = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return "{}".format(self.name)


class Secondary(TimeStampedModel):

    STUDENT_BODY_CHOICES = (
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('coed', 'Coed'),
    )
    STATE_CHOICES = (
        ('ma', 'MA'),
        ('ct', 'CT'),
        ('nj', 'NJ'),
        ('pa', 'PA'),
        ('dc', 'DC'),
        ('ca', 'CA'),
        ('fl', 'FL'),
        ('tx', 'TX'),
        ('others', 'Others'),
    )

    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True, related_name="secondary")
    grade_start = models.IntegerField(null=True, blank=True)
    grade_end = models.IntegerField(null=True, blank=True)
    accept_12_grade = models.BooleanField(default=False)
    application_fee = models.IntegerField(null=True, blank=True)
    program_fee = models.IntegerField(null=True, blank=True)
    admission_requirements = models.TextField(null=True, blank=True)
    toefl_requirement = models.IntegerField(null=True, blank=True)
    admission_documents = models.TextField(null=True, blank=True)
    selling_point = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=80, null=True, choices=STATE_CHOICES)
    student_body = models.CharField(max_length=80, choices=STUDENT_BODY_CHOICES, null=True, blank=True)
    international_students = models.IntegerField(null=True, blank=True)
    esl = models.BooleanField(default=False)
    student_teach_ratio = models.CharField(max_length=80, null=True, blank=True)
    class_size = models.CharField(max_length=80, null=True, blank=True)
    uniform = models.BooleanField(default=False)
    college_acceptance_rate = models.CharField(max_length=80, null=True, blank=True)
    avg_sat = models.CharField(max_length=80, null=True, blank=True)
    number_honor_courses = models.CharField(max_length=80, null=True, blank=True)
    list_honor_courses = models.TextField(null=True, blank=True)
    number_ap_courses = models.CharField(max_length=80, null=True, blank=True)
    list_ap_courses = models.TextField(null=True, blank=True)
    number_clubs = models.CharField(max_length=80, null=True, blank=True)
    number_sports = models.CharField(max_length=80, null=True, blank=True)
    facilities = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.school)


class College(TimeStampedModel):

    LOCATION_CHOICE = (
        ('ne', 'NE'),
        ('se', 'SE'),
        ('mw', 'MW'),
        ('w', 'W'),
    )
    NATIONAL_CHOICE = (
        ('es', 'Good-Engineering'),
        ('bs', 'Good-Business'),
        ('as', 'Good-Art'),
        ('ss', 'Good-Science'),
        ('lac', 'Liveral-Arts-College'),
        ('lc', 'Local-Collge'),
        ('pu', 'Pathway-University'),
    )
    SETTING_CHOICE = (
        ('urban', 'Urban'),
        ('Suburban', 'Suburban'),
    )

    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True, related_name="college")
    toefl_requirement = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=80, null=True, choices=LOCATION_CHOICE)
    national_univ = models.CharField(max_length=80, null=True, choices=NATIONAL_CHOICE)
    tuition = models.IntegerField(null=True, blank=True)
    room_and_board = models.IntegerField(null=True, blank=True)
    sat_act_requirement = models.CharField(max_length=80, null=True, blank=True)
    sat_25 = models.CharField(max_length=80, null=True, blank=True)
    sat_75 = models.CharField(max_length=80, null=True, blank=True)
    gpa_requirement = models.CharField(max_length=80, null=True, blank=True)
    ranking = models.CharField(max_length=80, null=True, blank=True)
    setting = models.CharField(max_length=80, null=True, blank=True, choices=SETTING_CHOICE)
    asian_percent = models.IntegerField(null=True, blank=True)
    high_school_10 = models.IntegerField(null=True, blank=True)
    full_time_faculty = models.IntegerField(null=True, blank=True)
    student_faculty_ration = models.CharField(max_length=80, null=True, blank=True)
    class_under_20 = models.IntegerField(null=True, blank=True)
    ed_ea_deadline = models.DateField(null=True, blank=True)
    ed_ea_noticedate = models.DateField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    degree_offered = models.CharField(max_length=80, null=True, blank=True)
    most_popular_majors = models.CharField(max_length=255, null=True, blank=True)
    selling_point = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.school)


def set_filename_format(now, instance, filename):

    return "{schoolname}-{microsecond}".format(
        schoolname=instance.name,
        microsecond=now.microsecond,
        )

def school_directory_path(instance, filename):
    now = datetime.datetime.now()
    path = "school/{schoolname}/{filename}".format(
        schoolname=instance.name,
        filename=set_filename_format(now, instance, filename),
    )
    return path


class SchoolTypes(TimeStampedModel):

    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name="school_type")
    type = models.CharField(max_length=80, null=True)

class SchoolPhotos(TimeStampedModel):

    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name="school_photo")
    photo = models.ImageField(upload_to=school_directory_path, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.school)
