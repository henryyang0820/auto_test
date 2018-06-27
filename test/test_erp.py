import os,time,unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config
from utils.log import logger

class TestErp(unittest.TestCase):
	user_access = ''
	loginUrl = Config().get('login_Url')
	base_path = os.path.dirname(os.path.abspath(__file__))+'\..'
	driver_path = os.path.abspath(base_path + '\drivers\chromedriver.exe')
	locator_username = (By.NAME,"userid")
	locator_pwd = (By.NAME,"pwd")
	locator_submit = (By.NAME,"Submit1")
	locator_name = (By.XPATH,'//*[@id="logo"]/table/tbody/tr/td[3]/div[1]/font')
	locator_xjxu = (By.XPATH, '//*[@id="dia-nq"]/div/div[2]/div[1]/div[1]/a')

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Chrome(executable_path=cls.driver_path)
		cls.driver.get(cls.loginUrl)
		# cls.driver.maximize_window()
		cls.driver.find_element(*cls.locator_username).send_keys('wuq')
		cls.driver.find_element(*cls.locator_pwd).send_keys('123456')
		cls.driver.find_element(*cls.locator_submit).click()
		cls.driver.implicitly_wait(3)
		cls.driver.switch_to.alert.accept()
		cls.driver.implicitly_wait(1)
		cls.driver.switch_to.frame(cls.driver.find_element_by_tag_name("frame"))
		# el = cls.driver.find_element(*cls.locator_name)
		# cls.assertEqual(el.text,'吴琼',msg='登录失败')
		#获取存在frame里的字符串
		cls.driver.switch_to.default_content()
		frame = cls.driver.find_element_by_tag_name("frame")
		src = frame.get_attribute('src')
		cls.user_access = str(src)[56:119]

	def setUp(self):
		print("setup当前driver的那么是=",self.driver.name)
	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()

	def tearDown(self):
		self.driver.switch_to.window(self.driver.window_handles[self.driver.window_handles.__len__() - 1])
		self.driver.close()
		""

	#验证资源管理
	def test_1_rm(self):
		self.open_zygl()
		locator_zygl = (By.XPATH, '/html/body/div[1]/div[1]/h3')
		zygl = self.driver.find_element(*locator_zygl)
		self.assertTrue('资源管理'==zygl.text, msg='打开资源管理失败')
		logger.info("打开了%s"%(zygl.text))

	#验证打开新建需求
	def test_2_demand(self):
		self.open_new_demand()
		create_zycb = self.driver.find_element(*self.locator_xjxu)
		self.assertTrue('创建资源成本项' == create_zycb.text, msg='打开新建需求页面失败')
		logger.info("打开了新建需求页面")
		locator_close = (By.XPATH,'//*[@id="dia-nq"]/div/div[2]/div[2]/div/a[1]')
		btn_close = self.driver.find_element(*locator_close)
		time.sleep(2)
		btn_close.click()
		time.sleep(2)

	def open_zygl(self):
		try:
		# 通过setup登录后获取session拼到项目看板URL里
			URL = 'http://172.16.250.150:6021/resourceManageClient/main?SID=%s{cn}LC{pc}C&SJXMBH=S201806-BJ-BJ-10-0006' % self.user_access
			js = " window.open('%s')" % (URL)
			print("open_zygl=",self.driver.name)
			#确保焦点在当前标签
			# self.driver.switch_to.window(self.driver.window_handles[self.driver.window_handles.__len__()-1])
			self.driver.execute_script(js)
			self.driver.implicitly_wait(1)
			# switch到目标标签页
			self.driver.switch_to.window(self.driver.window_handles[self.driver.window_handles.__len__()-1])
			# locator_fres = (By.XPATH, '//*[@id="nav-info"]/tbody/tr/td/div/ul[1]/li[3]/a')
			# self.driver.find_element(*locator_fres).click()
			# self.driver.implicitly_wait(2)
			# locator_res = (By.XPATH, '//*[@id="nav-info"]/tbody/tr/td/div/ul[1]/li[3]/ul/li[1]/a')
			# # driver.find_element(*locator_kw).send_keys('selenium 灰蓝')
			# self.driver.find_element(*locator_res).click()
			self.driver.implicitly_wait(3)
		except Exception as msg:
			print(msg)


	def open_new_demand(self):
		self.open_zygl()
		loctor_newdemand = (By.XPATH, '/html/body/div[7]/div/div/a[1]')
		new_sourse = self.driver.find_element(*loctor_newdemand)
		# self.driver.implicitly_wait(3)
		time.sleep(2)
		new_sourse.click()
		time.sleep(2)

if __name__ == '__main__':
	unittest.main()