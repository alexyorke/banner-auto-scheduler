# banner-auto-scheduler

Generates your university class schedule such that there are no time conflicts and satisfies your degree in a matter of seconds. All you need is an Excel sheet of courses (which you can copy and paste.) It will automatically generate all possible combinations of possible schedules that will allow you to take a collection of required courses, including automatically registering for applicable labs and tutorials.

*This application is not a substitute for a course or academic advisor, nor is it affiliated with the Banner system, Dalhousie University, or Saint Mary's University. It cannot determine your course eligibiity, or any special restrictions.*

## Getting started

Create an Excel spreadsheet called "Dal Course List.xlsx" in the directory where this script is stored. The data in this spreadsheet can be obtained by:

- log into DalOnline
- click "Web for Students"
- click "Registeration"
- click "Add/Drop Classes"
- click "Class Search"
- click "Advanced Search"
- select a section that has the course that you want to register for, and select it
- click "Section Search"
- copy from just after "Sections Found" text until the bottom of the schedule where the grey part ends
- paste it into an Excel spreadsheet called "Dal Course List.xlsx"
- save it in the directory where the script is stored
- if you have multiple courses from multiple different subjects, repeat the following except append the paste to the bottom of the spreadsheet, and do not copy any subject headers (make it look as if it was one large subject.) There should be no way to tell that it is a different subject other than different CRN numbers and different subject titles.

`git clone https://github.com/alhexyorke/banner-auto-scheduler`

`cd banner-auto-scheduler`

`pip install -r requirements.txt`

- modify the code (I said this was a quick-and-dirty project) so that the course list is the list of courses that you can register for. They are in the format as "CSCI1110", or whatever your course name is, case sensitive. The "5" is how many from that list you want to register for in that semester. You can change it to however many cousrses you'd like to register for.

`python banner-auto-scheduler.py`

- Afterwards, you will have a new directory called "dal_schedules_generated" in the directory where the script is. *Note: please check the waitlists and available seats before registering; this assumes that all courses do not have a waitlist.* You can open up the resulting Excel files and register for the sections that have "TRUE" next to them. Please see known bugs before registering though. *Note: when running the script twice, it will silently overwrite any pre-existing schedules in that folder.*

## How does it work?

Say I'm a first year student. For the sake of illustration, assume I can register for CSCI1105, CSCI1106, CSCI1107, CSCI1108, CSCI1109, CSCI1110, CSCI1120, CSCI1170, and/or CSCI1801. I want to take five courses from that list this semester; I don't care which ones. If I put these courses into `banner-auto-scheduler`, it will find all combinations of five courses from that list (126 combos), creates a set of SAT rules (constraints which dicate if another section can co-exist with another one), runs those rules through Microsoft's Z3 solver, then from the solutions which are satisfiable, creates a corresponding Excel sheet with those solutions. Just find the right-most column and register for the sections that say "TRUE". If there are multiple solutions, it will create more than one Excel sheet.

## Why did you use a SAT solver when brute-force is trivial?

A brute-force solution would have been cleaner and a lot simpler. However, it is not extensible. Future plans such as using it to satisfy future course requirements (I want to take CSCI 4001, what courses do I need to take for the next three years) becomes exponentially difficult to brute-force, as the requirements have lots of OR and AND clauses, and are linked to other courses.

A SAT solver really shines when the constraints and complexity increase exponentially. What if five friends in second year all want to take at least one course together? What if a resource planner want to estimate enrollment based from the students eligible to enroll in those courses, or what if I want to take a course at SMU and a course at Dal? 

### I have a part-time job and I can't attend lectures whenever I want

That's easy--just create a new course called CSCI 9999 on the master Excel sheet that you've copied and pasted, add the times that you are not available to it (following the same format as the other courses), and make it a required class. It will automatically "schedule" you to "attend" that course, and since there can be no two courses which are at the same time, then that schedule will schedule around your part-time job.

Saves hours trying to figure out how to register for your classes so that there are no time conflicts. Makes re-scheduling a breeze.

## Known bugs

- sometimes the resulting Excel sheet will say to register for a lab or tutorial without a lecture. Ignore those courses; just keep scrolling down until there is another course. The rest are valid solutions.

The code quality is horrible. This was meant to be a see-if-it-works experiment, but PR's are welcome.
