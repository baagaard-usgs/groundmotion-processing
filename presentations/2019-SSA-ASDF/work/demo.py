#!/usr/bin/env python

import os
import json
import glob
import warnings

from gmprocess.io.asdf.stream_workspace import StreamWorkspace
from gmprocess.io.read import read_data
from gmprocess.event import get_event_object
from gmprocess.io.fdsn.core import read_fdsn
from gmprocess.processing import process_streams
from gmprocess.config import get_config

from h5py.h5py_warnings import H5pyDeprecationWarning

FILENAME = "southnapa_demo.h5"
EVENTID = "nc72282711"
COMPONENT_METRICS = ["channels", "rotd50", "rotd100"]
INTENSITY_METRICS = ["pga", "pgv", "sa1.0", "arias"]

config = get_config()

warnings.filterwarnings("ignore", category=H5pyDeprecationWarning)


def data_import():

    # Import earthquake metadata
    eqfile = os.path.join(EVENTID, "event.json")
    with open(eqfile, "r") as fin:
        event = get_event_object(json.load(fin))

    # Import "raw" waveforms from CESMD
    datafiles = glob.glob(EVENTID+"/*.smc")
    raw_streams = []
    for dfile in datafiles:
        raw_streams += read_data(dfile)

    # Import "raw" waveforms from NCEDC
    datafiles = glob.glob(EVENTID+"/*.mseed")
    for dfile in datafiles:
        raw_streams += read_fdsn(dfile)

    # Write data to workspace
    workspace = StreamWorkspace(FILENAME)
    workspace.addStreams(event, raw_streams, label="raw")

    return


def process_waveforms():

    # :KLUDE: process_streams() takes event dict not ObsPy Event
    eventfile = os.path.join(EVENTID, "event.json")
    with open(eventfile, "r") as fin:
        event_dict = json.load(fin)

    # Get raw waveforms from workspace    
    workspace = StreamWorkspace.open(FILENAME)
    raw_streams = workspace.getStreams(EVENTID, labels=["raw"])
    event = workspace.getEvent(EVENTID)

    # Process waveforms
    processed_streams = process_streams(raw_streams, event_dict, config=config)
    processed_streams.describe()
    workspace.addStreams(event, processed_streams, label="processed")

    # Set waveform metrics in workspace
    workspace.setStreamMetrics(EVENTID, labels=["processed"], imclist=COMPONENT_METRICS, imtlist=INTENSITY_METRICS)
    
    return


def query():
    
    workspace = StreamWorkspace.open(FILENAME)
    print("Workspace contains earthquakes: {}".format(workspace.getEventIds()))

    print("Stream tags in workspace: {}".format(workspace.getStreamTags(EVENTID)))
    print("Processing labels in workspace: {}".format(workspace.getLabels()))
    
    stream_nc_n016 = workspace.getStreams(EVENTID, labels=["processed"])
    stream_nc_n016.describe()

    metrics_nc_n016 = workspace.getStreamMetrics(EVENTID, station="NC.N016", label=['processed'])
    return


if __name__ == "__main__":
    data_import()
    process_waveforms()
    query()
    
    
