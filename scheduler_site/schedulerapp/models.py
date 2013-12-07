from django.db import models

# Create your models here.

class Session(models.Model):
    DAYS_OF_THE_WEEK = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )
    day_of_the_week = models.CharField(max_length=50, choices=DAYS_OF_THE_WEEK)
    time_start_hr = models.IntegerField()
    time_start_min = models.IntegerField()
    time_end_hr = models.IntegerField()
    time_end_min = models.IntegerField()
    room = models.CharField(max_length=50)
    section = models.ForeignKey(Section)

class Course(models.Model):
    COURSE_TYPES = (
        ('lab', 'lab'),
        ('lecture', 'lecture')
    )
    dept = models.CharField(max_length=50)
    number = models.IntegerField() # course number
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField()
    prerequisites = models.ManyToMany(Course)
    corequsites = models.ManyToMany(Course)

class Section(models.Model):
    SEMESTERS = (
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    )
    course_id = models.IntegerField() # section-specific course id
    professor = models.ManyToManyField(Professor)
    semester = models.CharField(max_length=50, choices=SEMESTERS)
    year = models.IntegerField()
    evaluation = models.OneToOneField(Evaluation)

class Evaluation(models.Model):
    pass

class Professor(models.Model):
    name = models.CharField(max_length=128)
    
class Major(models.Model):
    courses = models.ManyToManyField(Course)

class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    sections = models.ManyToManyField(Section)
    friends = models.ManyToManyField(Users)
    majors = models.ManyToManyField(Major)

