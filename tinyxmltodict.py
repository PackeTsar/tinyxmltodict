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







##################################### T I N Y   D I C T T O X M L #####################################
#######################################################################################################

##### Skinny Python dictionary to XML converter which works in Python2 or Python3 and requires NO non-native libraries/modules #####
##### Works with nested dictionaries, lists, and strings. Other data types may not work properly #####
##### Input argument "dictdata" (dict) should be a dictionary containing lists, dictionaries, and strings as the values #####
##### Output is an unformatted string of XML. The 'formatxml' method can be used to format the XML and make it pretty to print #####

import xml.etree.ElementTree # Built in module for parsing the XML elements

def tinydicttoxml_recurse(node, dictdata):
	for element in dictdata: # For each element in the input dictionary
		if type(dictdata[element]) == type(""): # If this value is a string
			newnode = xml.etree.ElementTree.SubElement(node, element) # Create a new XML subelement named by the input dict key
			newnode.text = dictdata[element] # And set the text of the element as the string value
		elif type(dictdata[element]) == type({}): # If this value is a dictionary
			newnode = xml.etree.ElementTree.SubElement(node, element) # Create a new XML subelement named by the dict key
			xml.etree.ElementTree.SubElement(newnode, tinydicttoxml_recurse(newnode, dictdata[element])) # And re-run the method with dict value as input
		elif type(dictdata[element]) == type([]): # If this value is a list
			for entry in dictdata[element]: # For each entry in the list
				if type(entry) == type({}): # If the list entry is a dict
					newnode = xml.etree.ElementTree.SubElement(node, element) # Create a new XML subelement named by the dict key
					xml.etree.ElementTree.SubElement(newnode, tinydicttoxml_recurse(newnode, entry)) # And re-run the method with list entry as input
				elif type(entry) == type(""):# If the list entry is a string
					newnode = xml.etree.ElementTree.SubElement(node, element) # Create a new XML subelement named by the input dict key
					newnode.text = entry # And set the element text as the string entry

def tinydicttoxml(dictdata):
	if type(dictdata) != type({}) or len(dictdata.keys()) > 1: # If the input is not a dict or has multiple keys
		dictdata = {"root": dictdata} # Nest it in a new dictionary with one key named 'root'
	xmlroot = xml.etree.ElementTree.Element(dictdata.keys()[0]) # Create the root element using the dict key as the tag
	tinydicttoxml_recurse(xmlroot, dictdata[dictdata.keys()[0]]) # Run the recursive method to iterate the dictionary
	return xml.etree.ElementTree.tostring(xmlroot) # Then return a string output of the assembled XML object

def formatxml_recurse(node):
	global currentindent,formatroot
	currentindent += 1
	nodenum = len(node.getchildren())
	if nodenum != 0:
		for child in node.getchildren():
			if child.text == None:
				child.text = "\n" + currentindent * indenttext
			if nodenum == 1:
				child.tail = "\n" + (currentindent - 2) * indenttext
			else:
				child.tail = "\n" + (currentindent - 1) * indenttext
			nodenum -= 1
			formatxml_recurse(child)
	currentindent -= 1
	return node

def formatxml(xmldata):
	global currentindent,indenttext
	##### Set XML formatting info #####
	indenttext = "\t"
	###################################
	currentindent = 1
	root = xml.etree.ElementTree.fromstring(xmldata)
	root.text = "\n" + indenttext
	result = xml.etree.ElementTree.tostring(formatxml_recurse(root))
	del currentindent,indenttext
	return result.decode('UTF-8')

########################################## USAGE AND EXAMPLES #########################################
#
############ Used natively in your code ############
#>>> somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}} # Create a dict
#>>> tinydicttoxml(somedict) # Convert above dict variable
#>>> print(formatxml(tinydicttoxml(somedict))) # Convert and print above XML in a pretty format
#
#>>> tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}}) # Convert direct dict input
#>>> print(formatxml(tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}}))) # Pretty print dict input
#
#
############ Used as a module ############
#>>> import tinyxmltodict as txd # Import the module
#>>> somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}} # Create a dict
#>>> txd.tinydicttoxml(somedict) # Convert above dict variable
#>>> print(txd.formatxml(txd.tinydicttoxml(somedict))) # Convert and print above XML in a pretty format
#
#>>> txd.tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}}) # Convert direct dict input
#>>> print(txd.formatxml(txd.tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}})))
#
#
#
#######################################################################################################
#######################################################################################################