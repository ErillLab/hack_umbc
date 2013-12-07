from utils import *
from parse_txt import parse_all
from matplotlib import pyplot as plt
from matplotlib.mlab import PCA
import numpy as np

questions = sorted(list(set(concat(d['questions'].keys() for d in ds))))
main_q = 'How would you grade the overall teaching effectiveness'

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

def courses_by_instructor(instructor,ds):
    return [d for d in ds if d['instructor'] == instructor]

def instructor_matrix(ds):
    """Return a matrix whose rows are instructors and whose columns
    are mean scores for a given question over all courses taught by
    that instructor"""
    instructors = set(d['instructor'] for d in ds)
    course_lookup = {ins:courses_by_instructor(ins,ds) for ins in instructors}
    matrix = [[mean([mean_val(d,q) for d in course_lookup[ins]
                    if q in d['questions']])
               for q in questions]
              for ins in instructors]
    return matrix

def pca_instructor_matrix(ds):
    matrix = instructor_matrix(ds)
    # replace Nones with column_means
    trans_matrix = transpose(matrix)
    col_means = map(lambda col:mean(filter(lambda x:not x is None,col)),
                    trans_matrix)
    trans_matrix_filled = [[0 for val in col] for col in trans_matrix]
    # center by subtracting column means, missing vals set to zero
    for j,col in enumerate(trans_matrix):
        for i, val in enumerate(col):
            if val:
                trans_matrix_filled[j][i] = val - col_means[j]
            else:
                trans_matrix_filled[j][i] = 0
    matrix_filled = transpose(trans_matrix_filled)
    X = np.matrix(matrix_filled)
    pca_result = PCA(X)
    eigenvectors = [v.tolist()[0] for v in pca_result.Wt]
    
def interpret_eigenvectors(eigenvector):
    qes = zip(questions,eigenvector)
    qes.sort(key=lambda(q,e):e,reverse=True)
    return qes
    
def mean_exp_grade(d):
    scale = {"A":4,"B":3,"C":2,"D":1,"F":0,"I":0,"P":2}
    return (sum(d["num_exp_%s" % grade]*scale[grade] for grade in "ABCDFIP")
            /float(d['num_questionnaires']))

def cancelability(d):
    main_q = 'How many times was class cancelled'
    return mean_val(d, main_q)

def approachableness(d):
    return mean_eigenscore(d,eigen0)

def fairness(d):
    return mean_eigenscore(d,eigen1)

def engagingness(d):
    return mean_eigenscore(d,eigen2)

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

def mean_eigenscore(d,eigenvector):
    """Compute the transformed instructor score along the ith eigenvector"""
    return sum(filter(lambda x:not x is None,
                      [mean_val(d,q)*eigenvector[i] if mean_val(d,q) else None
                      for i,q in enumerate(questions)]))
    
    
def explore_correlations(scores):
    mean_responses = [[mean_val(d,q) for d in ds] for q in questions]
    #exp_grades = [mean_exp_grade(d) for d in ds]
    #effs = mean_responses[questions.index(main_q)]
    ranked_qs = [(q,spearmanr(scores,mean_response))
                     for (q,mean_response) in zip(questions,mean_responses)]
    # exp_ranked_qs = [(q,spearmanr(exp_grades,response))
    #                  for (q,response) in zip(all_questions,mean_responses)]
    # eff_ranked_qs.sort(key=lambda(q,(t,p)):t,reverse=True)
    ranked_qs.sort(key=lambda(q,(t,p)):t,reverse=True)
    return ranked_qs

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
    
def __main__():
    ds = parse_all()
    instructors = set(d['instructor'] for d in final_ds)
    eigenvectors = pca_instructor_matrix(ds)

eigen0 = [0.2045866757567234, 0.11813598031399564, -0.03262520277992126, 0.21931806255465452, 0.11727402572662901, -0.040125936746312235, 0.11580517840805195, 0.17334199189843572, 0.1695317057514744, 0.17092317041136906, 0.16186119437260163, 0.16113060173579685, 0.04187801096600372, 0.16002804691283498, 0.16667622759814685, 0.17150623880721563, -0.035709365338788795, 0.12877305549712942, 0.18591073494680546, -0.04125079612243615, 0.19497569963870243, 0.17206781381755343, 0.2193197346292979, 0.17264730270798043, 0.21595898382522144, -0.033667587818151615, 0.2158896216779336, 0.21157000644722548, 0.16455185683396015, 0.13463600025267786, 0.16115863866938804, 0.11843009334491164, 0.17191801193982134, 0.1817396254183546, 0.218381596796727, 0.20243860092004756, 0.19522194802521872, 0.16780973901253998]
eigen1 = [0.19699426957578173, -0.19492046441776756, -0.20845697022445134, 0.08112912423417806, 0.05668723526771163, -0.20139793272346868, -0.18802248245350517, -0.21010536778111788, 0.1410139439001265, -0.1551597151693193, 0.14379343918973667, -0.14733246044586018, 0.10504848273940738, -0.14199962386734125, -0.1387640995824786, -0.21485045945776649, -0.20215012939314522, -0.20632870946659426, 0.1003157500169604, -0.20082865180626364, 0.1939104334510239, -0.20913157811453653, 0.1917910952969623, 0.10226167445422281, 0.0856247589373285, -0.20331342909029387, 0.08532554148089777, 0.08226410067573811, -0.14780278292092183, -0.20451611205647896, -0.197599156647145, -0.19443636370665426, 0.0780495252260043, 0.043987043636500446, 0.19425498569925534, 0.09483459268697107, 0.05769880315343434, -0.20784581870559313]
eigen2 = [-0.08907650160642859, 0.026954769800911244, -0.3298966959781828, 0.10664932617995687, -0.20885986601938322, -0.3437701777907989, 0.02017156165110373, 0.05495738986679827, -0.027116955618531113, 0.12308349905739117, -0.20349792114634394, 0.12082485561913227, -0.16617161647211057, 0.12251653303533179, 0.12285161617646738, 0.05160226764512307, -0.3448853749013426, 0.022967034443606364, -0.1986175599799399, -0.343006158908526, -0.06933486753307437, 0.054934792100026324, -0.09590161773938392, -0.0999773221711038, -0.14495044981013536, -0.33930565920893163, 0.11232935737133166, 0.11170763992291768, 0.12055419936590943, 0.019532905141505325, 0.05607526054878952, 0.0331565084921608, -0.14653950122372245, 0.08759484247099937, -0.0830629303350005, -0.19936643722170241, -0.10392933599684473, 0.055226536719430806]
