from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_buy_product(browser, base_url):
    wait = WebDriverWait(browser, 10)

    # 1. Переход на сайт
    browser.get(base_url)

    # 2. Авторизация
    browser.find_element(By.ID, "user-name").send_keys(USERNAME)
    browser.find_element(By.ID, "password").send_keys(PASSWORD)
    browser.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory"))

    # 3. Добавление товара в корзину
    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    badge = browser.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1", "В корзине должен быть 1 товар"

    # 4. Переход в корзину и оформление
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.url_contains("cart"))
    browser.find_element(By.ID, "checkout").click()

    # 5. Заполнение формы
    wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
    browser.find_element(By.ID, "first-name").send_keys("Ivan")
    browser.find_element(By.ID, "last-name").send_keys("Ivanov")
    browser.find_element(By.ID, "postal-code").send_keys("123456")
    browser.find_element(By.ID, "continue").click()

    # 6. Покупка товара
    wait.until(EC.url_contains("checkout-step-two"))
    browser.find_element(By.ID, "finish").click()

    # 7. Проверка успешности покупки
    header = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert header.text == "Thank you for your order!"
