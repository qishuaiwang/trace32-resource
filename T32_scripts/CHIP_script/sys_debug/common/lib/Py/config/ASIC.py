#!/usr/bin/python
# -*- coding: latin-1 -*- 
'''
@author: ken.kuang
'''
import logging
from config.debug import *
import os
import xml.etree.ElementTree as ET
from com.djtag.djtag import djtag

import atexit
@atexit.register
def asic_goodbye():
    try:
        pass
    except:
        pass

class ASICConfig(object):
    def __init__(self, project = "Whale2"):
        the_path = os.path.split(os.path.realpath(__file__))
        self.tree = ET.parse(the_path[0] + "\\..\\projects\\" + project + "\\ASIC.xml")
        self.root = self.tree.getroot()
        project_name = self.root.attrib['project']
        if project_name != project :
            logging.error("mismatch the project name! expect %s, but %s", project, project_name)
            raise
        self.project = the_path[0] + "\\..\\projects\\" + project
        debug_file = self.project + "\\" + self.root.find('Debug').get('file')
        self.Debug = ET.parse(debug_file)

    def djtag_config(self):
        djtag_file = self.project + "\\" + self.root.find('DJTAG').get('file')
        self.DJTAG = ET.parse(djtag_file)
        dj_debug = self.DJTAG.find('Debug')
        self.djtag_cfg = dj_debug.text
        self.djtag_method = dj_debug.get('T32_EXT')
        if None == self.djtag_method :
            self.djtag_method = 0
        else:
            self.djtag_method = int(self.djtag_method)
        if 'DAP' == self.djtag_cfg :
            dap = self.Debug.find('DAP')
            dj = dap.find('DJTAG')
            self.djtag_port = int(dj.get('port'))
            jtag = dj.get('connect')
            self.djtag_switch_port = int(dap.find('DJTAG_Switch').get('port'))
            self.djtag_jtag_port = int(dap.find(jtag).get('port'))
        self.djtag_chanstart = int(self.DJTAG.find('CHANSTART').text)
        self.djtag_subsys = self.DJTAG.find('SubSystem')
        self.__subtree_expend(self.djtag_subsys, self.DJTAG)
        self.dj = djtag(method=self.djtag_method)
        self.dj_logger = debugConfig.get_logger('DJTAG')
        idc = self.DJTAG.find('IDCODE')
        idcode = int(idc.text, 16)
        ir = int(idc.get('IR'))
        exp_idcode = self.dj.execute(0, 0, ir)
        logging.debug("DJTAG IDCODE is 0x%08x", exp_idcode)
        if idcode != exp_idcode:
            logging.error("DJTAG IDCODE Doesn't match! readout is 0x%08x expect is 0x%08x", exp_idcode, idcode)

    def __bit_op(self, r, op, v):
        if 'AND' == op :
            r = r and v
        elif 'OR' == op :
            r = r or v
        return r

    def __tag_cloud_match(self, match_str, tag_cloud):
        #return False
        ret = True
        last_op = 'AND'
        for m in match_str.split() :
            if m.upper() in ('AND', 'OR') :
                last_op = m.upper()
            else :
                if -1 == tag_cloud.upper().find(m.upper()) :
                    ret = self.__bit_op(ret, last_op, False)
                else :
                    ret = self.__bit_op(ret, last_op, True)
                last_op = 'AND'    
        return ret

    def __tag_cloud_match_el(self, match_str, tag_cloud, el, new, end_tag, new_parent = None):
        ret = False
        local_tag_cloud = ""
        for child in el:
            str = child.get('tag_cloud')
            if None != str :
                local_tag_cloud = tag_cloud + str
            str =  child.get('name')
            if None != str :
                local_tag_cloud = local_tag_cloud + str
            if end_tag == child.tag :
                end_tag_cloud = local_tag_cloud
                end_tag_cloud += child.text + ";"
                if self.__tag_cloud_match(match_str, end_tag_cloud) :
                    node = ET.SubElement(new_parent, child.tag, child.attrib)
                    node.text = child.text
                    ret = True
            else:
                if self.__tag_cloud_match(match_str, local_tag_cloud) :
                    if new_parent == None :
                        new.append(child)
                    else :
                        new_parent.append(child)
                    ret = True
                else :
                    local_parent = ET.Element(child.tag, child.attrib)
                    ret_t = self.__tag_cloud_match_el(match_str, local_tag_cloud, child, new, end_tag, local_parent)
                    if  ret_t:
                        ret = True
                        if new_parent == None :
                            new.append(local_parent)
                        else :
                            new_parent.append(local_parent)
        return ret

    def __subtree_expend(self, el, root):
        for child in el:
            subtree_str = child.get('subtree')
            if None != subtree_str :
                subtree = root.find(subtree_str)
                child.append(subtree[0])
            self.__subtree_expend(child, root)

    def __djtag_dump(self, el, line = "", subsys = None, dap = None, chan = None, chan_data = None):
        #ET.dump(el)
        #return
        c_ssys = subsys
        c_dap = dap
        c_chan = chan
        c_data = chan_data
        local_line = "%s" % line
        table_str = "  "
        mux_sel_chan = 0
        mux_sel_dr_len = self.dj.default_dr_len
        mux_sel_def = 0
        for child in el:
            if child.tag == "DAP" :
                c_dap = int(child.get('sel'))
                if (dap == None) or (c_dap == dap) :
                    name = child.get('name')
                    if None == name :
                        self.dj_logger.info("%s[%s%2s]", local_line, child.tag, child.get('sel'))
                    else :
                        self.dj_logger.info("%s[%s%2s] %s", local_line, child.tag, child.get('sel'), name)
                    local_line += table_str
                    self.__djtag_dump(child, local_line, c_ssys, c_dap, c_chan)
                    local_line = "%s" % line
            elif child.tag == "CHAN" :
                c_chan = int(child.get('sel'))
                if (chan == None) or (c_chan == chan) :
                    mux_sel = child.get('mux_sel')
                    if mux_sel != None :
                        self.dj.execute(c_ssys, c_dap, mux_sel_chan + self.djtag_chanstart, 0, mux_sel_def|int(mux_sel), mux_sel_dr_len)
                    c_dr_len = child.get('dr_len')
                    if (c_dr_len == None) :
                        c_dr_len = self.dj.default_dr_len
                    else :
                        c_dr_len = int(c_dr_len)
                    c_data = self.dj.execute(c_ssys, c_dap, c_chan + self.djtag_chanstart, dr_len = c_dr_len)
                    name = child.get('name')
                    if None == name :
                        self.dj_logger.info("%s[%s%2s]: 0x%08x", local_line, child.tag, child.get('sel'), c_data)
                    else :
                        self.dj_logger.info("%s[%s%2s]: 0x%08x %s", local_line, child.tag, child.get('sel'), c_data, name)
                    local_line += table_str
                    self.__djtag_dump(child, local_line, c_ssys, c_dap, c_chan, c_data)
                    local_line = "%s" % line
            elif child.tag == "BIT" :
                bit_str = child.get('sel')
                try:
                    (bit_str_h, bit_str_l) = bit_str.split(':')
                    bit = int(bit_str_l)
                    bit_h = int(bit_str_h)
                except:
                    bit = int(bit_str)
                    bit_h = bit
                bit_val = (c_data>>bit)&((1<<(bit_h+1-bit))-1)
                self.dj_logger.info("%s[%s%5s]: 0x%08x %d {%s}", local_line, child.tag, bit_str, bit_val, bit_val, child.text)
            elif child.tag == "MUX_SEL" :
                mux_sel_chan = int(child.get('sel'))
                mux_sel_dr_len = child.get('dr_len')
                if (mux_sel_dr_len == None) :
                    mux_sel_dr_len = self.dj.default_dr_len
                else :
                    mux_sel_dr_len = int(mux_sel_dr_len)
                mux_sel_def = child.get('def_mux_sel')
                if (mux_sel_def == None) :
                    mux_sel_def = 0
                else :
                    mux_sel_def = int(mux_sel_def, 16)
            else :
                c_ssys = int(child.get('sel'))
                if (subsys == None) or (c_ssys == subsys) :
                    self.dj_logger.info(local_line + child.tag)
                    local_line += table_str
                    self.__djtag_dump(child, local_line, c_ssys, c_dap, c_chan)
                    local_line = "%s" % line
            

    def djtag_dump(self, match_str = "", subsys = None, dap = None, chan = None):
        dj = ET.Element(self.djtag_subsys.tag)
        self.__tag_cloud_match_el(match_str, "", self.djtag_subsys, dj, "BIT")
        self.__djtag_dump(dj, "", subsys, dap, chan)


def ASIC_test():
    logging.debug("Test")
    asic = ASICConfig()
    try :
        asic.djtag_config()
        asic.djtag_dump("busmon")
    finally:
        asic.dj.destroy()
    print("Test Done")

if __name__ == "__main__" :
    ASIC_test()
