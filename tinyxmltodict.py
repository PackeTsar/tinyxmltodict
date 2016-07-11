#!/usr/bin/python

#####       Written by John W Kerns        #####
#####      http://blog.packetsar.com       #####
#####    https://github.com/packetsar/     #####


##################################### T I N Y   X M L T O D I C T #####################################
#######################################################################################################

##### Skinny XML to Python dictionary converter which works in Python2 or Python3 and requires NO non-native libraries/modules #####
##### Works with simple XML element names and attributes. Some XML formats may not work properly #####
##### Input argument "inputdata" (str) can be either a file path, or a string of XML data; the method detects which is used #####
##### Output is a formatted python dictionary of the XML data #####

import xml.etree.ElementTree # Built in module for parsing the XML elements

##### Self-recursive method for XML conversion #####
def tinyxmltodict_recurse(node):
	if len(node.getchildren()) == 0 and len(node.items()) == 0: # If there are no more child elements, and no element attributes
		result = node.text # Set the element text as the result and return it
	else: # If there are children and/or attributes
		result = {} # Start with empty dict
		if len(node.items()) > 0: # If attributes exist for the element
			result.update(dict(node.items())) # Add the attributes to the result
		for child in node: # For each child of this element node
			if child.tag not in result.keys(): # If this child element does not have an existing key
				result[child.tag] = tinyxmltodict_recurse(child) # Add the key and iterate again
			else: # If this child element does have an existing key
				if type(result[child.tag]) != type([]): # And it is not already a list
					result[child.tag] = [result[child.tag], tinyxmltodict_recurse(child)] # Nest it in a list and iterate again
				else: # If it is already a list
					result[child.tag].append(tinyxmltodict_recurse(child)) # Append to that list
	return result

##### Simple starter method for the XML to Dict conversion process #####
def tinyxmltodict(inputdata):
	if "<" not in inputdata: # If the 'less than' symbol is not in the inputdata, it is likely a file path (don't use "<" in your file names, damnit!)
		with open(inputdata, 'r') as filetext: # Open file in read mode
			xmldata = filetext.read() # Suck in text of file
			filetext.close() # And close the file
	else: # If "<" is in the inputdata, then you are likely inputting XML data as a string
		xmldata = inputdata # So set the xmldata variable as your string input
	root = xml.etree.ElementTree.fromstring(xmldata) # Mount the root element
	return {root.tag: tinyxmltodict_recurse(root)} # Set root element name as key and start first iteration

########################################## USAGE AND EXAMPLES #########################################
#
############ Used natively in your code ############
#>>> tinyxmltodict('/root/somefile.xml') # Parsing Linux/Unix file
#>>> tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml') # Parsing Windows file (Use double-slashes)
#>>> tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''') # Parsing direct XML input
#
#
############ Used as a module ############
#>>> import tinyxmltodict as txd # Import the module
#>>> txd.tinyxmltodict('/root/somefile.xml') # Parsing Linux/Unix file
#>>> txd.tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml') # Parsing Windows file (Use double-slashes)
#>>> txd.tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''') # Parsing direct XML input
#
#######################################################################################################
#######################################################################################################







dictdata = {'loopback': {'units': {'entry': [{'ip': {'entry': {'name': '69.194.131.240/32'}}, 'adjust-tcp-mss': {'enable': 'no'}, 'name': 'loopback.22', 'interface-management-profile': 'PORTAL'}, {'ip': {'entry': {'name': '216.240.168.140/32'}}, 'name': 'loopback.23', 'interface-management-profile': 'PORTAL'}, {'ip': {'entry': {'name': '38.96.15.167/32'}}, 'name': 'loopback.24', 'interface-management-profile': 'PORTAL'}, {'ip': {'entry': {'name': '10.180.32.5/32'}}, 'name': 'loopback.25', 'interface-management-profile': 'PORTAL'}]}}}



dictdata = {'config': {'globalsettings': {'paths': {'logfile': '/etc/radiuid/radiuid.log', 'radiuslogpath': '/var/log/radius/radacct/'}, 'searchterms': {'ipaddressterm': 'Framed-IP-Address', 'usernameterm': 'User-Name', 'delineatorterm': 'Acct-Authentic'}, 'uidsettings': {'timeout': '70', 'userdomain': 'domain.com'}}, 'targets': {'target': [{'username': 'admin', 'password': 'admin', 'hostname': 'pan1.kernshosting.com', 'version': '7'}, {'username': 'admin', 'password': 'admin', 'hostname': '10.162.30.51', 'version': '7'}]}}}




def tinydicttoxml_recurse(node, dictdata):
	for element in dictdata:
		if type(dictdata[element]) == type(""):
			newnode = xml.etree.ElementTree.SubElement(node, element)
			newnode.text = dictdata[element]
		if type(dictdata[element]) == type({}):
			newnode = xml.etree.ElementTree.SubElement(node, element)
			xml.etree.ElementTree.SubElement(newnode, tinydicttoxml_recurse(newnode, dictdata[element]))







def tinydicttoxml(dictdata):
	for key in dictdata:
		currentroot = xml.etree.ElementTree.Element(key)
		tinydicttoxml_recurse(currentroot, dictdata[key])
	return xml.etree.ElementTree.tostring(currentroot)




