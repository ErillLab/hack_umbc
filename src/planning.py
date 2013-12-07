"""
Given a list of course constraints and time constraints, find a
schedule satisfying those constraints.
"""
from itertools import product

def matching_sections(dept,course_num,avail_courses):
    return filter(lambda course:course.dept==dept and
                  course.number==course_num,avail_courses)

def plan(course_constraints,time_constraints,avail_courses):
    sectionses = [matching_sections(course.dept,course.number,avail_courses)
                  for course in course_constraints]
    possible_schedules = product(*sectionses)
    schedules = []
    for possible_schedule in possible_schedules:
        if all(time_constraint(cls)
               for time_constraint,cls
               in product(time_constraints, possible_schedules)):
            schedules.append(possible_schedule)
    return schedules

def make_time_constraint(day,(hr,minutes),before_or_not):
    """Forbid sections on day before or after time.  Return a function
    which returns true if constraint is satisfied by a given section"""
    hr,minutes = time
    def satisfies(section):
        sessions = section.session_set.all()
        if before_or_not: #if constraint forbids classes before given time
            return all(session.day_of_the_week != day or
                       session.time_start_hr > hr or
                       (session.time_start_hr == hr and
                        session.time_start_min > minutes))
        else: #if constraint forbids classes after given time
            return all(session.day_of_the_week != day or
                       session.time_start_hr < hr or
                       (session.time_start_hr == hr and
                        session.time_start_min < minutes))
    return satisfies

def no_classes_before((hr,minutes),day):
    return make_time_constraint(day,(hr,minutes),before_or_not=True)

def no_classes_after((hr,minutes),day):
    return make_time_constraint(day,(hr,minutes),before_or_not=True)
            
    
