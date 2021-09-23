import logging
import time
import unittest
import random

import requests
from parameterized import parameterized

from api.loginAPI import loginAPI
from utils import assert_utils, read_imgVerify_data, read_register_data, read_param_data


class login(unittest.TestCase):
    phone1 = '16611111121'
    phone2 = '16611111122'
    phone3 = '16611111123'
    phone4 = '16611111124'
    imgCode = '8888'
    password = "s123456"
    invite_phone = "19146864686"
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()
    def tearDown(self) -> None:
        self.session.close()

    # @parameterized.expand(read_imgVerify_data("imgVerify.json"))
    @parameterized.expand(read_param_data("imgVerify.json", "test_get_img_verify_code", "type,status_code"))
    def test01_get_img_code_random_float(self, type, status_code):
        r = ''
        if type == 'float':
            r = str(random.random())
        elif type == 'int':
            r = str(random.randint(1000000, 5000000))
        elif type == 'char':
            r = ''.join(random.sample('abcdefghijklmn',8))
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, r)
        logging.info('r = {} response = {}'.format(r, response))
        # 接收接口的返回结果，进行断言
        self.assertEqual(status_code, response.status_code)
    # 参数为随机整数时获取图片验证码成功
    def test02_get_img_code_random_int(self):
        # 定义参数（随机整数）
        r = random.randint(1000000, 2000000)
        # 调用接口类中的发送图片验证接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，并进行断言
        self.assertEqual(200, response.status_code)

    # 参数为空时，获取图片验证码失败
    def test03_get_img_code_param_is_null(self):
        # 定义参数（参数为空）
        # 调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session, "")
        # 接收接口返回的结果
        self.assertEqual(404, response.status_code)

    # 参数为字母时，获取图片验证码失败
    def test04_get_img_code_random_char(self):
        # 定义参数（参数为字母）
        r = random.sample("abcdefghijklmn", 8)
        rand = ''.join(r)
        logging.info(rand)
        # 调用接口类中的发送图片验证接口
        response = self.login_api.getImgCode(self.session, rand)
        # 接收接口的返回结果，并进行断言
        self.assertEqual(400, response.status_code)
    # 获取短信验证码成功-参数正确
    def test05_get_sms_code_succese(self):
        # 1、获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1,self.imgCode)
        logging.info("get sms code response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")

    # 获取短信验证码失败-图片验证码错误
    def test06_get_sms_code_wrong_img_code(self):
        #1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码失败
        error_code = "1234"
        response = self.login_api.getSmsCode(self.session, self.phone1, error_code)
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败-图片验证码为空
    def test07_get_sms_code_null_img_code(self):
        #1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码失败
        response = self.login_api.getSmsCode(self.session, self.phone1, "")
        logging.info("get sms code response={}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败-手机号码为空
    def test08_get_sms_code_null_phone(self):
        #1.获取图片验证码成功
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, "", self.imgCode)
        logging.info("get sms code response={}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 获取短信验证码失败-未调用图片验证码接口
    def test09_get_sms_code_no_img_code(self):
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response={}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 输入必填项，注册成功
    @parameterized.expand(read_register_data("register.json"))
    def test10_register_success_param_must(self,phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description):
        # 1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册成功
        response = self.login_api.register(session=self.session, phone=phone, password=password, verifycode=verifycode,phone_code=phone_code,dy_server=dy_server,invite_phone=invite_phone)
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, status_code, status, description)

    # 未填写邀请人，其他参数正确，注册成功
    def test11_register_success_no_invite_phone(self):
        #1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone2, imgVerifyCode=self.imgCode)
        assert_utils(self,response, 200, 200, "短信发送成功")
        # 3.注册成功
        response = self.login_api.register(session=self.session, phone=self.phone2, password=self.password)
        assert_utils(self, response, 200, 200,"注册成功")

    # 手机号码已存在，注册失败
    def test12_register_phone_is_exist(self):
        # 1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone2, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册成功
        response = self.login_api.register(session=self.session, phone=self.phone2, password=self.password)
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "手机已存在!")

    #手机号码为空，注册失败
    def test13_register_is_null(self):
        # 1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone3, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败
        response = self.login_api.register(session=self.session, phone="", password=self.password)
        logging.info("register response{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 密码为空，注册失败
    def test14_register_no_password(self):
        # 1.获取图片验证码
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone3, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败
        response = self.login_api.register(session=self.session, phone=self.phone3, password="")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    #图⽚验证码错误，注册失败
        # 1.获取图片验证码
    def test15_register_code_is_wrong(self):
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone4, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败
        response = self.login_api.register(session=self.session, phone=self.phone4, password=self.password, verifycode="1234")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误!")

    #图⽚验证码为空，注册失败
    def test16_register_code_is_null(self):
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone4, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败
        response = self.login_api.register(session=self.session, phone=self.phone4, password=self.password,
                                           verifycode="")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码不能为空!")

    #手机验证码错误，注册失败
    def test16_register_sms_code_is_wrong(self):
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone4, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败
        response = self.login_api.register(session=self.session, phone=self.phone4, password=self.password,
                                           verifycode=self.imgCode, phone_code="123456")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误")

    #手机验证码为空，注册失败
    def test17_register_sms_code_is_null(self):
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone4, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败2333333333333330
        response = self.login_api.register(session=self.session, phone=self.phone4, password=self.password,
                                           verifycode=self.imgCode, phone_code="")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "短信验证码不能为空")

    #未选择同意协议，注册失败
    def test18_register_no_dy_server(self):
        r = random.randint(1000000, 5000000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone=self.phone4, imgVerifyCode=self.imgCode)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败2333333333333330
        response = self.login_api.register(session=self.session, phone=self.phone4, password=self.password,
                                           verifycode=self.imgCode, dy_server="off")
        logging.info("register response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "请同意我们的条款")

    # 手机号码正确，登录成功
    def test19_login_success(self):
        response = self.login_api.login(self.session, phone=self.phone2, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

    # 手机号码不存在，登录失败
    def test20_login_no_phone(self):
        Wphone = "16666666666"
        response = self.login_api.login(self.session, phone=Wphone, password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "用户不存在")

    # 手机号码为空，登录失败
    def test21_login_phone_is_null(self):
        response = self.login_api.login(self.session, phone="", password=self.password)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "用户名不能为空")

    # 密码为空，注册失败
    def test22_login_password_id_null(self):
        response = self.login_api.login(self.session, phone=self.phone2, password="")
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")


    def test23_login_password_wrong(self):
        Wpassword = "error"
    # 密码错误1次，注册失败-密码错误1次,达到3次将锁定账户
        response = self.login_api.login(self.session, password=Wpassword)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
    # 密码错误2次，注册失败-密码错误2次,达到3次将锁定账户
        response = self.login_api.login(self.session, password=Wpassword)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
    # 密码错误3次，注册失败-由于连续输⼊错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录
        response = self.login_api.login(self.session, password=Wpassword)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        time.sleep(60)
        response = self.login_api.login(self.session)
        logging.info("login response{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")





