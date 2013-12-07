import pickle
import sys
import random
import schedulerapp.models as models
import string

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
        instructor,_ = models.Professor.objects.get_or_create(name=sec['instructor'])
        evaluation = models.Evaluation.objects.create()

        section = models.Section.objects.create(course=course,
                                                semester=sec['semester'],
                                                yr=sec['year'],
                                                courseid=random.randint(1, 10000),
                                                evaluation=evaluation,
                                                professor=instructor,
                                                #section=sec['section'],
                                                )


        def create_session():
            time_start_min = random.choice([0, 15, 30, 45])
            time_start_hr = random.randint(8, 19)
            print time_start_min
            print time_start_hr
            return models.Session.objects.create(
                day_of_the_week = random.choice(models.Session.DAYS_OF_THE_WEEK)[0],
                time_start_hr = time_start_hr,
                time_start_min = time_start_min,
                time_end_hr = time_start_hr + 2,
                time_end_min = time_start_min,
                room = (random.choice(string.letters) +
                        random.choice(string.letters) +
                        str(random.randint(1,999))),
                section=section,
                )

        session_a = create_session()
        session_b = create_session()


def run():
    populate_db()
