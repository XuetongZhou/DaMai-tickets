from selenium import webdriver
import pickle
import time
import datetime


def concert_info_input():
    # 填写演唱会信息
    print("请输入演唱会地点（如 杭州）：")
    city_in = input()
    print("请输入演唱会名称 （如 周杰伦嘉年华）：")
    concert_in = input()
    print(r"请输入开售时间，按%H:%M:%S格式 （如09:30:00,注意切换到英文输入法）")
    time_in = input()

    print("您要抢票的演唱会为" + concert_in + city_in + "站")
    print("开抢时间为" + time_in)
    return city_in, concert_in, time_in


def login_damai(driver):
    # 登录大麦网
    driver.implicitly_wait(5)
    driver.get("https://www.damai.cn")

    date_today = datetime.datetime.now().strftime('%m%d')
    cookies_name = "cookies" + date_today + ".pkl"

    try:
        cookies = pickle.load(open(cookies_name, "rb"))

        for cookie in cookies:
            cookie_dict = {
                'domain': '.damai.cn',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": "",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False}
            driver.add_cookie(cookie_dict)

        time.sleep(2)
        driver.refresh()
    except FileNotFoundError:
        print("请登录大麦网")

        while driver.title != "大麦登录":
            time.sleep(1)
        while driver.title == "大麦登录":
            time.sleep(2)

        pickle.dump(driver.get_cookies(), open(cookies_name, "wb"))
        print("登录成功！今日再次使用脚本时无需登录！")


def search_concert(driver, city_in, concert_in):
    # 查找演唱会 这里认为想看的演唱会在搜索结果的第一条
    concert_input = driver.find_element_by_class_name("input-search")
    concert_input.send_keys(city_in + " " + concert_in)
    driver.find_element_by_class_name("btn-search").click()

    time.sleep(2)

    concert_path = '/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/div[1]/a'
    driver.find_element_by_xpath(concert_path).click()

    time.sleep(2)

    all_handles = driver.window_handles
    ticket_handle = all_handles[-1]
    return ticket_handle


def buy_ticket(driver, ticket_handle, time_in):
    # 尝试到开售时间进行购买
    driver.switch_to.window(ticket_handle)

    print("请于开抢时间之前选择好要购买的票，不要关闭浏览器，脚本会自动在此界面抢票")

    buy_btn = driver.find_element_by_class_name("buybtn")
    while datetime.datetime.now().strftime('%H:%M:%S') != time_in:
        pass
    buy_btn.click()
    print("请付款")


city, concert, sale_time = concert_info_input()
d = webdriver.Chrome()
login_damai(d)
ticket_window = search_concert(d, city, concert)
buy_ticket(d, ticket_window, sale_time)
