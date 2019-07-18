import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Base:
    # 初始化
    @allure.step(title='正在 初始化driver')
    def __init__(self, driver):
        self.driver = driver

    # 查找元素
    @allure.step(title='正在查找元素')
    def base_find(self, loc, timeout=30, poll=0.5):
        allure.attach("查找的元素：", "{}".format(loc))
        return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until\
            (lambda x: x.find_element(*loc))

    # 查找一组元素
    @allure.step(title='正在查找元素')
    def base_finds(self, loc, timeout=30, poll=0.5):
        allure.attach("查找的元素：", "{}".format(loc))
        return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until\
            (lambda x: x.find_elements(*loc))

    # 点击方法
    @allure.step(title='正在点击操作')
    def base_click(self, loc):
        self.base_find(loc).click()

    # 输入方法
    @allure.step(title='正在输入操作')
    def base_input(self, loc, value):
        allure.attach("给{}元素输入：{}值".format(loc, value), " ")
        # 获取元素
        el = self.base_find(loc)
        # 清空操作
        el.clear()
        # 输入操作
        el.send_keys(value)

    # 获取文本
    @allure.step(title='正在获取文本操作')
    def base_get_text(self, loc):
        return self.base_find(loc).text

    # 获取toast消息
    @allure.step(title='正在获取toast消息操作')
    def base_get_toast(self, msg):
        loc = By.XPATH, "//*[contains(@text,'{}')]".format(msg)
        return self.base_find(loc, timeout=2, poll=0.2).text

    # 拖拽
    @allure.step(title='正在执行拖拽')
    def base_drag_and_drop(self, start_loc, end_loc):
        # 查找起点元素
        start_el = self.base_find(start_loc)
        # 查找结束元素
        end_el = self.base_find(end_loc)
        self.driver.drag_and_drop(start_el, end_el)

    # 截图
    @allure.step(title='正在截图操作')
    def base_get_img(self):
        self.driver.get_screenshot_as_file("./image/file.png")
        # 将图片写入报告
        self.base_write_allure()

    # 将图片写入allure报告
    @allure.step(title='正在写入报告')
    def base_write_allure(self, title="断言失败原因："):
        with open("./image/fail.png", "rb")as f:
            allure.attach(title, f.read(), allure.attach_type.PNG)

    # 根据文本获取元素并点击
    @allure.step(title='根据文本点击元素')
    def base_text_click(self, text):
        allure.attach("查找元素中包含：{} 文字的元素，并进行点击".format(text)," ")
        loc = By.XPATH, "//*[contains(@text,'{}')]".format(text)
        self.base_find(loc).click()
