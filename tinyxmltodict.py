#!/usr/bin/python

#####       Written by John W Kerns        #####
#####      http://blog.packetsar.com       #####
#####    https://github.com/packetsar/     #####

##################################### T I N Y   X M L T O D I C T #####################################
#######################################################################################################

##### Skinny XML to Python dictionary converter which works in Python2 or Python3 and requires NO non-native libraries/modules #####
##### Works with simple XML elements and attributes. XML attributes are preserved by nesting them in another dictionary #####
##### Input argument "inputdata" (str) can be either a file path, or a string of XML data; the method detects which is used #####
##### Output is a formatted python dictionary of the XML data #####

import xml.etree.ElementTree # Built in module for parsing the XML elements

##### Self-recursive method for XML conversion #####
def tinyxmltodict_recurse(node):
	attributekey = "attributes" # Set the dictionary key name which will store XML attributes
	if len(node.getchildren()) == 0 and len(node.items()) == 0: # If there are no more child elements, and no element attributes
		result = node.text # Set the element text as the result and return it
	else: # If there are children and/or attributes
		result = {} # Start with empty dict
		if len(node.items()) > 0: # If attributes exist for the element
			result.update({attributekey: {}}) # Create a nested dictionary which will store the attribute(s)
			result[attributekey].update(dict(node.items())) # Add the attributes to attribute dictionary
		for child in node: # For each child of this element node
			if child.tag not in list(result): # If this child element does not have an existing key
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
#>>> tinyxmltodict('''<food greens="yes"><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''') # Parsing direct XML input
#
#
############ Used as a module ############
#>>> import tinyxmltodict as txd # Import the module
#>>> txd.tinyxmltodict('/root/somefile.xml') # Parsing Linux/Unix file
#>>> txd.tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml') # Parsing Windows file (Use double-slashes)
#>>> txd.tinyxmltodict('''<food greens="yes"><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''') # Parsing direct XML input
#
#######################################################################################################
#######################################################################################################



##################################### T I N Y   D I C T T O X M L #####################################
#######################################################################################################

##### Skinny Python dictionary to XML converter which works in Python2 or Python3 and requires NO non-native libraries/modules #####
##### Works with nested dictionaries, lists, and strings. Other data types may not work properly #####
##### Input argument "dictdata" (dict) should be a dictionary (with one key) containing lists, dictionaries, and strings as the values #####
##### Output is an unformatted string of XML. The 'formatxml' method can be used to format the XML and make it pretty to print and read #####

import xml.etree.ElementTree # Built in module for parsing the XML elements

def tinydicttoxml_recurse(node, dictdata):
	attributekey = "attributes" # Set the dictionary key name you used to store XML attributes
	for element in dictdata: # For each element in the input dictionary
		if element == attributekey: # If this dictionary key matches the key used to store XML element attributes
			for attribute in dictdata[element]: # For each attribute in the dictionary
				node.set(attribute, dictdata[element][attribute]) # Set the attribute for the element
		elif type(dictdata[element]) == type(""): # If this value is a string
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
	if type(dictdata) != type({}) or len(list(dictdata)) > 1: # If the input is not a dict or has multiple keys
		dictdata = {"root": dictdata} # Nest it in a new dictionary with one key named 'root'
	xmlroot = xml.etree.ElementTree.Element(list(dictdata)[0]) # Create the root element using the dict key as the tag
	tinydicttoxml_recurse(xmlroot, dictdata[list(dictdata)[0]]) # Run the recursive method to iterate the dictionary
	return xml.etree.ElementTree.tostring(xmlroot).decode('UTF-8') # Then return a string output of the assembled XML object

def formatxml_recurse(node):
	global currentindent,formatroot # Set indent length and text as global variables 
	currentindent += 1 # Add 1 to the indentation length
	nodenum = len(node.getchildren()) # Count the number of child elements in the current node
	if nodenum != 0: # If there are children
		for child in node.getchildren(): # For each child in the current node
			if child.text == None: # If the child element has no value data
				child.text = "\n" + currentindent * indenttext # Set the indent for the next grandchild element
			if nodenum == 1: # If this is the last child in the list of children
				child.tail = "\n" + (currentindent - 2) * indenttext # Set a shortened indent for the end of the parent tag
			else: # If this is not the last child in the list of children
				child.tail = "\n" + (currentindent - 1) * indenttext # Set a slightly shortened indent for the next child
			nodenum -= 1 # Subtract one from the number of children
			formatxml_recurse(child) # Reiterate the method on each child element
	currentindent -= 1 # Subtract one from the current indentation length
	return node

def formatxml(xmldata):
	global currentindent,indenttext # Set indent length and text as global variables
	##### Set XML formatting info #####
	indenttext = "\t" # Set the text to use for indenting here
	###################################
	currentindent = 1 # Initialize indentation as 1
	root = xml.etree.ElementTree.fromstring(xmldata) # Mount the XML data to an element tree as "root"
	root.text = "\n" + indenttext # Set initial indent of first child element
	result = xml.etree.ElementTree.tostring(formatxml_recurse(root)) # Set the result text by calling the recursive method
	del currentindent,indenttext # Delete the temporary indent variables
	return result.decode('UTF-8') # Return the formatted text decoded to UTF-8

########################################## USAGE AND EXAMPLES #########################################
#
############ Used natively in your code ############
#>>> somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}} # Create a dict
#>>> tinydicttoxml(somedict) # Convert above dict variable
#>>> print(formatxml(tinydicttoxml(somedict))) # Convert and print above XML in a pretty format
#
#>>> tinydicttoxml({'food': {'attributes': {'greens': 'yes'}, 'fru': 'Apple', 'veg': ['Arugula', 'Celery']}}) # Convert direct dict input
#>>> print(formatxml(tinydicttoxml({'food': {'attributes': {'greens': 'yes'}, 'fru': 'Apple', 'veg': ['Arugula', 'Celery']}}))) # Pretty print dict input
#
#
############ Used as a module ############
#>>> import tinyxmltodict as txd # Import the module
#>>> somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}} # Create a dict
#>>> txd.tinydicttoxml(somedict) # Convert above dict variable
#>>> print(txd.formatxml(txd.tinydicttoxml(somedict))) # Convert and print above XML in a pretty format
#
#>>> txd.tinydicttoxml({'food': {'attributes': {'greens': 'yes'}, 'fru': 'Apple', 'veg': ['Arugula', 'Celery']}}) # Convert direct dict input
#>>> print(txd.formatxml(txd.tinydicttoxml({'food': {'attributes': {'greens': 'yes'}, 'fru': 'Apple', 'veg': ['Arugula', 'Celery']}}))) # Convert and format direct input
#
#######################################################################################################
#######################################################################################################