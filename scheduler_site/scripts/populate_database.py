import pickle
import sys
import random
import schedulerapp.models as models

def populate_db():
    # read pickle
    print 'reading pickle ..',
    sys.stdout.flush()
    sections = pickle.load(open("final_dicts.pkl"))
    print 'done'
    for i,sec in enumerate(sections):
        print 'processing section %d' % i
        # check course is already in db
        course,_ = models.Course.objects.get_or_create(dept=sec['dept'],
                                                       number=sec['course_num'],
                                                       title=sec['title'],
                                                       )
        print 'course'
        instructor,_ = models.Professor.objects.get_or_create(name=sec['instructor'])
        print 'instructor'
        evaluation = models.Evaluation.objects.create()
        print 'evaluation'
        section = models.Section.objects.create(course=course,
                                                semester=sec['semester'],
                                                year=sec['year'],
                                                courseid=random.randint(1, 10000),
                                                evaluation=evaluation)
        section.save()
        print 'section'
        


def run():
    populate_db()
