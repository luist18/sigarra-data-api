# The SIGARRA statistics scrapper

The **scrapper** is responsible for fetching the necessary data (*i.e,* the pass rate and the grades) from the SIGARRA website.

The process might take a while as it scraps a lot of data from the **ten** Integrated Masters taught at the Faculty of Engineering of the University of Porto.

## The classes

The following classes store the data scrapped as well as useful information.

### Course

- [X] **Name** - name of the course;
- [X] **Identifier** - course identifier, mainly used in *URLs* and parameters;
- [X] **Course units** - the course units of the course, the name and the identifier;
- [ ] **Difficulty** - 0.0 to 5.0 rating based on the average grade of each course unit.

### Course Unit

- [X] **Name** - name of the course unit;
- [X] **Identifier** - course unit identifier, mainly used in *URLs* and parameters;
- [X] **Year** - year of the course in which the course unit is taught;
- [X] **Semester** - semester of the course in which the course unit is taught;
- [ ] **Average grade** - the average grade of the course unit;
- [ ] **Average rate** - the average pass rate of the course unit;
- [ ] **Difficulty** - 0.0 to 5.0 rating based on the average grade and the average rate of the course unit;
- [X] **Grades** - array of grades given in the course unit;
- [X] **Years** - information about a panoply of data from 2010 to the current year.

### Course Unit Year

- [X] **Year** - the year of the data;
- [X] **Pass rate** - the pass rate of the course unit;
- [X] **Average grade** - the average grade of the course unit;
- [X] **Grades** - array of the grades given in the course unit.