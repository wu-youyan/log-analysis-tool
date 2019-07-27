# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch


class Elastic(object):
	"""docstring for Elastic"""
	def __init__(self, arg):
		super(Elastic, self).__init__()
		self.arg = arg
		esConfig = [{'host':arg['host'],'port':arg['port']}]
		self.es = Elasticsearch(esConfig)

	#创建索引
	def createIndex(self, indexName):
		print(self.arg)
		res = self.es.indices.create(index=indexName, ignore=400)
		return res
	#创建索引
	def deleteIndex(self, indexName):
		res = self.es.indices.delete(index=indexName, ignore=400)
		return res
	#根据ID创建文档
	def createDocById(self, index, docType, id, data):
		res = self.es.create(index=index, doc_type=docType, id=id, body=data)
		return res
	#创建文档
	def createDoc(self, index, docType, data):
		res = self.es.index(index=index, doc_type=docType, body=data)
		return res
	#根据ID修改文档
	def updateDocById(self, index, docType, id, data):
		res =self.es.update(index=index, doc_type=docType, body=data, id=id)
		return res
	#删除文档
	def deleteDoc(self, index, docType, data):
		res =self.es.delete(index=index, doc_type=docType, body=data)
		return res