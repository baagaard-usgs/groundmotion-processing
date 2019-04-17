#!/usr/bin/env python

import io
import re

import h5py

import pygments
import pygments.formatters
import pygments.lexers

from pygments.styles import get_style_by_name
from pygments.token import Token

from pygments.style import Style
class MyStyle(Style):
    default_style = ""
    native = get_style_by_name("native")
    styles = native.styles
    styles[Token.Comment] = "italic #bbbb00"
    styles[Token.Text] = "#ffffff"
    background_color = native.background_color

def create_formatter():
    #native = get_style_by_name("native")
    #native.styles[Token.Comment] = "italic #ff0000"
    formatter = pygments.formatters.ImageFormatter(
        style=MyStyle, image_format="png", font_size=18, line_numbers=False)
    return formatter
    

class H5App(object):

    @staticmethod
    def xml_to_png(xmlbytes, png_filename):

        REPLACE = [
            (">[\s]+<value>", "><value>"),
            ("</value>[\s]+</", "</value></"),
            ("\" xmlns:", "\"\n  xmlns:"),
        ]
        formatter = create_formatter()
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


class XMLApp(object):

    @staticmethod
    def xml_to_png(xml, png_filename):
        formatter = create_formatter()
        lexer = pygments.lexers.XmlLexer()
        pygments.highlight(xml, lexer, formatter, outfile=png_filename)
        return

    def run(self):
        with open("waveform_metrics.xml", "r") as fin:
            self.xml_to_png(fin.read(), "asdf_waveformmetricsxml.png")

        with open("station_metrics.xml", "r") as fin:
            self.xml_to_png(fin.read(), "asdf_stationmetricsxml.png")

        return


class PythonApp(object):

    @staticmethod
    def py_to_png(code, png_filename):
        formatter = create_formatter()
        lexer = pygments.lexers.PythonLexer()
        pygments.highlight(code, lexer, formatter, outfile=png_filename)
    
    def run(self):
        code = "\n".join([
            'import h5py',
            'with h5py.File("asdf_test.h5", "r") as h5:',
            '    acc_NZ_THZ_HN1 = h5["Waveforms"]["NZ.THZ"]["HN1"]["acc"][:]',
            ])
        self.py_to_png(code, "why_hdf5.png")

        code = "\n".join([
            '# Import earthquake metadata',
            'eqfile = os.path.join(EVENTID, "event.json")',
            'with open(eqfile, "r") as fin:',
            '    event = get_event_object(json.load(fin))',
            '',
            '# Import "raw" waveforms from CESMD',
            'datafiles = glob.glob(EVENTID+"/*.smc")',
            'raw_streams = []',
            'for dfile in datafiles:',
            '    raw_streams += read_data(dfile)',
            '',
            '# Import "raw" waveforms from NCEDC',
            'datafiles = glob.glob(EVENTID+"/*.mseed")',
            'for dfile in datafiles:',
            '    raw_streams += read_fdsn(dfile)',
            '',
            '# Write data to workspace',
            'workspace = StreamWorkspace(FILENAME)',
            'workspace.addStreams(event, raw_streams, label="raw")',
        ])
        self.py_to_png(code, "asdf_demo_import.png")

        code = "\n".join([
            '# Get raw waveforms from workspace',
            'workspace = StreamWorkspace.open(FILENAME)',
            'raw_streams = workspace.getStreams(EVENTID, labels=["raw"])',
            'event = workspace.getEvent(EVENTID)',
            '',
            '# Process waveforms',
            'processed_streams = process_streams(raw_streams, event, config=config)',
            'processed_streams.describe()',
            'workspace.addStreams(event, processed_streams, label="processed")',
            '',
            '# Set waveform metrics in workspace',
            'workspace.setStreamMetrics(EVENTID, labels=["processed"],',
            '    imclist=COMPONENT_METRICS, imtlist=INTENSITY_METRICS)',
        ])
        self.py_to_png(code, "asdf_demo_process.png")


        code = "\n".join([
            'workspace = StreamWorkspace.open(FILENAME)',
            '',
            '# Get earthquake event ids',
            'eventIds = workspace.getEventIds()',
            '',
            '# Get tags associated with earthquake id',
            'tags = workspace.getStreamTags(EVENTID)',
            '',
            '# Get processed streams',
            'processed_streams = workspace.getStreams(EVENTID, labels=["processed"])',
            '',
            '# Get waveform metrics for processed station NC.N016',
            'metrics_n016 = workspace.getStreamMetrics(EVENTID, station="NC.N016",',
            '    label=["processed"])',
        ])
        self.py_to_png(code, "asdf_demo_query.png")
                         
        return


if __name__ == "__main__":
    H5App().run()
    PythonApp().run()
    XMLApp().run()
