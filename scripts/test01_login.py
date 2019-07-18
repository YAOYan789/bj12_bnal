import os
import sys
sys.path.append(os.getcwd())
from tool.read_yaml import read_yaml
from page.page_in import PageIn
from tool.get_driver import GetDriver

import pytest
from page.page_login import PageLogin


def get_data():
    arrs = []
    for arr in read_yaml("login.yaml").values():
        arrs.append(tuple(arr.values()))
    return arrs


class TestLogin():
    # 初始化
    def setup_class(self):
        # 获取PageLogin对象
        self.login = PageIn().page_get_PageLogin()
        # 点击我
        self.login.page_click_me()
        # 点击已有账号去登录
        self.login.page_clicke_account_link()

    # 结束
    def teardown_class(self):
        #关闭driver
        GetDriver().quit_driver()

    @pytest.mark.parametrize("username,pwd,nickname,expect_toast", get_data())
    # 登录测试方法
    def test_login(self, username, pwd, nickname, expect_toast):
        # 调用登录业务方法
        self.login.page_login(username, pwd)
        # 如果是正向
        if nickname:
            try:
                # 断言昵称
                assert nickname == self.login.page_get_nickname()
            except:
                # 截图
                self.login.base_get_img()
            finally:
                # 退出登录
                self.login.page_logout()
                #点击我
                self.login.page_click_me()
                #点击已有账号，去登录
                self.login.page_clicke_account_link()
        # 否则逆向
        else:
            try:
                # 断言toast
                assert expect_toast in self.login.page_get_err_info(expect_toast)
            except:
                #截图并将截图写入报告
                self.login.base_get_img()
                raise