


import xml.etree.ElementTree
import re

def tinyxml2dict_recurse(node):
	if len(node.getchildren()) == 0:
		result = node.text
	else:
		result = dict()
		for child in node:
			if child.tag not in result.keys():
				result[child.tag] = tinyxml2dict(child)
			else:
				if type(result[child.tag]) != type([]):
					result[child.tag] = [result[child.tag], tinyxml2dict(child)]
				else:
					result[child.tag].append(tinyxml2dict(child))
	return result

##### Simple starter method for the XML to Dict conversion process #####
def tinyxml2dict(mode, input):
	if mode == "file":
		with open(input, 'r') as filetext:
			xmldata = filetext.read()
	elif mode == "string":
		xmldata = input
	regex = "(?s)<!--.*-->"
	configcomment = re.findall(regex, xmldata, flags=0)[0]
	cleanedxml = xmldata.replace(configcomment, "")
	root = xml.etree.ElementTree.fromstring(cleanedxml)
	return {root.tag: tinyxml2dict_recurse(root)}







