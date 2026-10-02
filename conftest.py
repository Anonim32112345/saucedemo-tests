import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Браузер для запуска тестов: chrome, firefox или edge",
    )
    parser.addoption(
        "--url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Базовый URL тестируемого приложения",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера без графического интерфейса",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Фикстура для получения url из командной строки (--url)."""
    return request.config.getoption("--url")


@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для работы с браузером (--browser, --headless)."""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        # отключаем всплывающее окно менеджера паролей Chrome
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Браузер '{browser_name}' не поддерживается")

    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()  # закрытие браузера
