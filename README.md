# tinyxmltodict
A Skinny XML to Python dictionary converter which works in Python2 or Python3 and requires **NO** non-native libraries/modules



###About
Tinyxmltodict was built to do XML conversions for simple data structures (like REST calls) whilst being very lightweight, portable, understandable, and requiring as few external dependencies as possible (you don't need to install any Python modules).

It works with simple XML element names and attributes. Some of the more complex XML formats may not work properly.



###Input, Output
The only argument "inputdata" should be a string and can be either a file path, or a string of XML data; the method automatically detects which was used (assuming you don't use "<" in your file names)

The output is a formatted python dictionary of the XML data



###Usage and Examples
Tinyxmltodict can be imported as a module (if that's how you want to do it), but was written to be easily copied and pasted into your own codebase (fewer files to manage). Use it however you like.


#####Direct in Code
\>>>`tinyxmltodict('/root/somefile.xml')` # Parsing Linux/Unix file directly

\>>>`tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml')` # Parsing Windows file directly (Use double-slashes)

\>>>`tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''')` # Parsing direct XML input


#####As a Module
\>>>`import tinyxmltodict as txd` # Import the module

\>>>`txd.tinyxmltodict('/root/somefile.xml')` # Parsing Linux/Unix file directly

\>>>`txd.tinyxmltodict('C:\\Users\\Public\\Desktop\\somefile.xml')` # Parsing Windows file directly (Use double-slashes)

\>>>`txd.tinyxmltodict('''<food><veg>Arugula</veg><veg>Celery</veg><fru>Apple</fru></food>''')` # Parsing direct XML input
