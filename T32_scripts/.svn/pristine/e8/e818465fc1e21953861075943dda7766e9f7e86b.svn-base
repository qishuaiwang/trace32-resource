#!/usr/bin/python
# -*- coding: latin-1 -*- 
'''
@author: ken.kuang
'''
import logging
from config.debug import *
import xml.etree.ElementTree as ET
from ctypes import *


import atexit

@atexit.register
def goodbye():
    try :
        si.clean_up()
        logging.debug("goodbye JTAGAdaptor!")
        JTAG.Adaptor.destroy()
    except:
        pass

lock_name = ""
global si

class JtagConfig(object):
    def __init__(self):
        the_path = os.path.split(os.path.realpath(__file__))
        self.tree = ET.parse(the_path[0] + "\\JTAGAdaptor.xml")
        self.root = self.tree.getroot()
        self.select_adaptor = self.root.attrib['adaptor']
        select_config = self.root.attrib['config']
        for cfg in self.root.findall('config') :
            if self.select_adaptor == cfg.attrib['adaptor'] :
                self.config = cfg
            elif 'default' == cfg.attrib['adaptor'] :
                self.def_cfg = cfg
        self.default = self.config.findall('default')[0]
        self.select = self.config.findall('%s' % select_config)[0]
    
    def __get(self, tag):
        for child in self.select :
            if tag == child.tag :
                return child.text
        if self.default != self.select :
            for child in self.default :
                if tag == child.tag :
                    return child.text
        for child in self.def_cfg :
            if tag == child.tag :
                return child.text
        raise
    
    def get_port(self):
        return self.__get('port')
    def get_node(self):
        return self.__get('node')
    def get_packlen(self):
        return self.__get('packlen')
    def get_swd(self):
        return int(self.__get('swd'))
    def get_path(self):
        return self.__get('path').replace('\\', '/')
    def get_t32_ext(self):
        return self.__get('t32_ext').replace('\\', '/')


class JTAG(object) :
    Jcfg = JtagConfig()
    Adaptor = 0

def t32_api_connect(port="20000", node="localhost", packlen="1024"):
    logging.debug(node.encode('latin-1'))
    logging.debug(port.encode('latin-1'))
    logging.debug(packlen.encode('latin-1'))
    if t32.T32_OK != t32.api.T32_Config(b"NODE=", node.encode('latin-1')) :
        logging.error('invalid node: %s' %(node))
        raise
    if t32.T32_OK != t32.api.T32_Config(b"PACKLEN=", packlen.encode('latin-1')):
        logging.error('invalid packet length: %s' %(packlen))
        raise
    if t32.T32_OK != t32.api.T32_Config(b"PORT=", port.encode('latin-1')) :
        logging.error('port number %s not accepted' %(port))
        raise

    logging.debug('Connecting...')
    if t32.api.T32_Init()==t32.T32_OK:
        if t32.api.T32_Attach(1)==t32.T32_OK:
            logging.debug('Successfully established a remote connection with TRACE32 PowerView.')
        else :
            logging.error('Failed to established a remote connection with TRACE32 PowerView.')
            raise
    else :
        logging.error('Failed to initialize a remote connection with TRACE32 PowerView.')
        raise

def detect():
    mode = c_uint32(0)
    t32.api.T32_Cmd(b"EVAL ICD()")
    if t32.T32_OK == t32.api.T32_EvalGet(byref(mode)) :
        logging.debug("mode %d", mode.value)
    t32.is_icd = mode.value
    logging.debug("ICD %d", t32.is_icd)

