from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

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

    name = models.CharField(max_length=80, null=True)
    type = models.CharField(max_length=80, null=True, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='school', null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True, choices=COUNTRY_CHOICES)
    address = models.CharField(max_length=140, null=True, blank=True)
    contacts = models.CharField(max_length=140, null=True, blank=True)
    founded = models.CharField(max_length=80, null=True, blank=True)
    transfer = models.BooleanField(default=False)
    term = models.CharField(max_length=80, null=True, blank=True, choices=TERM_CHOICES)
    number_students = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Secondary(TimeStampedModel):

    DETAIL_TYPE = (
        ('day_school', 'Day-School'),
        ('boarding_school', 'Boarding-School'),
        ('only_boy', 'Only-Boy'),
        ('only_girl', 'Only-Girl'),
        ('co_ed', 'Co-ed'),
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
    detail_type = models.CharField(max_length=80, choices=DETAIL_TYPE, null=True)
    total_fee = models.IntegerField(null=True, blank=True)
    grade_start = models.IntegerField(null=True, blank=True)
    grade_end = models.IntegerField(null=True, blank=True)
    toefl_requirement = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=80, null=True, choices=STATE_CHOICES)
    number_i18n_students = models.IntegerField(null=True, blank=True)
    program_fee = models.IntegerField(null=True, blank=True)
    number_ap_courses = models.IntegerField(null=True, blank=True)
    number_honor_courses = models.IntegerField(null=True, blank=True)
    number_clubs = models.IntegerField(null=True, blank=True)
    number_sports = models.IntegerField(null=True, blank=True)
    entry_requirement = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.school)

class College(TimeStampedModel):

    DETAIL_TYPE = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
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
    detail_type = models.CharField(max_length=80, choices=DETAIL_TYPE, null=True)
    toefl_requirement = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=80, null=True, choices=LOCATION_CHOICE)
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
