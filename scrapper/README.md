# SIGARRA U.Porto data scrapper

The **scrapper** is responsible for fetching the data (*i.e,* the pass rate and the grades, as well as useful information) from the SIGARRA website.

[**SIGARRA**](https://sigarra.up.pt/) is the digital information service of the University of Porto responsible for the information services of the **14** faculties of the university:

* Faculdade de Arquitetura;
* Faculdade de Belas Artes;
* Faculdade de Ciências;
* Faculdade de Ciências da Nutrição e Alimentação;
* Faculdade de Desporto;
* Faculdade de Direito;
* Faculdade de Economia;
* Faculdade de Engenharia;
* Faculdade de Farmácia;
* Faculdade de Letras;
* Faculdade de Medicina;
* Faculdade de Medicina Dentária;
* Faculdade de Psicologia e de Ciências da Educação;
* Instituto de Ciências Biomédicas Abel Salazar.

The scrapper needs the credentials of any student of any of the 14 faculties to work as the pass rate and grades are exclusive data for the students of the University of Porto.

The scrapping process might take a while as it scraps a lot of data. For example, the process of scrapping the data from the **ten** Integrated Masters taught at the Faculty of Engineering of the University of Porto takes about ~12 minutes.

## Installation

### Installation with PyPI package

```bash
pip install sigarra-data-scrapper
```

### Installation from the GitHub repository

1. Clone the GitHub repository
    ```bash
    git clone https://github.com/luist18/sigarra-course-stats-api.git
    ```
2. Change the working directory to the scrapper directory (*i.e.,* ```scrapper/```)
3. Install the scrapper package
    ```bash
    python setup.py sdist bdist_wheel
    ```
    
    or

    ```bash
    python setup.py install
    ```

## The classes

The following classes store the data scrapped as well as useful information.

### Course

- [X] **Name** - name of the course;
- [X] **Identifier** - course identifier, mainly used in *URLs* and parameters;
- [X] **Course units** - the course units of the course, the name and the identifier;
- [X] **Difficulty** - 0.0 to 5.0 rating based on the average grade of each course unit.

### Course Unit

- [X] **Name** - name of the course unit;
- [X] **Identifier** - course unit identifier, mainly used in *URLs* and parameters;
- [X] **Year** - year of the course in which the course unit is taught;
- [X] **Semester** - semester of the course in which the course unit is taught;
- [X] **Average grade** - the average grade of the course unit;
- [X] **Average rate** - the average pass rate of the course unit;
- [X] **Difficulty** - 0.0 to 5.0 rating based on the average grade and the average rate of the course unit;
- [X] **Grades** - array of grades given in the course unit;
- [X] **Years** - information about a panoply of data from 2010 to the current year.

### Course Unit Year

- [X] **Year** - the year of the data;
- [X] **Pass rate** - the pass rate of the course unit;
- [X] **Average grade** - the average grade of the course unit;
- [X] **Grades** - array of the grades given in the course unit.

