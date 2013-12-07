"""
Code to read a scraped txt and emit some kind of rational data structure :(
"""
from utils import *
import re,os,cPickle
from collections import defaultdict

def parse_all():
    txt_path = "../../data/sceq_txts"
    txt_names = filter(lambda x:x.endswith("txt"),os.listdir(txt_path))
    ds = []
    for txt_name in txt_names:
        print "txt_name:,",txt_name
        ds.append(parse_txt(os.path.join(txt_path,txt_name)))
    return sum(ds,[])

def combine_dicts(d1,d2):
    """Given two dictionaries, combine them"""
    assert all(d1[val]==d2[val] for val in "year semester course_num section".split())
    ##print "d1:",[d1[val] for val in "year semester course_num section".split()]
    ##print "d2:",[d2[val] for val in "year semester course_num section".split()]
    combined_dict = {}
    for k,v in d1.items():
        #print "d1 k,v",k,v
        combined_dict[k] = v
    for k,v in d2.items():
        #print "d2 k,v",k,v
        if not k == 'questions':
            combined_dict[k] = v
    for q,v in d2['questions'].items():
        #print "q,v:",q,v
        combined_dict['questions'][q] = v
    return combined_dict

def proj(d):
        return (d['year'],d['semester'],d['dept'],d['course_num'],d['section'])

def parse_txt(text_filename):
    """Parse the txt corresponding to one pdf by splitting it into
    pages, parsing the pages, and combining the resulting dicts"""
    with open(text_filename) as f:
            lines = f.readlines()
            page_strings = "".join(lines).split('\x0c')
            all_ds = []
            for i,page in enumerate(page_strings):
                #print "page:",i
                all_ds.append(parse_page(page))
    ds = filter(lambda d:not d is None,all_ds)
    print "Parsed %s pages in %s with %s success rate" % (len(all_ds),text_filename,len(ds)/float(len(all_ds)))
    # ds may contain multiple dicts for a single class, so combine them...
    print "partitioning:",text_filename
    partition = partition_according_to(proj,ds)
    final_partition = (map(lambda equiv_class:reduce(combine_dicts,equiv_class),partition))
    final_partition
    print "reduced to %s unique classes" % len(final_partition)
    return final_partition

def parse_page(page_string):
    """Parse text corresponding to one page of the pdf, returning a
    dictionary of relevant fields"""
    if page_string.strip() == "":
        print "found empty page"
        return None
    page_dict = {}
    page_dict["questions"] = defaultdict(dict)
    lines = page_string.split("\n")
    is_2010 = "Spring 2010" in page_string
    for line in lines:
        line = line.strip()
        if line.startswith("Course-Section") and not is_2010:
            _,dept,course_num,section,_,_,semester,year,_,enrollment_number = line.split()
            for var in "dept course_num section semester year enrollment_number".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("Course-Section") and is_2010:
            _,dept,course_num,section,_,_,_,_,_ = line.split()
            for var in "dept course_num section".split():
                page_dict[var] = read(eval(var))            
        elif line.startswith("Title:") and not is_2010:
            fields = line.split()
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
            try:
                question = " ".join(re.findall(r"[A-Za-z,]+",line))
                question_ends_at = line.rindex(question[-1])
                numeric_fields = line[question_ends_at+1:].split()
                (nr,na,one,two,three,four,five,mean,rank,
                 course_mean,org_mean,umbc_mean,level_mean,sect) = numeric_fields
                rank_numer,rank_denom = rank.split("/")
                for var in "nr na one two three four five mean course_mean org_mean umbc_mean level_mean sect".split():
                    page_dict["questions"][question][var] = read(eval(var))
                page_dict["rank"] = (rank_numer,rank_denom)
            except IndexError:
                print "shitty pdf, moving to next line"
        elif line.startswith("00-27"):
            (_,num_fresh,_,num_gpa0,_,num_exp_A,_,_,_,
             req_for_maj,_,grad,_,maj) = line.split()
            for var in "num_fresh num_gpa0 num_exp_A req_for_maj grad maj".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("28-55"):
            (_,num_soph,_,num_gpa1,_,num_exp_B) = line.split()
            for var in "num_soph num_gpa1 num_exp_B".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("56-83"):
            (_,num_jun,_,num_gpa2,_,num_exp_C,_,general,_,ugrad,_,non_maj) = line.split()
            for var in "num_jun num_gpa2 num_exp_C general ugrad non_maj".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("84-150"):
            (_,num_sen,_,num_gpa3,_,num_exp_D) = line.split()
            for var in "num_sen num_gpa3 num_exp_D".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("Grad."):
            eff_line = line[:line.index("*")]
            (_,num_grad,_,num_gpa35,_,num_exp_F,_,electives) = eff_line.split()
            for var in "num_grad num_gpa35 num_exp_F electives".split():
                page_dict[var] = read(eval(var))
        elif line.startswith("P "):
            page_dict["num_exp_P"] = int(line.split()[1])
        elif line.startswith("I "):
            page_dict["num_exp_I"] = int(line.split()[1])
        else:
            pass
            #print "skipping:",line[:60],"..."
    if not ('year' in page_dict):
        print "found page_dict w/out year"
        print "page string:",page_string,"|"
        return None
    return page_dict

def read(x):
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            return x
