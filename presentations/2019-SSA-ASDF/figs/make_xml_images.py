import io
import h5py

import pygments
import pygments.formatters
import pygments.lexers

with h5py.File("asdf_test.h5", "r") as h5:

    events = h5["QuakeML"][:]

xml = events.tostring().strip(b"\x00 ").strip()
# <element>\n WHITESPACE<value> -> <element><value>
# </value>\n WHITESPACE</element> -> </value></element>

formatter = pygments.formatters.ImageFormatter(style="native", image_format="png", font_size=18, line_numbers=False)
lexer = pygments.lexers.XmlLexer()
with open("eqsrc.png", "w") as fout:
    fout.write(pygments.highlight(xml, lexer, formatter))
1
