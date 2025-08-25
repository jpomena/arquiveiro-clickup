from selenium.webdriver.support.ui import WebDriverWait
import queue

fila_log = queue.Queue()


def log(texto):
    fila_log.put(texto)


def wait(driver, HTML_element=None, timeout=None):
    if not timeout:
        timeout = 45
    if not HTML_element:
        return WebDriverWait(driver, timeout)
    else:
        return WebDriverWait(HTML_element, timeout)
