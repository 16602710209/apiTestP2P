import logging
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils


class approve(unittest.TestCase):
    phone1 = "16611111111"
    phone2 = "16611111112"
    password = "s123456"
    realname = "长孙民绿"
    card_id = "51012919830119158X"
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 参数正确，实名认证成功
    def test01_approve_success(self):
        #1.登录
        response = self.login_api.login(self.session, phone=self.phone1, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证成功
        response = self.approve_api.approve(self.session, realname=self.realname, card_id=self.card_id)
        logging.info("approve response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "提交成功!")

    # 身份证号码错误，实名认证失败
    def test02_approve_cardId_is_wrong(self):
        WcardId = "510129198301191580"
        # 1.登录
        response = self.login_api.login(self.session, phone=self.phone2, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证失败
        response = self.approve_api.approve(self.session, realname=self.realname, card_id=WcardId)
        logging.info("approve response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "身份证号码错误")


    # 身份证号码为空，实名认证失败
    def test03_approve_cardId_is_null(self):
        # 1.登录
        response = self.login_api.login(self.session, phone=self.phone2, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证失败
        response = self.approve_api.approve(self.session, realname=self.realname, card_id="")
        logging.info("approve response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "身份证号不能为空")

    # 姓名错误，实名认证失败
    def test04_approve_realname_is_wrong(self):
        Wrealname = "长孙"
        # 1.登录
        response = self.login_api.login(self.session, phone=self.phone2, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证失败
        response = self.approve_api.approve(self.session, realname=Wrealname, card_id=self.card_id)
        logging.info("approve response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "姓名错误")

    #姓名为空，实名认证失败
    def test05_approve_realname_is_null(self):
        # 1.登录
        response = self.login_api.login(self.session, phone=self.phone2, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证失败
        response = self.approve_api.approve(self.session, realname="", card_id=self.card_id)
        logging.info("approve response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "姓名不能为空")

    def test06_get_approve(self):
        # 1.登录
        response = self.login_api.login(self.session, phone=self.phone1, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        # 2.认证失败
        response = self.approve_api.getApprove(self.session)
        logging.info("approve response{}".format(response.json()))
        self.assertEqual(200, response.status_code)