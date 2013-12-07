"""
Download all pdfs since 2010, throw them in data/sceq_pdfs
"""

import urllib2,cookielib,os

# Fall 2010 was the first semester to use the new format.
years = "10 11 12 13".split()
semesters = "F S".split()
depts = ["AFST","ECAC","GERO","LATN","SCI",
         "AGNG", "ECON", "GES", "LING", "SOCY",
         "AMST", "EDUC", "GREK", "LLC", "SOWK",
         "ANCS", "EHS", "GWST", "MAED", "SPAN",
         "ANTH", "ELC", "HAPP", "MATH", "SPCH",
         "ARBC", "ENCE", "HCST", "MCS", "STAT",
         "ARCH", "ENCH", "HEBR", "MLL", "THTR",
         "ART", "ENEE", "HIST", "MUSC", "WOL",
         "BIOL", "ENES", "HONR", "PHED",
         "BTEC", "ENGL", "HUM", "PHIL",
         "CHEM", "ENME", "INDS", "PHYS",
         "CHIN", "ENMG", "JDST", "POLI",
         "CMPE", "FREN", "JPNS", "PSYC",
         "CMSC", "FYS", "KORE", "PUBL",
         "DANC", "GERM", "LAS", "RUSS"]

def make_url(year,sem,dept):
    """Generate the address of the corresponding pdf"""
    if sem == "spring" and year == "10":
        raise ValueError("Can't lookup pdfs fmor that semester'")
    url = "http://oir.umbc.edu/files/2013/02/%s_%s%s.pdf" % (dept,sem,year)
    return url

def dl_pdf(url):
    """Download pdf hosted at url"""
    #http://stackoverflow.com/questions/5627083/
    theurl = url
    pdf_name = url.split("/")[-1]
    pdf_dir = os.path.join("..","..","data","sceq_pdfs")
    full_filename = os.path.join(pdf_dir,pdf_name)
    if pdf_name in os.listdir(pdf_dir):
        print "found %s, moving on" % pdf_name
        return
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders.append(('Cookie', cj))
    try:
        print("... Sending HTTP GET to %s" % theurl)
        request = urllib2.Request(theurl)
        f = opener.open(request)
        data = f.read()
        f.close()
        opener.close()
        FILE = open(full_filename, "wb")
        FILE.write(data)
        FILE.close()
    except:
        print "Something bad happened with %s, moving on" % theurl
        return
    
def __main__():
    for year in years:
        for sem in semesters:
            for dept in depts:
                try:
                    url = make_url(year,sem,dept)
                except ValueError:
                    continue
                dl_pdf(url)
