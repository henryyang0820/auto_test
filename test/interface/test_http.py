import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.config import  DATA_PATH

# urls = {'ERP_FIN_PC_YS': 'http://172.16.250.150:6027/health', 'ERP_FIN_SERVICE_YS': 'http://172.16.250.150:6028/health',
# 		'ERP_MAINSITE_SERVICE_YS': 'http://172.16.250.150:6030/health',
# 		'ERP_PM_SERVICE_YS': 'http://172.16.250.150:6026/health',
# 		'ERP_PM_WEBSITE_PC_YS': 'http://172.16.250.150:6025/health', 'ERP_PRM_PC_YS': 'http://172.16.250.150:6021/health',
# 		'ERP_PRM_SERVICE_YS': 'http://172.16.250.150:6022/health',
# 		'ERP_SUPPLIER_PC_YS': 'http://172.16.250.150:6023/health',
# 		'ERP_SUPPLIER_SERVICE_YS': 'http://172.16.250.150:6024/health','ERP_WF_SERVICE_PRM_YS':'http://172.16.250.150:6029/health'}

class TestPrmHTTP(unittest.TestCase):

	excel = DATA_PATH + '/prm.xlsx'

	def sub_setUp(self):
		''

	def sub_tearDown(self):
		''
	def test_prm_http(self):
		URLS = ExcelReader(self.excel).data
		for u in URLS:
			with self.subTest(url = u):
				self.sub_setUp()
				self.client = HTTPClient(url=u['url'], method='GET')
				res = self.client.send()
				logger.debug(res.text)
				self.assertEqual(res.json()['status'],'UP')

if __name__ == '__main__':
	report = REPORT_PATH + '\\report_interface.html'
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='接口自动化', description='接口报告')
		runner.run(TestPrmHTTP('test_prm_http'))