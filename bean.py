class Paper(object):
	def __init__(self, Id, F_FId, C_CId, J_JId, AA_AuId, AA_AFId):
		self.Id = Id
		self.F_FId = F_FId
		self.C_CId = C_CId
		self.J_JId = J_JId
		self.AA_AuId = AA_AuId
		self.AA_AFId = AA_AFId
	
class Params(object):
	def __init__(self):
		self.base_params = {
			# Request parameters
			'expr': '',
			'model': 'latest',
			'count': '',
			'offset': '0',
			'orderby': '',
			'attributes': '',
			'subscription-key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
		}
	def sta_params(self, expr):
		self.base_params = {
			# Request parameters
			'expr': expr,
			'model': 'latest',
			'count': '1000',
			'offset': '0',
			'orderby': '',
			'attributes': 'Id,RId,F.FId,C.CId,J.JId,AA.AuId,AA.AfId',
			'subscription-key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
		}
		return self.base_params
	def judge_params(self, expr):
		self.base_params = {
			# Request parameters
			'expr': expr,
			'model': 'latest',
			'count': '',
			'offset': '0',
			'orderby': '',
			'attributes': 'Ti',
			'subscription-key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
		}
		return self.base_params