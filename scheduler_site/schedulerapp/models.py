from django.db import models

# Create your models here.

class Course(models.Model):
    COURSE_TYPES = (
        ('lab', 'lab'),
        ('lecture', 'lecture')
    )
    dept = models.CharField(max_length=50)
    number = models.CharField(max_length=50) # course number
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField()
    prerequisites = models.ManyToManyField('Course',
                                           null=True,
                                           blank=True,
                                           related_name='prerequsites_all')
    corequsites = models.ManyToManyField('Course',
                                         null=True,
                                         blank=True,
                                         related_name='corequsites_all')

    def __unicode__(self):
        return u'%s%s %s' % (self.dept, self.number, self.title)

class Section(models.Model):
    course = models.ForeignKey('Course', null=False, blank=False)
    courseid = models.IntegerField() # section-specific course id
    professors = models.ManyToManyField('Professor',)
    semester = models.CharField(max_length=50)
    yr = models.IntegerField()
    evaluation = models.OneToOneField('Evaluation',
                                      null=False,
                                      blank=False)

    def __unicode__(self):
        return u'%s [section: %d]' % (self.course, self.courseid)

class Evaluation(models.Model):
    pass

class Professor(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s' % self.name
    
class Major(models.Model):
    courses = models.ManyToManyField(Course)

class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    sections = models.ManyToManyField(Section, blank=True, null=True)
    friends = models.ManyToManyField('Users', blank=True, null=True)
    majors = models.ManyToManyField(Major)


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

    def __unicode__(self):
        return u'%s %d:%d - %d:%d' % (self.day_of_the_week,
                                      self.time_start_hr,
                                      self.time_start_min,
                                      self.time_end_hr,
                                      self.time_end_min)
