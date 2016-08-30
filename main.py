########### Python 2.7 #############
#! python
from helper import *
import bean
import json, copy, falcon

class Resource(object):
	def on_get(self, req, resp):
		######################################################################
		ans = []
		#temp = json.loads(req.stream.read())
		#input = [temp[0], temp[1]]
		id1 = req.get_param_as_int('id1', True)
		id2 = req.get_param_as_int('id2', True)
		input = [id1, id2]
		flag = judge(input)
		if not flag:
			resp.status = falcon.HTTP_200
			resp.body = '[]'
			return


		if flag[0] == 'Id' and flag[1] == 'Id':
			#onehop
			params = bean.Params().sta_params('Id=' + str(input[0]))#params for search
			entities_1 = (json.loads(reqAPI(params)))['entities'][0]
			for v in entities_1['RId']:
				if v == input[1] and input not in ans:
					ans.append(input)
					break
					
			#twohop
			Fs_1, Cs_1, Js_1, AAs_1 = [], [], [], []
			if 'F' in entities_1: Fs_1 = entities_1['F']
			if 'C' in entities_1: Cs_1 = entities_1['C']
			if 'J' in entities_1: Js_1 = entities_1['J']
			if 'AA' in entities_1: AAs_1 = entities_1['AA']
			
			entities_2_ids = []
			for v in entities_1['RId']:
				params = bean.Params().sta_params('Id=' + str(v))
				temp = json.loads(reqAPI(params))
				entities_2_ids.append(copy.copy(temp['entities']))
				RIds_2_temp = temp['entities'][0]['RId']
				for w in RIds_2_temp:
					if w == input[1] and [input[0], v, input[1]] not in ans:
						ans.append([input[0], v, input[1]])
						
			params = bean.Params().sta_params('Id=' + str(input[1]))
			data_n1_id = json.loads(reqAPI(params))#n represent 'negative', backforward
			entities_n1 = data_n1_id['entities'][0]
			Fs_n1, Cs_n1, Js_n1, AAs_n1 = [], [], [], []
			if 'F' in entities_n1: Fs_n1 = entities_n1['F']
			if 'C' in entities_n1: Cs_n1 = entities_n1['C']
			if 'J' in entities_n1: Js_n1 = entities_n1['J']
			if 'AA' in entities_n1: AAs_n1 = entities_n1['AA']
			Ids_n1_R, Fs_n1_R, Cs_n1_R, Js_n1_R, AAs_n1_R = [], [], [], [], []
			params = bean.Params().sta_params('RId=' + str(input[1]))
			entities_n1_R = (json.loads(reqAPI(params)))['entities']
			for v in entities_n1_R:
				Ids_n1_R += v['Id'],
				if 'F' in v:
					for w in v['F']:
						Fs_n1_R += w['FId'],
				if 'C' in v: Cs_n1_R += v['C']['CId'],
				if 'J' in v: Js_n1_R += v['J']['JId'],
				if 'AA' in v:
					for w in v['AA']:
						AAs_n1_R += w['AuId'],
			
			for v in Fs_1:
				for w in Fs_n1:
					if v['FId'] == w['FId'] and [input[0], v['FId'], input[1]]:
						ans.append([input[0], v['FId'], input[1]])
			if Cs_1 and Cs_n1 and Cs_1['CId'] == Cs_n1['CId'] and [input[0], Cs_1['CId'], input[1]] not in ans:
				ans.append([input[0], Cs_1['CId'], input[1]])
			if Js_1 and Js_n1 and Js_1['JId'] == Js_n1['JId'] and [input[0], Js_1['JId'], input[1]] not in ans:
				ans.append([input[0], Js_1['JId'], input[1]])
			for v in AAs_1:
				for w in AAs_n1:
					if v['AuId'] == w['AuId'] and [input[0], v['AuId'], input[1]] not in ans:
						ans.append([input[0], v['AuId'], input[1]])
						
			#threehop
			Ids_2s, Fs_2s, Cs_2s, Js_2s, AAs_2s = [], [], [], [], []
			for entities_2_id in entities_2_ids:
				if 'Id' in entities_2_id[0]: Ids_2s += entities_2_id[0]['Id'],
				if 'F' in entities_2_id[0]: 
					for v in entities_2_id[0]['F']:
						Fs_2s += v['FId'],
				if 'C' in entities_2_id[0]: Cs_2s += entities_2_id[0]['C']['CId'],
				if 'J' in entities_2_id[0]: Js_2s += entities_2_id[0]['J']['JId'],
				if 'AA' in entities_2_id[0]: 
					for v in entities_2_id[0]['AA']:
						AAs_2s += v['AuId'],
			for nv in Ids_n1_R:
				for v in Ids_2s:
					if v == nv:
						for entities_2_id in entities_2_ids:
							for w in entities_2_id[0]['RId']:
								if w == v and [input[0],entities_2_id[0]['Id'], v, input[1]] not in ans:
									ans += [input[0],entities_2_id[0]['Id'], v, input[1]],
			for entities_2_id in entities_2_ids:
				if 'F' in entities_2_id[0]: 
					for v in entities_2_id[0]['F']:
						for nv in Fs_n1_R:
							if v['FId'] == nv and [input[0], entities_2_id[0]['Id'], nv, input[1]] not in ans:
								ans += [input[0], entities_2_id[0]['Id'], nv, input[1]],
				if 'AA' in entities_2_id[0]: 
					for v in entities_2_id[0]['AA']:
						for nv in AAs_n1_R:
							if v['AuId'] == nv and [input[0], entities_2_id[0]['Id'], nv, input[1]] not in ans:
								ans += [input[0], entities_2_id[0]['Id'], nv, input[1]],
				if 'C' in entities_2_id[0]:
					for nv in Cs_n1_R:
						if entities_2_id[0]['C']['CId'] == nv and [input[0], entities_2_id[0]['Id'], nv, input[1]] not in ans:
							ans += [input[0], entities_2_id[0]['Id'], nv, input[1]],
				if 'J' in entities_2_id[0]:
					for nv in Js_n1_R:
						if entities_2_id[0]['J']['JId'] == nv and [input[0], entities_2_id[0]['Id'], nv, input[1]] not in ans:
							ans += [input[0], entities_2_id[0]['Id'], nv, input[1]],
				
			for v in Fs_1:
				for temp in entities_n1_R:
					if 'F' in temp:
						for w in temp['F']:
							if w['FId'] == v['FId'] and [input[0], v['FId'], temp['Id'], input[1]] not in ans:
								ans += [input[0], v['FId'], temp['Id'], input[1]],
			if Cs_1:
				for temp in entities_n1_R:
					if 'C' in temp and Cs_1['CId'] == temp['C']['CId'] and [input[0], Cs_1['CId'], temp['Id'], input[1]] not in ans:
						ans += [input[0], Cs_1['CId'], temp['Id'], input[1]],
			if Js_1:
				for temp in entities_n1_R:
					if 'J' in temp and Js_1['JId'] == temp['J']['JId'] and [input[0], Js_1['JId'], temp['Id'], input[1]] not in ans:
						ans += [input[0], Js_1['JId'], temp['Id'], input[1]],
			
			for v in AAs_1:
				for temp in entities_n1_R:
					if 'AA' in temp:
						for w in temp['AA']:
							if w['AuId'] == v['AuId'] and [input[0], v['AuId'], temp['Id'], input[1]] not in ans:
								ans += [input[0], v['AuId'], temp['Id'], input[1]],
			
			
		elif flag[0] == 'Id' and flag[1] == 'AA.AuId':
			#onehop
			params = bean.Params().sta_params('Id=' + str(input[0]))
			data_1_id = json.loads(reqAPI(params))
			entities_1 = data_1_id['entities'][0]
			AAs_1 = []
			if 'AA' in entities_1: AAs_1 = entities_1['AA']
			for v in AAs_1:
				if v['AuId'] == input[1] and input not in ans:
					ans.append(input)
					break
			
			#twohop
			Fs_1, Cs_1, Js_1, RIds_1 = [], [], [], []
			if 'F' in entities_1: Fs_1 = entities_1['F']
			if 'C' in entities_1: Cs_1 = entities_1['C']
			if 'J' in entities_1: Js_1 = entities_1['J']
			if 'RId' in entities_1: RIds_1 = entities_1['RId']
			
			entities_2_ids = []
			for v in RIds_1:
				params = bean.Params().sta_params('Id=' + str(v))
				temp = json.loads(reqAPI(params))
				entities_2_ids.append(copy.copy(temp['entities'][0]))
				for w in entities_2_ids[-1]['AA']:
					if w['AuId'] == input[1] and [input[0], v, input[1]] not in ans:
						ans.append([input[0], v, input[1]])
			
			params = bean.Params().sta_params('Composite(AA.AuId=' + str(input[1]) + ')')
			entities_n1 = (json.loads(reqAPI(params)))['entities']
			for entity_n1 in entities_n1:
				for entity_2 in entities_2_ids:
					for v in entity_2['RId']:
						if v == entity_n1['Id'] and [input[0], entity_2['Id'], v, input[1]] not in ans:
							ans += [input[0], entity_2['Id'], v, input[1]],
				if 'AA' in entity_n1:
					for w in entity_n1['AA']:
						for v in AAs_1:
							if v['AuId'] == w['AuId'] and [input[0], v['AuId'], entity_n1['Id'], input[1]] not in ans:
								ans += [input[0], v['AuId'], entity_n1['Id'], input[1]],
				if 'F' in entity_n1:
					for w in entity_n1['F']:
						for v in Fs_1:
							if v['FId'] == w['FId'] and [input[0], v['FId'], entity_n1['Id'], input[1]] not in ans:
								ans += [input[0], v['FId'], entity_n1['Id'], input[1]],
				if 'C' in entity_n1:
					if 'CId' in Cs_1 and Cs_1['CId'] == entity_n1['C']['CId'] and [input[0], Cs_1['CId'], entity_n1['Id'], input[1]] not in ans:
						ans += [input[0], Cs_1['CId'], entity_n1['Id'], input[1]],
				if 'J' in entity_n1:
					if 'JId' in Js_1 and Js_1['JId'] == entity_n1['J']['JId'] and [input[0], Js_1['JId'], entity_n1['Id'], input[1]] not in ans:
						ans += [input[0], Js_1['JId'], entity_n1['Id'], input[1]],
				if 'AA' in entities_1 and 'AA' in entity_n1:
					for AA_temp in entities_1['AA']:
						for AA_n_temp in entity_n1['AA']:
							if 'AfId' in AA_temp and 'AfId' in AA_n_temp and AA_temp['AfId'] == AA_n_temp['AfId'] and [input[0], AA_temp['AuId'], AA_n_temp['AfId'], input[1]] not in ans:
								ans += [input[0], AA_temp['AuId'], AA_n_temp['AfId'], input[1]],
			
		elif flag[0] == 'AA.AuId' and flag[1] == 'Id':
			#onehop
			params = bean.Params().sta_params('Composite(AA.AuId=' + str(input[0]) + ')')
			data_1_auid = json.loads(reqAPI(params))
			entities_1 = data_1_auid['entities']
			for entity in entities_1:
				if entity['Id'] == input[1] and input not in ans:
					ans.append(input)
					break
			#twohop
			for entity in entities_1:
				for v in entity['RId']:
					if v == input[1] and [input[0], entity['Id'], input[1]] not in ans:
						ans += [input[0], entity['Id'], input[1]],
			
			#threehop
			params = bean.Params().sta_params('RId=' + str(input[1]))
			entities_n1_R = (json.loads(reqAPI(params)))['entities']
			params = bean.Params().sta_params('Id=' + str(input[1]))
			entities_n1 = (json.loads(reqAPI(params)))['entities']
			for entity in entities_1:
				for entity_n in entities_n1_R:
					for v in entity['RId']:
						if v == entity_n['Id'] and [input[0], entity['Id'], v, input[1]] not in ans:
							ans += [input[0], entity['Id'], v, input[1]],
			for entity in entities_1:
				for entity_n in entities_n1:
					if 'F' in entity and 'F' in entity_n:
						for v in entity['F']:
							for w in entity_n['F']:
								if v['FId'] == w['FId'] and [input[0], entity['Id'], v['FId'], input[1]] not in ans:
									ans += [input[0], entity['Id'], v['FId'], input[1]],
					if 'AA' in entity and 'AA' in entity_n:
						for v in entity['AA']:
							for w in entity_n['AA']:
								if v['AuId'] == w['AuId'] and [input[0], entity['Id'], v['AuId'], input[1]] not in ans:
									ans += [input[0], entity['Id'], v['AuId'], input[1]],
					if 'C' in entity and 'C' in entity_n:
						if entity['C']['CId'] == entity_n['C']['CId'] and [input[0], entity['Id'], entity['C']['CId'], input[1]] not in ans:
							ans += [input[0], entity['Id'], entity['C']['CId'], input[1]],
					if 'J' in entity and 'J' in entity_n:
						if entity['J']['JId'] == entity_n['J']['JId'] and [input[0], entity['Id'], entity['J']['JId'], input[1]] not in ans:
							ans += [input[0], entity['Id'], entity['J']['JId'], input[1]],
					if 'AA' in entity and 'AA' in entity_n:
						for v in entity['AA']:
							for w in entity_n['AA']:
								if 'AfId' in v and 'AfId' in w and v['AfId'] == w['AfId'] and [input[0], v['AfId'], w['AuId'], input[1]] not in ans:
									ans += [input[0], v['AfId'], w['AuId'], input[1]],

		else:
			#onehop
			pass
			#twohop
			params = bean.Params().sta_params('Composite(AA.AuId=' + str(input[0]) + ')')
			entities_1 = (json.loads(reqAPI(params)))['entities']
			params = bean.Params().sta_params('Composite(AA.AuId=' + str(input[1]) + ')')
			entities_n1 = (json.loads(reqAPI(params)))['entities']
			for entity in entities_1:
				if 'AA' in entity:
					for v in entity['AA']:
						if v['AuId'] == input[1] and [input[0], entity['Id'], input[1]] not in ans:
							ans += [input[0], entity['Id'], input[1]],
				for entity_n in entities_n1:
					if 'AA' in entity and 'AA' in entity_n:
						for v in entity['AA']:
							for w in entity_n['AA']:
								if 'AfId' in v and 'AfId' in w and v['AuId'] == input[0] and w['AuId'] == input[1] and v['AfId'] == w['AfId'] and [input[0], v['AfId'], input[1]] not in ans:
									ans += [input[0], v['AfId'], input[1]],
			#threehop
			for entity in entities_1:
				for entity_n in entities_n1:
					for v in entity['RId']:
						if v == entity_n['Id'] and [input[0], entity['Id'], v, input[1]] not in ans:
							ans += [input[0], entity['Id'], v, input[1]],

		####################################
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = str(ans)
# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
go = Resource()

# things will handle all requests to the '/things' URL path
app.add_route('/search', go)