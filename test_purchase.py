from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "standard_user"
PASSWORD = "secret_sauce"
TIMEOUT = 10


def test_buy_product(browser, base_url):
    wait = WebDriverWait(browser, TIMEOUT)

    # ---------- Страница авторизации ----------
    browser.get(base_url)
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()

    # ---------- Страница с товарами ----------
    wait.until(EC.url_contains("inventory"))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
    add_to_cart_button = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    add_to_cart_button.click()

    # ждём, пока счётчик корзины покажет 1 товар
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
    )
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    # ---------- Страница корзины ----------
    wait.until(EC.url_contains("cart"))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))
    checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()

    # ---------- Страница с оформлением (форма) ----------
    wait.until(EC.url_contains("checkout-step-one"))
    first_name = wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
    last_name = wait.until(EC.visibility_of_element_located((By.ID, "last-name")))
    postal_code = wait.until(EC.visibility_of_element_located((By.ID, "postal-code")))

    first_name.send_keys("Ivan")
    last_name.send_keys("Ivanov")
    postal_code.send_keys("123456")

    continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
    continue_button.click()

    # ---------- Страница с оплатой товара ----------
    wait.until(EC.url_contains("checkout-step-two"))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_info")))
    finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
    finish_button.click()

    # ---------- Текст об успешной покупке ----------
    wait.until(EC.url_contains("checkout-complete"))
    header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "complete-header"), "Thank you for your order!"
    ))
    assert header.text == "Thank you for your order!"
