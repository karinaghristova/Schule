# Schule
# What is Schule?
Schule is my final project for a course in university called Programming with Python. Schule is a Django application that represents an online gradebook. 
# Who can use Schule?
Upon registration every user selects a role - a parent or a student. Registration for teachers happens at a different place for a reason.
# What can admin do?
Well, except for everything... 
- There is also a homepage for them where they can see statistics about the amount of users and their count by roles, the amount of schools, grades, absences, remarks and praises
# What can teachers do?
Teachers have a more active role in Schule as they can do the following thing:
- Edit information of students from their school
- See details about students from their school
- See details about students from their subject classes
- Assign child to every parent from their school
- See details about parents from their school
- Create subjects
- Create subject classes
- Edit subject classes, which includes changing their subject and class levels as well as adding and removing students from them
- Delete subject classes
- Add grades for a subject class
- Update grades for a subject class
- Delete grades for a subject class
- Add absence for a subject class
- Edit absences for their subject classes, which includes changing their date, excusing them, changing the student for which the absence is intended, changing the term
- Delete absences for their subject classes
- Add remarks
- Edit remarks they have made
- Delete remarks they have made
- Add praises
- Edit praises they have made
- Delete praises they have made
# What can parents do?
Parents and students have more of a passive role in this application, but there is still a lot of things they can do passively
## If they don't have a child
- See information about them
- Update information about themselves
## If they have a child:
- Same things, but also...
- See statistics about:
- The amount of grades their child has for both terms
- The amount of grades their child has for both terms according to their value
- The amount absences their child has for both terms
- The amount remarks their child has for both terms
- The amount praises their child has for both terms
- See grades of their child
- Amount of grades for every term and for the year
- Amount of grades for every term according to their values
- Every grade for every subject class the child is part of
- See absences of their child
- Amount of absences for every term and for the year
- Absences of the child for every subject, where an absence is present (Funny right, an absence is present)
- See remarks of their child
- Amount of remarks for every term and for the year
- Every remark of the child 
- See praises of their child
- Amount of praises for every term and for the year
- Every praise of the child 
# What can students do?
Basically the same things their parents can do :)
- See information about them
- Update information about themselves
- See statistics about:
- The amount of grades they have for both terms
- The amount of grades they have for both terms according to their value
- The amount absences they have for both terms
- The amount remarks they have for both terms
- The amount praises they have for both terms
- See their grades 
- Amount of grades for every term and for the year
- Amount of grades for every term according to their values
- Every grade for every subject class they are part of
- See their absences 
- Amount of absences for every term and for the year
- Absences for every subject, where an absence is present 
- See remarks teachers have made about them
- Amount of remarks for every term and for the year
- Every remark 
- See praises teachers have made for them
- Amount of praises for every term and for the year
- Every praise 
# Techologies used
- Python Django
- Bootstrap
- Chart.js
