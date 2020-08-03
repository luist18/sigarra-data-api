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

## Running tests and coverage

### Testing

The tests are run after each commit by the `test.yml` GitHub workflow, but you can also run them locally with:
```bash
python -m unittest discover -s test -p '*_test.py'
```

### Coverage
```bash
coverage run --include="sigarra_data_scrapper/*" -m unittest
coverage report
```

## Examples

1. Import necessary classes
    ```python
    import json
    from sigarra_data_scrapper import Faculty
    ```
2. Authenticate to a faculty
    ```python
    auth = {
        'user': 'up201809679',
        'password': 'rick_astley_dancing'
    }

    feup = Faculty(auth, 'feup')
    ```
3. Fetch one or more courses
    ```python
    feup.courses.extend([2496, 2708]) # 2496 is the curricular plan id of MIEIC and 2708 is the curricular plan id of MIEQ
    ```

    or specify the courses while creating the `Faculty` object,

    ```python
    feup = Faculty(auth, 'feup', course_ids=[2496, 2708])
    ``` 

    then, fetch the data

    ```python
    feup.fetch_courses()
    ```
4. Show the data
    ```python
    for course in feup.courses:
        course_json = course.json_object()
        print(json.dumps(course_json, indent=4))
    ```

    or save to a file

    ```python
    for course in feup.courses:
        course.to_json('{}.json'.format(course.name))
    ```

### Example file

For demonstration purposes the data shown is shortened from the original data.

```json
{
    "name": "Mestrado Integrado em Engenharia Química",
    "id": 2708,
    "difficulty": 3.526216989553871,
    "course_units": [
        {
            "id": "436762",
            "name": "Álgebra",
            "year": 1,
            "semester": "1",
            "code": "EQ0058",
            "acronym": "A",
            "credits": "5",
            "average_grade": 14.018957345971565,
            "average_pass_rate": 87.82555555555557,
            "difficulty": 3.859354713006846,
            "grade_count": 422,
            "grades": {
                "2": 1,
                "6": 3,
                "7": 6,
                "8": 6,
                "10": 38,
                "11": 19,
                "12": 36,
                "13": 55,
                "14": 39,
                "15": 78,
                "16": 65,
                "17": 38,
                "18": 26,
                "19": 9,
                "5": 1,
                "4": 1,
                "20": 1
            },
            "years": {
                "2010": {
                    "year": 2010,
                    "average_grade": null,
                    "pass_rate": 81.61,
                    "difficulty": null,
                    "grade_count": 0,
                    "grades": null
                },
                ...
                ...
                ...
                "2018": {
                    "year": 2018,
                    "average_grade": 14.97142857142857,
                    "pass_rate": 94.52,
                    "difficulty": 4.136114285714285,
                    "grade_count": 70,
                    "grades": {
                        "8": 1,
                        "10": 5,
                        "11": 3,
                        "12": 1,
                        "13": 6,
                        "14": 9,
                        "15": 8,
                        "16": 21,
                        "17": 7,
                        "18": 6,
                        "19": 2,
                        "20": 1
                    }
                }
            }
        },
        ...
        ...
        ...
    }
}
```

## Verbosity

It is possible to enable verbosity while creating a faculty or at the middle of a process. By default, the verbosity is set to `False`.

```python
# While creating a faculty
fmup = Faculty(auth, 'fmup', course_ids=[5402], verbosity=True)
fmup.fetch_data()

feup = Faculty(auth, 'feup', course_ids=[2496])
feup.fetch_courses()

feup.courses.append(2708)
# At the middle of a process
feup.set_verbosity(True)

feup.fetch_courses()

```

### TODO

- [ ] Add verbosity to course_unit.py and course_unit_year.py