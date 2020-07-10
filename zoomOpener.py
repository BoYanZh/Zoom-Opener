import time, json, datetime, subprocess, sys, os
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import COOKIE, CLASS_INFO

driver = None
URL_TEMPLATE = "https://umjicanvas.com/courses/{id}/external_tools/78"


def isOddWeek(d):
    d2 = datetime.datetime(2020, 5, 11)
    return ((d - d2).days // 7 + 1) % 2 == 1


def getCourseName(index):
    d = datetime.datetime.now()
    timeStr = d.strftime('%m-%d %H:%M:%S')
    print(f"\r{timeStr}", end="", flush=True)
    weekDayNow, isOdd = d.weekday() + 1, isOddWeek(d)
    for courseName, info in CLASS_INFO.items():
        url = URL_TEMPLATE.format(id=info['id'])
        for weekDay, classTime, onlyOdd in info["time"]:
            if weekDay != weekDayNow or \
               classTime != index or \
               (not isOdd and onlyOdd):
                continue
            print(f"{timeStr} {courseName} will start soon!", flush=True)
            return courseName


def initDriver():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches",
                                           ["enable-logging"])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://umjicanvas.com")
    for key, value in COOKIE.items():
        driver.add_cookie({'name': key, 'value': value})


def openZoom(courseName, timeout=10):
    initDriver()
    url = URL_TEMPLATE.format(id=CLASS_INFO[courseName]['id'])
    print(f"Canvas Url: {url}", flush=True)
    driver.get(url)
    seq = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "tool_content")))
    driver.switch_to.frame(seq)
    btns = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[class='ant-btn ant-table-span']")))
    links = [btn.get_attribute('href') for btn in btns]
    print(f"Join Url: {url}", flush=True)
    driver.get(links[0])
    launchElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#zoom-ui-frame > div > div > div > div > div:nth-child(3) > h3 > a:nth-child(1)"
        )))
    launchLink = launchElement.get_attribute('href')
    if sys.platform.startswith('linux'):
        subprocess.call(["xdg-open", launchLink])
    else:
        os.startfile(launchLink)
    driver.quit()


def cronJob(index):
    courseName = getCourseName(index)
    if courseName is not None:
        openZoom(courseName)


def cronJobGenerator(index):
    def wrapper():
        return cronJob(index)

    return wrapper


def main():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    startTimes = ['0755', '0955', '1205', '1355', '1555', '1825']
    for i, t in enumerate(startTimes):
        h, m = t[:2], t[-2:]
        scheduler.add_job(cronJobGenerator(i + 1), 'cron', hour=h, minute=m)
    print(datetime.datetime.now().strftime("%m-%d %H:%M:%S"),
          "task start",
          flush=True)
    scheduler.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
