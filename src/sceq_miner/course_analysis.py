from utils import *
from parse_txt import parse_all

def question_entropy(question_dict):
    """Given a dictionary for a question, compute the entropy of the
    responses.  This should be a measure of the 'controversiality of
    the question.'"""
    if question_dict == {}:
        return 0
    counts = [question_dict[val] for val in "na nr one two three four five".split()]
    ps = normalize(counts)
    return h(ps)

def instructor_average(instructor_name,ds):
    """Return the mean overall teaching effectiveness for the instructor"""
    main_q = 'How would you grade the overall teaching effectiveness'
    return mean([d['questions'][main_q]['mean']
                for d in ds
                if (d['instructor'] == instructor_name
                    and 'mean' in d['questions'][main_q])])

def mean_exp_grade(d):
    scale = {"A":4,"B":3,"C":2,"D":1,"F":0,"I":0,"P":2}
    return (sum(d["num_exp_%s" % grade]*scale[grade] for grade in "ABCDFIP")
            /float(d['num_questionnaires']))

def effectiveness(d):
    return mean_val(d,main_q)

def mean_val(d,q):
    responses = "one two three four five".split()
    scores = {"one":1,"two":2,"three":3,"four":4,"five":5}
    try:
        return (sum([d['questions'][q][val]*scores[val] for val in responses])
                /float(d['num_questionnaires']))
    except:
        return None
    
def __main__():
    ds = parse_all()
    instructors = set(d['instructor'] for d in final_ds)

    
def explore_response_correlations():
    all_questions = list(set(concat(d['questions'].keys() for d in ds)))
    mean_responses = [[mean_val(d,q) for d in ds] for q in all_questions]
    exp_grades = [mean_exp_grade(d) for d in ds]
    effs = mean_responses[all_questions.index(main_q)]
    eff_ranked_qs = [(q,spearmanr(effs,mean_response))
                     for (q,mean_response) in zip(all_questions,mean_responses)]
    exp_ranked_qs = [(q,spearmanr(exp_grades,response))
                     for (q,response) in zip(all_questions,mean_responses)]
    eff_ranked_qs.sort(key=lambda(q,(t,p)):t,reverse=True)
    exp_ranked_qs.sort(key=lambda(q,(t,p)):t,reverse=True)

def matching_sections(dept,course_num,ds):
    return filter(lambda d:d['dept']==dept and d['course_num']==course_num,ds)

def get_instructors(ds):
    return list(set([d['instructor'] for d in ds]))

def major_ratio(d):
    return d['maj']/float(d['num_questionnaires'])

def do_majors_like_their_classes_more_exp():
    courses = list(set([(d['dept'],d['course_num']) for d in ds]))
    spears = []
    for course in courses:
        dept,course_num = course
        sections = matching_sections(dept,course_num,ds)
        effs = map(effectiveness,sections)
        major_ratios = map(major_ratio,sections)
        if len(effs) > 2:
            spears.append(spearmanr(effs,major_ratios))
    return spears
        
        
    major_percentages = map(major_percentage,ds)
    all_questions = list(set(concat(d['questions'].keys() for d in ds)))
    mean_responses = [[mean_val(d,q) for d in ds] for q in all_questions]
    effs = mean_responses[all_questions.index(main_q)]
    plt.scatter(*transpose(filter(lambda(x,y):not(x is None or y is None),
                                  zip(major_percentages,effs))))
    print spearmanr(major_percentages,effs)
    plt.show()
    
