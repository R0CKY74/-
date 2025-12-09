import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    """Настройка драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    return driver, WebDriverWait(driver, 10)


def fill_text_field(driver, css_selector, value):
    """Заполнение текстового поля"""
    field = driver.find_element(By.CSS_SELECTOR, css_selector)
    field.send_keys(value)
    return field


def click_checkbox(driver, css_selector):
    """Клик по чекбоксу"""
    checkbox = driver.find_element(By.CSS_SELECTOR, css_selector)
    if not checkbox.is_selected():
        checkbox.click()
    return checkbox


def fill_registration_form(driver, data):
    """Заполнение всей формы регистрации"""
    fields = {
        ".test-locator-sf-lastName input": data['last_name'],
        ".test-locator-sf-firstName input": data['first_name'],
        ".test-locator-sf-patronymic input": data['patronymic'],
        ".test-locator-sf-birth-date input": data['date'],
        ".test-locator-sf-email input": data['email'],
        ".test-locator-sf-vosh-login-optional input": data['optional'],
        ".test-locator-sf-phone input": data['phone'],
        ".test-locator-sf-snils-opt input": data['snils'],
        ".test-locator-sf-profession input": data['profession'],
        ".test-locator-sf-school-city input": data['city'],
        ".test-locator-sf-school-organization input": data['organization'],
        ".test-locator-sf-school-school input": data['school'],
        ".test-locator-sf-school-grade input": data['grade']
    }

    filled_fields = {}
    for selector, value in fields.items():
        filled_fields[selector] = fill_text_field(driver, selector, value)

    return filled_fields


def check_fields_values(fields, data):
    """Проверка значений полей"""
    mapping = {
        ".test-locator-sf-lastName input": 'last_name',
        ".test-locator-sf-firstName input": 'first_name',
        ".test-locator-sf-patronymic input": 'patronymic',
        ".test-locator-sf-birth-date input": 'date',
        ".test-locator-sf-email input": 'email',
        ".test-locator-sf-vosh-login-optional input": 'optional',
        ".test-locator-sf-phone input": 'phone',
        ".test-locator-sf-snils-opt input": 'snils',
        ".test-locator-sf-profession input": 'profession',
        ".test-locator-sf-school-city input": 'city',
        ".test-locator-sf-school-organization input": 'organization',
        ".test-locator-sf-school-school input": 'school',
        ".test-locator-sf-school-grade input": 'grade'
    }

    for selector, field in fields.items():
        expected_value = data[mapping[selector]]
        assert field.get_attribute("value") == expected_value, \
            f"Поле {selector} содержит '{field.get_attribute('value')}', а ожидалось '{expected_value}'"


@pytest.mark.parametrize("data", [
    {"last_name": "Иванов", "first_name": "Иван", "patronymic": "Иванович", "date": "01.01.2000", "email": "ivanov@mail.ru",
     "optional": "v00.000.000", "phone": "+79991234567", "snils": "41825422769", "profession": "Программист", "city": "Москва",
     "organization": "ООО", "school": "Средняя школа №1", "grade": "10"},  # Валидные данные
    {"last_name": "Иванов", "first_name": "Иван", "patronymic": "Иванович", "date": "01.01.2000", "email": "ivanovmail.ru",
     "optional": "v00.000.000", "phone": "+79991234567", "snils": "41825422769", "profession": "Программист", "city": "Москва",
     "organization": "ООО", "school": "Средняя школа №1", "grade": "10"},  # Невалидный email
    {"last_name": "Иванов", "first_name": "Иван", "patronymic": "Иванович", "date": "01.01.2000", "email": "ivanov@mail.ru",
     "optional": "v0.000.000", "phone": "+79991234567", "snils": "41825422769", "profession": "Программист", "city": "Москва",
     "organization": "ООО", "school": "Средняя школа №1", "grade": "10"},  # Некорректный ВОШ-логин
])
def test_registration_fields_simple(data):
    driver, wait = setup_driver()

    try:
        driver.get('https://uts.sirius.online//#/auth/register/qainternship')

        # Заполнение формы
        fields = fill_registration_form(driver, data)

        # Дополнительные элементы
        country_field = driver.find_element(By.CSS_SELECTOR, "[class*='reset'] [value='RU']")
        country_field.click()

        confirmation_checkbox = click_checkbox(driver, "[class *='outline'][wfd-id='id13']")
        personal_checkbox = click_checkbox(driver, "[class *='outline'][wfd-id='id14']")
        familiarized_checkbox = click_checkbox(driver, "[class *='outline'][wfd-id='id15']")

        # Проверка кнопки
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button__content")))

        # Проверки
        check_fields_values(fields, data)
        assert country_field.is_selected() == True
        assert confirmation_checkbox.is_selected() == True
        assert personal_checkbox.is_selected() == True
        assert familiarized_checkbox.is_selected() == True

        print(f"✓ Тест пройден для {'Валидные данные'}, {'Невалидный email'}, {'Некорректный ВОШ-логин'}")

    finally:
        driver.quit()
