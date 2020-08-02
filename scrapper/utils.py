#!/usr/bin/python
# -*- coding: utf-8 -*-

SIGARRA_URLS = {
    'homepage': 'https://sigarra.up.pt/feup/pt/',
    'course_plan': 'https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_plano_id={}&pv_ano_lectivo=2019&pv_tipo_cur_sigla=MI&pv_origem=CUR',
    'rate_stats': 'https://sigarra.up.pt/feup/pt/est_geral.dist_result_ocorr?pv_ocorrencia_id={}&PV_ANO_LETIVO={}',
    'grade_stats': 'https://sigarra.up.pt/feup/pt/est_geral.dist_result_ocorr_detail?pv_ocorrencia_id={}&PV_ANO_LETIVO={}'
}

SIGARRA_URL_HEADERS = {
    'auth': 'vld_validacao.validacao'
}

NUMBERS_PT = {
    'Zero': 0,
    'Um': 1,
    'Dois': 2,
    'Três': 3,
    'Quatro': 4,
    'Cinco': 5,
    'Seis': 6,
    'Sete': 7,
    'Oito': 8,
    'Nove': 9,
    'Dez': 10,
    'Onze': 11,
    'Doze': 12,
    'Treze': 13,
    'Catorze': 14,
    'Quinze': 15,
    'Dezasseis': 16,
    'Dezassete': 17,
    'Dezoito': 18,
    'Dezanove': 19,
    'Vinte': 20
}


def get_course_units(soup):
    a_list = soup.find_all('a')

    years_div_list = []

    for a in a_list:
        if a.text is not None and 'Ano' in a.text:
            div = a.find_parent('div', {'class': 'caixa'})
            years_div_list.append(div)

    years = {}

    for year_div in years_div_list:

        years[years_div_list.index(year_div) + 1] = {
            '1': get_course_units_by_semester(year_div, 1),
            '2': get_course_units_by_semester(year_div, 2)
        }

    return years


def get_course_units_by_semester(year_div, semester):
    semester_object = []

    for semester_header in year_div.find_all('th', text='{}º Semestre'.format(semester)):
        table = semester_header.find_parent('table')

        rows_i = table.find_all('tr', {'class': 'i'})
        rows_j = table.find_all('tr', {'class': 'p'})

        rows = []

        rows.extend(rows_i)
        rows.extend(rows_j)

        for row in rows:
            a = row.find('a')

            if a is None:
                continue

            href = a.get('href')

            if href is None:
                continue
            elif 'ucurr_geral' not in href:
                continue

            code = row.find('td', {'class': 'k'}).text
            acronym = row.find('td', {'class': 'l'}).text
            credits = row.find('td', {'class': 'n'}).text

            id = href.split('=')[1]
            name = a.text

            subject = {
                'id': id,
                'code': code,
                'acronym': acronym,
                'name': name,
                'credits': credits
            }

            semester_object.append(subject)

    return semester_object
