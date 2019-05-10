#!/usr/bin/python
# -*- coding: latin-1 -*- 
'''
@author: ken.kuang
'''


class debugConfig(object):
    DumpPath = ""
    formatter = ""
    @staticmethod
    def get_logger(subname):
        logger = logging.getLogger('DebugDump.' + subname)
        fh = logging.FileHandler(debugConfig.DumpPath + subname + ".log", 'w')
        fh.setLevel(logging.INFO)
        fh.setFormatter(debugConfig.formatter)
        logger.addHandler(fh)
        return logger

try:
    a = this_debug_logging_is_configured
except:
    this_debug_logging_is_configured = 0

if this_debug_logging_is_configured == 0 :
    this_debug_logging_is_configured = 1
    import os
    import xml.etree.ElementTree as ET
    the_path = os.path.split(os.path.realpath(__file__))
    tree = ET.parse(the_path[0] + "\\debug.xml")
    root = tree.getroot()
    logfile = root.find('logfile').text
    format_str = root.find('format').text
    datefmt_str = root.find('date_format').text
    debugConfig.DumpPath = root.find('dumppath').text
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format=format_str,
                        datefmt=datefmt_str,
                        filename=logfile,
                        filemode='w'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.WARN)
    #console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_str, datefmt_str)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.debug("logging basicConfig")
    logger = logging.getLogger('DebugDump')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    debugConfig.formatter = logging.Formatter('%(message)s')
    ch.setFormatter(debugConfig.formatter)
    logger.addHandler(ch)
