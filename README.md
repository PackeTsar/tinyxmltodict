# TinyXMLtoDict ![TinyXMLtoDict][logo]

A Skinny, XML to Python dictionary (and back) converter which works in Python2 or Python3 and requires **NO** non-native libraries/modules


###About
Tinyxmltodict (TXD) was built to do dictionary conversions to and from XML for simple data structures (like REST calls) whilst being very lightweight, portable, understandable, Python2 and Python3 compatible, and requiring as few external dependencies as possible (you don't need to install any external Python modules).

TXD works with simple XML element names and attributes. Some of the more complex and less used XML features may not work properly.

##XML-to-Dict Conversion

###Input, Output
The only argument "inputdata" should be a string and can be either a file path, or a string of XML data; the method automatically detects which is used.

The output is a formatted python dictionary of the XML data


###Usage and Examples
Tinyxmltodict (TXD) can be imported as a module (if that's how you want to do it), but was written to be easily copied and pasted into your own codebase (fewer files to manage). Use it however you like.


#####Direct in Code
\>>>`tinyxmltodict('/root/somefile.xml')` # Parsing Linux/Unix file

\>>>`tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml')` # Parsing Windows file (Use double-slashes)

\>>>`tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''')` # Parsing direct XML input


#####As a Module
\>>>`import tinyxmltodict as txd` # Import the module

\>>>`txd.tinyxmltodict('/root/somefile.xml')` # Parsing Linux/Unix file

\>>>`txd.tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml')` # Parsing Windows file (Use double-slashes)

\>>>`txd.tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''')` # Parsing direct XML input


##Dict-to-XML Conversion

###Input, Output

#####tinydicttoxml
The argument "dictdata" in the 'tinydicttoxml' method should be a dictionary (with one key for the root element) containing lists, dictionaries, and strings as the values. The output of that method is an unformatted XML string.

#####xmlformatter
The 'formatxml' method can be called in-line or after the creation of the XML string to format the XML string into properly indented and easily readable XML. The 'formatxml' method has only one input ('xmldata') and it returns the formatted XML string in unicode


###Usage and Examples
Tinydicttoxml, just like its counterpart, can be imported as a module (if that's how you want to do it), but was written to be easily copied and pasted into your own codebase (fewer files to manage). Use it however you like.


#####Direct in Code
\>>>`somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}}` # Create a dict

\>>>`tinydicttoxml(somedict)` # Convert above dict variable

\>>>`print(formatxml(tinydicttoxml(somedict)))` # Convert and print above XML in a pretty format


\>>>`tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}})` # Convert direct dict input

\>>>`print(formatxml(tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}})))` # Pretty print dict input


#####As a Module
\>>>`import tinyxmltodict as txd` # Import the module

\>>>`somedict = {'buy-stuff': {'bath': {'soap': ['shampoo', 'handsoap']}, 'bedroom': {'bed': 'sheets'}}}` # Create a dict

\>>>`txd.tinydicttoxml(somedict)` # Convert above dict variable

\>>>`print(txd.formatxml(txd.tinydicttoxml(somedict)))` # Convert and print above XML in a pretty format


\>>>`txd.tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}})` # Convert direct dict input

\>>>`print(txd.formatxml(txd.tinydicttoxml({'food': {'veg': ['Arugula', 'Celery'], 'fru': 'Apple'}})))` # Convert and format direct input


##Contributing
If you use TXD and find a bug, please report it as an issue on GitHub.

If you fork the repo and write a fix, submit a pull request so we can all benefit :)

[logo]: http://www.packetsar.com/wp-content/uploads/tinyxmltodict-tiny.png