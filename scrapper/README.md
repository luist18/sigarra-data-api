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

The scrapping process might take a while as it scrapes a lot of data. For example, the process of scrapping the data from the **ten** Integrated Masters taught at the Faculty of Engineering of the University of Porto takes about ~12 minutes.

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
    feup.course_ids.extend([2496, 2708]) # 2496 is the curricular plan id of MIEIC and 2708 is the curricular plan id of MIEQ
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
    "name": "Mestrado Integrado em Engenharia Informática e Computação",
    "curricular_plan_id": 2496,
    "faculty_id": "feup",
    "faculty_name": "Faculdade de Engenharia",
    "difficulty": 3.614957047730138,
    "course_units": [
        {
            "id": "436426",
            "name": "Matemática Discreta",
            "year": 1,
            "semester": 1,
            "code": "EIC0011",
            "acronym": "MDIS",
            "credits": 6.0,
            "average_grade": 10.816378758797187,
            "average_pass_rate": 67.82999999999998,
            "difficulty": 2.979056813819578,
            "grade_count": 1563,
            "grades": {
                "3": 41,
                "4": 37,
                "6": 41,
                "7": 58,
                "8": 74,
                "9": 63,
                "10": 281,
                "11": 209,
                "12": 179,
                "13": 147,
                "14": 106,
                "15": 78,
                "16": 66,
                "17": 42,
                "18": 35,
                "19": 13,
                "5": 30,
                "1": 25,
                "2": 30,
                "20": 6,
                "0": 2
            },
            "years": [
                {
                    "year": 2010,
                    "average_grade": 11.96551724137931,
                    "pass_rate": 68.28,
                    "difficulty": 3.1604275862068967,
                    "grade_count": 116,
                    "grades": {
                        "3": 1,
                        "4": 2,
                        "6": 2,
                        "7": 3,
                        "8": 8,
                        "9": 1,
                        "10": 20,
                        "11": 12,
                        "12": 17,
                        "13": 17,
                        "14": 13,
                        "15": 4,
                        "16": 5,
                        "17": 7,
                        "18": 3,
                        "19": 1
                    }
                },
                {
                    "year": 2011,
                    "average_grade": 10.345864661654133,
                    "pass_rate": 52.47,
                    "difficulty": 2.60127969924812,
                    "grade_count": 133,
                    "grades": {
                        "5": 1,
                        "6": 6,
                        "7": 9,
                        "8": 18,
                        "9": 14,
                        "10": 26,
                        "11": 22,
                        "12": 14,
                        "13": 7,
                        "14": 6,
                        "15": 5,
                        "16": 3,
                        "17": 2
                    }
                }
            ]
        },
        {
            "The rest of the data goes here": "Not shown for demonstration purposes"
        },
        {
            "The rest of the data goes here": "Not shown for demonstration purposes"
        },
        {
            "The rest of the data goes here": "Not shown for demonstration purposes"
        }
    ]
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

feup.course_ids.append(2708)
# At the middle of a process
feup.set_verbosity(True)

feup.fetch_courses()

```
