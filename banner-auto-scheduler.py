from datetime import datetime

class Section:
  def __init__(self, crn):
    self.crn = str(crn)
    self.start = ""
    self.end = ""
    self.days = ""
    self.name = ""
    self.conflicts = []
  def __str__(self):
    return("c" + str(self.crn))

  def get_start_offset(self):
    fmt = '%I:%M %p'
    d1 = datetime.strptime("12:00 am", fmt)
    d2 = datetime.strptime(self.start, fmt)
    return (d2 - d1).total_seconds()

  def get_end_offset(self):
    fmt = '%I:%M %p'
    d1 = datetime.strptime("12:00 am", fmt)
    d2 = datetime.strptime(self.end, fmt)
    return (d2 - d1).total_seconds()

  def __repr__(self):
    return self.__str__()

  def get_sympy_constraints(self):
    output = str(self.__str__()) + " = Not(Or(" + str(self.conflicts) + "))"
    output = output.replace("]", "").replace("[", "")
    return(output)
	
def doesOverlap(a, b):
  return max(0, min(a[1], b[1]) - max(a[0], b[0])) != 0

def doSectionsOverlap(s1, s2):
  cond1 = doesOverlap([s1.get_start_offset(), s1.get_end_offset()], [s2.get_start_offset(), s2.get_end_offset()])
  cond2 = set(list(s1.days)) & set(list(s2.days))

  # if the times overlap, then the days might not have any in common
  return (len(cond2) != 0) and cond1

class Course:
  def __init__(self, name):
    self.name = name
    self.lectures = []
    self.labs = []
    self.tutorials = []
	
  def __str__(self):
    return(self.name)

  def get_sympy_constraints(self):
    lectureCondition = "Or(" + str(self.lectures) + ")"
    labCondition = "True"
    if (len(self.labs) > 0):
      labCondition = "Or(" + str(self.labs) + ")"
    tutorialCondition = "True"
    if (len(self.tutorials) > 0):
      tutorialCondition = "Or(" + str(self.tutorials) + ")"
    
    return(self.name + (" = And(" + lectureCondition + "," + tutorialCondition + "," + labCondition + ")").replace("[", "").replace("]", ""))

import pandas as pd
ex_data = pd.read_excel('Dal Course List.xlsx', dtype={'CRN': object, "Crse": object})

sections = []
courses = {}

for index, row in ex_data.iterrows():
  section = Section(str(row["CRN"]))
  if (row["Time"] != "TBA"):
    section.start = row["Time"].split("-")[0]
    section.end = row["Time"].split("-")[1]
    section.days = row["Days"]
    section.name = row["Sec"]
    section.course_title = str(row["Subj"]) + str(row["Crse"])
    sections.append(section)

for section in sections:
  if not section.course_title in courses.keys():
    courses[section.course_title] = Course(section.course_title)

  if (str(section.name).startswith("B")):
    courses[section.course_title].labs.append(section)
  elif (str(section.name).startswith("T")):
    courses[section.course_title].tutorials.append(section)
  else:
    courses[section.course_title].lectures.append(section)

print("Calculating conflicts...")
for i in range(len(sections)):
  for j in range(len(sections)):
    if (doSectionsOverlap(sections[i], sections[j])) and (sections[i].crn != sections[j].crn):
      sections[i].conflicts.append(sections[j])

	  
# add each lecture, tutorial, and lab as a conflict to every other lab in the course so that the student
# can only register for one lecture, one tutorial, and one lab

for title, contents in courses.items():
  for i in range(len(contents.tutorials)):
    for j in range(len(contents.tutorials)):
	  if (contents.tutorials[i].crn != contents.tutorials[j].crn):
		contents.tutorials[i].conflicts.append(contents.tutorials[j])
		contents.tutorials[i].conflicts = list(set(contents.tutorials[i].conflicts))
  for i in range(len(contents.labs)):
    for j in range(len(contents.labs)):
	  if (contents.labs[i].crn != contents.labs[j].crn):
		contents.labs[i].conflicts.append(contents.labs[j])
		contents.labs[i].conflicts = list(set(contents.labs[i].conflicts))
  for i in range(len(contents.lectures)):
    for j in range(len(contents.lectures)):
	  if (contents.lectures[i].crn != contents.lectures[j].crn):
		contents.lectures[i].conflicts.append(contents.lectures[j])
		contents.lectures[i].conflicts = list(set(contents.lectures[i].conflicts))


programToExecute = ["from z3 import *"]
sectionCrns = []
for section in sections:
  programToExecute.append("c" + section.crn + " = Bool('" + section.crn + "')")
  sectionCrns.append("c" + section.crn)

for section in sections:
  programToExecute.append(section.get_sympy_constraints())

courseConstraints = []
for key in courses.keys():
  courseConstraints.append(courses[key].get_sympy_constraints())

tmp = "\n".join(programToExecute) + "\n"
out2 = "\n".join(courseConstraints)

outFinal = tmp + out2
exec(outFinal)

from itertools import combinations 

firstYearCourses = [CSCI1105,CSCI1106,CSCI1107,CSCI1108,CSCI1109,CSCI1110,CSCI1120,CSCI1170,CSCI1801]

#firstYearCourses = [CSCI2202,CSCI2203,CSCI2201,CSCI2141,CSCI4152,CSCI4155,CSCI3151,CSCI2100,CSCI4116,CSCI3130,CSCI2691,CSCI2690,CSCI3171,CSCI4144,CSCI1120,CSCI6999,CSCI5100,CSCI3172,CSCI6610,CSCI1108,CSCI1109,CSCI6708,CSCI6802,CSCI5409,CSCI3901,CSCI1105,CSCI1106,CSCI1107,CSCI5408,CSCI4181,CSCI3691,CSCI3136,CSCI5708,CSCI4166,CSCI4163,CSCI4145,CSCI3101,CSCI6406,CSCI2170,CSCI3160,CSCI2114,CSCI2112,CSCI2113,CSCI2110,CSCI6709,CSCI6405,CSCI1170,CSCI5709,CSCI6505,CSCI2122,CSCI6509,CSCI1110,CSCI3162,CSCI4691,CSCI5306,CSCI5308,CSCI2134,CSCI4177,CSCI4174]

comb = combinations(firstYearCourses, 5)

anotherProgram = "totalThings = [" + ",".join(sectionCrns) + "]\n"
anotherProgram = anotherProgram + "nan = False\ntotalThingsOffsets = [" + (",".join(sectionCrns)).replace("c", "") + "]"

exec(anotherProgram)

solutions = []
totalNonSols = 0
totalSols = 0
longestSolution = 0
for i in list(comb):
	s = Solver()
	combList = list(i)
	s.add(And(combList))
	if (str(s.check()) == "sat"):
		totalSols = totalSols + 1
		k = 0
		localSolutions = []
		for j in totalThings:
			localSolutions.append([totalThingsOffsets[k], is_true(s.model().eval(j))])
			k = k + 1
		solutions.append(localSolutions)
	else:
		totalNonSols = totalNonSols + 1


out = solutions
print("There are " + str(totalSols) + " possible schedules and " + str(totalNonSols) + " non-solutions")
	
import os
ex_data = pd.read_excel('Dal Course List.xlsx')
os.mkdir('dal_proposed_schedules')

for i in range(len(out)):
	print("Saving schedule " + str(i) + "...")
	outData = pd.DataFrame(out[i], columns=['CRN', 'Must take'])
	left_merge = pd.merge(ex_data, outData, how='left')

	left_merge.to_excel("dal_proposed_schedules/output_" + str(i) + ".xlsx")
