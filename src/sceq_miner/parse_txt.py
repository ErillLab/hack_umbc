"""
Code to read a scraped txt and emit some kind of rational data structure :(
"""
import re,os
from collections import defaultdict

class Course(object):
    """Represents a course"""
    def __init__(self,dept_name):
        pass

def test_parse_page():
    txt_path = "../../data/sceq_txts"
    txt_names = os.listdir(txt_path)
    for txt_name in txt_names:
        print "txt_name:,",txt_name
        with open(os.path.join(txt_path,txt_name)) as f:
            lines = f.readlines()
            page_strings = "".join(lines).split('\x0c')
            for i,page in enumerate(page_strings):
                print "page:",i
                d = parse_page(page)

def parse_page(page_string):
    page_dict = {}
    page_dict["questions"] = defaultdict(dict)
    lines = page_string.split("\n")
    is_2010 = "Fall 2010" in page_string or "Spring 2010" in page_string
    for line in lines:
        line = line.strip()
        if line.startswith("Course-Section") and not is_2010:
            _,dept,course_num,section,_,_,semester,year,_,enrollment_number = line.split()
            for var in "dept course_num section semester year enrollment_number".split():
                page_dict[var] = eval(var)
        elif line.startswith("Course-Section") and is_2010:
            _,dept,course_num,section,_,_,_,_,_ = line.split()
            for var in "dept course_num section".split():
                page_dict[var] = eval(var)
            
        elif line.startswith("Title:") and not is_2010:
            fields = line.split()
            print fields
            questionnaire_field = fields.index("Questionnaires:")
            title = " ".join(fields[1:questionnaire_field])
            num_questionnaires = fields[questionnaire_field + 1]
            page_dict["title"] = title
            page_dict["num_questionnaires"] = num_questionnaires
        elif line.startswith("Title:") and is_2010:
            fields = line.split()
            baltimore_field = fields.index("Baltimore")
            title = " ".join(fields[1:baltimore_field])
            page_dict["title"] = title
        elif line.startswith("Instructor:") and not is_2010:
            fields = line.split()
            instructor = "".join(fields[1:])
            page_dict["instructor"] = instructor
        elif line.startswith("Instructor:") and is_2010:
            fields = line.split()
            year_index = fields.index("2010")
            relevant_fields = fields[:year_index - 1]
            instructor = "".join(relevant_fields[1:])
            page_dict["instructor"] = instructor
            page_dict["semester"] = fields[year_index-1]
            page_dict["year"] = fields[year_index]
        elif line.startswith("Questionnaires") and is_2010:
            fields = line.split()
            page_dict["Questionnaires"] = fields[1]
        elif re.match(r"\d\.",line): # begins with [0-9]., i.e. is a question
            question = " ".join(re.findall(r"[A-Za-z,]+",line))
            question_ends_at = line.rindex(question[-1])
            numeric_fields = line[question_ends_at+1:].split()
            (nr,na,one,two,three,four,five,mean,rank,
             course_mean,org_mean,umbc_mean,level_mean,sect) = numeric_fields
            rank_numer,rank_denom = rank.split("/")
            for var in "nr na one two three four five mean course_mean org_mean umbc_mean level_mean sect".split():
                page_dict["questions"][question][var] = eval(var)
            page_dict["rank"] = (rank_numer,rank_denom)
        elif line.startswith("00-27"):
            (_,num_fresh,_,num_gpa0,_,num_exp_A,_,_,_,
             req_for_maj,_,grad,_,maj) = line.split()
            for var in "num_fresh num_gpa0 num_exp_A req_for_maj grad maj".split():
                page_dict[var] = eval(var)
        elif line.startswith("28-55"):
            (_,num_soph,_,num_gpa1,_,num_exp_B) = line.split()
            for var in "num_soph num_gpa1 num_exp_B".split():
                page_dict[var] = eval(var)
        elif line.startswith("56-83"):
            (_,num_jun,_,num_gpa2,_,num_exp_C,_,general,_,ugrad,_,non_maj) = line.split()
            for var in "num_jun num_gpa2 num_exp_C general ugrad non_maj".split():
                page_dict[var] = eval(var)
        elif line.startswith("84-150"):
            (_,num_sen,_,num_gpa3,_,num_exp_D) = line.split()
            for var in "num_sen num_gpa3 num_exp_D".split():
                page_dict[var] = eval(var)
        elif line.startswith("Grad."):
            eff_line = line[:line.index("*")]
            (_,num_grad,_,num_gpa35,_,num_exp_F,_,electives) = eff_line.split()
            for var in "num_grad num_gpa35 num_exp_F electives".split():
                page_dict[var] = eval(var)
        elif line.startswith("P "):
            page_dict["num_exp_P"] = int(line.split()[1])
        elif line.startswith("I "):
            page_dict["num_exp_I"] = int(line.split()[1])
        else:
            print "skipping:",line[:60],"..."
    return page_dict
