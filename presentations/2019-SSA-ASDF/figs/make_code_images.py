#!/usr/bin/env python

import io
import re

import h5py

import pygments
import pygments.formatters
import pygments.lexers

class H5App(object):

    @staticmethod
    def xml_to_png(xmlbytes, png_filename):

        REPLACE = [
            (">[\s]+<value>", "><value>"),
            ("</value>[\s]+</", "</value></"),
            ("\" xmlns:", "\"\n  xmlns:"),
        ]

        formatter = pygments.formatters.ImageFormatter(
            style="native", image_format="png", font_size=18, line_numbers=False)
        lexer = pygments.lexers.XmlLexer()

        xml = xmlbytes.tostring().strip(b"\x00 ").strip()
        for current, new in REPLACE:
            xml = re.sub(current, new, xml)
        
        pygments.highlight(xml, lexer, formatter, outfile=png_filename)
        return

    def run(self):
        with h5py.File("asdf_test.h5", "r") as h5:
            self.xml_to_png(h5["QuakeML"][:], "asdf_quakeml.png")
            self.xml_to_png(h5["Provenance"]["hses_foo_nz_hses_hn1"][:], "asdf_provxml.png")
        return


class PythonApp(object):

    def run(self):
        code = "\n".join([
            'import h5py',
            'with h5py.File("asdf_test.h5", "r") as h5:',
            '    acc_NZ_THZ_HN1 = h5["Waveforms"]["NZ.THZ"]["HN1"]["acc"][:]',
            ])
        formatter = pygments.formatters.ImageFormatter(
            style="native", image_format="png", font_size=18, line_numbers=False)
        lexer = pygments.lexers.PythonLexer()
        pygments.highlight(code, lexer, formatter, outfile="why_hdf5.png")
        return


if __name__ == "__main__":
    H5App().run()
    PythonApp().run()
