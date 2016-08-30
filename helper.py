import httplib, urllib, base64, json
import bean

def reqAPI(params):
	"""request for API"""
	conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
	conn.request("GET", "/academic/v1.0/evaluate?%s" % urllib.urlencode(params), '', {})
	response = conn.getresponse()
	data = response.read()
	conn.close()
	return data

def judge(ids):
	"""judge types of two given ids, Id or AA.AuId"""
	ids1, ids2 = ids[0], ids[1]
	flag1 = flag2 = 'AA.AuId'
	
	params = bean.Params().judge_params('Id=' + str(ids1))
	data1 = reqAPI(params)
	data1_json = json.loads(data1)
	if not data1_json['entities']:
		print 'input error'
		return []
	if 'Ti' in data1_json['entities'][0]:
		flag1 = 'Id'
	
	params = bean.Params().judge_params('Id=' + str(ids1))
	params['expr'] = 'Id=' + str(ids2)
	data2 = reqAPI(params)
	data2_json = json.loads(data2)
	if not data2_json['entities']:
		print 'input error'
		return []
	if 'Ti' in data2_json['entities'][0]:
		flag2 = 'Id'
		
	return [flag1, flag2]
