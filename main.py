from Model.QUERIES import *
from Model.Request import *
from pymysql import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait, Select
from Model.tools import *
import time


ENV = 'production'


def dbs() -> dict:
    n = json.loads(''.join([line for line in open('.config')]))
    return n[ENV]['db']


def uris() -> dict:
    n = json.loads(''.join([line for line in open('.config')]))
    return n[ENV]['uri']


db = dbs()
uri = uris()

conn4260 = connect(
    **db['qateam']
)
curs4260 = conn4260.cursor()

conn4397 = connect(
    **db['mantis']
)
curs4397 = conn4397.cursor()

testLink = uri['testlink']
mantis = uri['mantis']

rq_input = open('input.txt', encoding='utf-8')
rq_number = rq_input.readline().replace('\n', '')

# Se podrían separar por (',', ', ', ';', '; ', ':', ': ', '|', '-')
rq_associates = set(rq_input.readline().replace('\n', '').split(' '))

rq_summary = ''.join([line for line in rq_input])

curs4260.execute(CHILD_QUERY.replace('?', rq_number))
info = curs4260.fetchall()
if info:
    kwargs = {
        'request_number': info[0][0],
        'request_name': info[0][1],
        'request_status': info[0][2],
        'request_father': info[0][3],
        'request_type': info[0][4],
        'request_business_line': info[0][5],
        'request_business': info[0][6],
        'request_app': info[0][7],
        'request_dev_area': info[0][8],
        'request_dev_factory': info[0][9],
        'request_interested': info[0][10],
        'request_summary': rq_summary
    }

    r = Request(**kwargs)
    r.interested = rq_associates
    r.teams = r.make_teams()
    curs4260.execute(INTERESTED_QUERY.replace('?', str(r.teams)[1:-1]))
    interested = curs4260.fetchall()
    for i in interested:
        r.append_interested(*i)

    driver = webdriver.Chrome(executable_path=r'tools/chromedriver.exe')
    driver.maximize_window()

    curs4260.execute(TESTLINK_QUERY.replace('?', f'%{rq_number}%'))
    test_plan = curs4260.fetchone()

    if test_plan and rq_number in extract_numbers(test_plan[0]):
        print(f'Hallado, test-plan creado: {test_plan[0]}')
    else:
        driver.get(testLink['url'])
        login_field = driver.find_element(By.NAME, 'tl_login')
        login_field.clear()
        login_field.send_keys(testLink['username'])

        pass_field = driver.find_element(By.ID, 'tl_password')
        pass_field.clear()
        pass_field.send_keys(testLink['password'])

        driver.find_element(By.XPATH, '//*[@id="login"]/div[3]/input').submit()

        titlebar = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '/html/frameset/frame[1]')
            )
        )

        driver.switch_to.frame(titlebar)

        testproject = Select(driver.find_element(By.NAME, 'testproject'))
        testproject.select_by_visible_text('sph:Sophos')

        driver.switch_to.default_content()

        mainframe = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '/html/frameset/frame[2]')
            )
        )

        driver.switch_to.frame(mainframe)
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="test_plan_mgmt_topics"]/a[1]')
            )
        )
        driver.find_element(By.XPATH, '//*[@id="test_plan_mgmt_topics"]/a[1]').click()

        time.sleep(10)

        driver.find_element(By.NAME, 'create_testplan').submit()

        test_plan_name = driver.find_element(By.NAME, 'testplan_name')
        test_plan_name.send_keys(f'{r.type}{r.number}-{r.name}')

        driver.find_element(By.NAME, 'active').click()
        driver.find_element(By.NAME, 'is_public').click()

        notes_field = driver.find_element(By.NAME, 'notes')
        notes_field.clear()
        notes_field.send_keys(r.summary)

        driver.find_element(By.NAME, 'do_create').submit()

    # Consultar existencia en MANTIS-BT
    curs4397.execute(MANTIS_QUERY.replace('?', f'{r.number}'))
    mantis_project = curs4397.fetchone()

    if mantis_project and f'{r.number}' in mantis_project:
        print(f'Hallado, proyecto creado: {mantis_project[0]}')
    else:
        option = ''
        for op in (r.business, r.business_line, r.dev_area, r.app):
            op = op.upper()
            if op in OPTIONS:
                option = op
                break
            else:
                option = 'OTROS'

        driver.get(mantis['url'])
        input_username = driver.find_element(By.NAME, 'username')
        input_username.clear()
        input_username.send_keys(mantis['username'])  # Dejar el usuario y la contraseña en un archivo SQLite
        input_password = driver.find_element(By.NAME, 'password')
        input_password.clear()
        input_password.send_keys(mantis['password'])  # Dejar el usuario y la contraseña en un archivo SQLite
        driver.find_element(By.XPATH, "//form[@id='login-form']/fieldset/span/input").submit()

        WebDriverWait(driver, 2).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//ul[@id='menu-items']/li[8]/a")
            )
        )
        driver.find_element(By.XPATH, "//ul[@id='menu-items']/li[8]/a").click()
        WebDriverWait(driver, 2).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@id='manage-menu']/ul/li[2]/a")
            )
        )
        driver.find_element(By.XPATH, "//div[@id='manage-menu']/ul/li[2]/a").click()
        WebDriverWait(driver, 2).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//*[@id='content']/div[2]/table/tbody/tr[23]/td[1]/a")
            )
        )
        driver.find_element(By.LINK_TEXT, f'{op}').click()  # Calcular la linea de negocio
        WebDriverWait(driver, 2).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//input[@value='Nuevo Requerimiento']")
            )
        )
        driver.find_element(By.XPATH, "//input[@value='Nuevo Requerimiento']").click()
        WebDriverWait(driver, 2).until(
            expected_conditions.presence_of_element_located(
                (By.ID, 'project-description')
            )
        )
        input_project_name = driver.find_element(By.ID, 'project-name')
        input_project_name.clear()
        input_project_name.send_keys(f'{r.type}{r.number}-{r.name}')
        input_request_number = driver.find_element(By.ID, 'number-requ')
        input_request_number.clear()
        input_request_number.send_keys(f'{r.number}')
        input_project_description = driver.find_element(By.ID, 'project-description')
        input_project_description.clear()
        input_project_description.send_keys(f'{r.summary}')
        driver.find_element(By.CLASS_NAME, 'button').submit()

        driver.close()

    for j in r.interested:
        curs4397.execute(f"CALL sbtg0001_p_appendUserToProject('{j}', '{r.number}')")
        conn4397.commit()

else:
    print('No fue posible encontrar el requerimiento en QA-Team')

conn4397.commit()
curs4397.close()
conn4397.close()
curs4260.close()
conn4260.close()