if JTAG.Jcfg.select_adaptor == 'T32' :
# use the right JTAG.Adaptor selected by configuration file!
    from lib.T32ADAPTOR.t32_dap import t32_dap
    from lib.T32API.t32 import *
    import sys
    from lib.single_instance import *
    if 0 == t32.connected :
        t32.connected = 1
        lock_name = '%s_%s' %(JTAG.Jcfg.get_node(), JTAG.Jcfg.get_port())
        si = SingleInstance(lock_name)
        if si.is_running :
            logging.error('Maybe you run this more than once, please DO NOT do it')
            raise
        try:
            t32_api_connect(JTAG.Jcfg.get_port(), JTAG.Jcfg.get_node(), JTAG.Jcfg.get_packlen())
            JTAG.Adaptor = t32_dap(JTAG.Jcfg.get_swd())
            detect()
            if t32.is_icd :
                if JTAG.Adaptor.swd :
                    JTAG.Adaptor.send_cmd("SYStem.CONFIG.DEBUGPORTTYPE SWD")
                JTAG.Adaptor.detect_SWD()
                JTAG.Adaptor.send_cmd('SYStem.Mode.Prepare')
                JTAG.Adaptor.send_cmd('EXTension.CONFIG "%s"' % JTAG.Jcfg.get_t32_ext())
                #Reset previous configuration
                t32.api.T32_DirectAccessResetAll(t32.T32_DIRECTACCESS_HOLD)
                t32.api.T32_DirectAccessResetAll(t32.T32_DIRECTACCESS_RELEASE)
        
                JTAG.Adaptor.dap_init()
        except:
            logging.error("T32 connect error, exit!")
            raise
elif JTAG.Jcfg.select_adaptor == 'DS5' :
    pass
else :
    logging.error("Please select the right JTAG adaptor!")
    raise

def test_arm_idcode(wdata = 0):
    return JTAG.Adaptor.jtag_shift(0xE, 4, 32, wdata)

def test_dap_idcode():
    JTAG.Adaptor.switch_tap_config(JTAG.Adaptor.tap_of_dap)
    data = test_arm_idcode()
    logging.debug("The DAP IDCODE is 0x%08x", data)
    return data

def test_dap_tap_arm_idcode():
    JTAG.Adaptor.switch_tap_config(JTAG.Adaptor.tap_of_dap_jtagap)
    data = test_arm_idcode()
    logging.debug("The DAP TAP IDCODE is 0x%08x", data)
    return data

def test_dap_dp():
    JTAG.Adaptor.dap_dp_write(0x8, 0x00000000)
    data = JTAG.Adaptor.dap_dp_read(0x4)
    logging.debug("The DAP DP STAT is 0x%08x", data)
    data = JTAG.Adaptor.dap_dp_read(0x0)
    logging.debug("The DAP DP IDR is 0x%08x", data)
    return data

def test_dap_ap():
    for ap in range (0, 2):
        data = JTAG.Adaptor.dap_ap_read(ap, 0xFC)
        logging.debug("The DAP AP(%d) is 0x%08x", ap, data)
    return data

def test_dap_apb():
    data = JTAG.Adaptor.dap_apb_read(0x80000FFC)
    logging.debug("The DAP APB is 0x%08x", data)
    return data

def test_all():
    if (0 == JTAG.Adaptor.swd) and (0x5BA00477 != test_dap_idcode()) :
        logging.error("The DAP test failed!")
    if (0xB1 != test_dap_apb()):
        logging.error("The DAP APB test failed!")
    dp = test_dap_dp()
    if (1 == JTAG.Adaptor.swd) and (0x5BA02477 != dp) :
        logging.error("The DAP DP test failed!")
    test_dap_ap()

if __name__ == "__main__" :
    try :
        if t32.is_icd :
            #JTAG.Adaptor.tap_config(JTAG.Adaptor.tap_of_dap, t32.T32_DIRECTACCESS_TAP_IRPRE_UINT32, 0)
            #JTAG.Adaptor.tap_config(JTAG.Adaptor.tap_of_dap, t32.T32_DIRECTACCESS_TAP_IRPOST_UINT32, 10)
            #JTAG.Adaptor.tap_config(JTAG.Adaptor.tap_of_dap, t32.T32_DIRECTACCESS_TAP_DRPRE_UINT32, 0)
            #JTAG.Adaptor.tap_config(JTAG.Adaptor.tap_of_dap, t32.T32_DIRECTACCESS_TAP_DRPOST_UINT32, 2)
            JTAG.Adaptor.dap_apb_init()
            #test_dap_dp()
            test_all()
        else :
            JTAG.Adaptor.send_cmd("PRINT ICD()")
    finally:
        JTAG.Adaptor.destroy()
    print("Test Done")



