import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize("last_name, first_name, patronymic, date, email, optional, phone, snils, "
                         "profession, country, city, organization, school, grade", [
    ("Иванов", "Иван", "Иванович", "01.01.2000", "ivanov@mail.ru", "v00.000.000", "+79991234567",
     "41825422769", "Программист", "Россия", "Москва", "ООО", "Средняя школа №1", "10"),  # Валидные данные
    ("Иванов", "Иван", "Иванович", "01.01.2000", "ivanovmail.ru", "v00.000.000", "+79991234567",
     "41825422769", "Программист", "Россия", "Москва", "ООО", "Средняя школа №1", "10"),  # Невалидный email
    ("Иванов", "Иван", "Иванович", "01.01.2000", "ivanov@mail.ru", "v11.11.111", "+79991234567",
     "41825422769", "Программист", "Россия", "Москва", "ООО", "Средняя школа №1", "10"),  # Некорректным форматом ВОШ-логина

])
def test_registration_fields_simple(last_name, first_name, patronymic, date, email, optional,
                                    phone, snils, profession, country, city, organization, school, grade):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)

    driver.get('https://uts.sirius.online//#/auth/register/qainternship')

    # Заполняем поля
    last_name_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-lastName input")
    last_name_field.send_keys(last_name)

    first_name_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-firstName input")
    first_name_field.send_keys(first_name)

    patronymic_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-patronymic input")
    patronymic_field.send_keys(patronymic)

    date_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-birth-date input")
    date_field.send_keys(date)

    email_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-email input")
    email_field.send_keys(email)

    optional_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-vosh-login-optional input")
    optional_field.send_keys(optional)

    phone_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-phone input")
    phone_field.send_keys(phone)

    snils_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-snils-opt input")
    snils_field.send_keys(snils)

    profession_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-profession input")
    profession_field.send_keys(profession)

    country_field = driver.find_element(By.CSS_SELECTOR, "[class*='reset'] [value='RU']")
    country_field.click()

    city_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-school-city input")
    city_field.send_keys(city)

    organization_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-school-organization input")
    organization_field.send_keys(organization)

    school_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-school-school input")
    school_field.send_keys(school)

    grade_field = driver.find_element(By.CSS_SELECTOR, ".test-locator-sf-school-grade input")
    grade_field.send_keys(grade)

    confirmation_checkbox = driver.find_element(By.CSS_SELECTOR, "[class *='outline'][wfd-id='id13']")
    confirmation_checkbox.click()

    personal_checkbox = driver.find_element(By.CSS_SELECTOR, "[class *='outline'][wfd-id='id14']")
    personal_checkbox.click()

    familiarized_checkbox = driver.find_element(By.CSS_SELECTOR, "[class *='outline'][wfd-id='id15']")
    familiarized_checkbox.click()

    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button__content")))

    # Проверяем
    assert last_name_field.get_attribute("value") == last_name
    assert first_name_field.get_attribute("value") == first_name
    assert patronymic_field.get_attribute("value") == patronymic
    assert date_field.get_attribute("value") == date
    assert email_field.get_attribute("value") == email
    assert optional_field.get_attribute("value") == optional
    assert phone_field.get_attribute("value") == phone
    assert snils_field.get_attribute("value") == snils
    assert profession_field.get_attribute("value") == profession
    assert country_field.is_selected() == True
    assert city_field.get_attribute("value") == city
    assert organization_field.get_attribute("value") == organization
    assert school_field.get_attribute("value") == school
    assert grade_field.get_attribute("value") == grade

    # Проверяем чекбоксы
    assert confirmation_checkbox.is_selected() == True
    assert personal_checkbox.is_selected() == True
    assert familiarized_checkbox.is_selected() == True

    print(f"✓ Тест пройден: {last_name}, {first_name}, {patronymic}, {date}, {email}, {optional}, {phone}, {snils}, {profession}, {country}, {city}, {organization}, {school}, {grade}")

    driver.quit()
