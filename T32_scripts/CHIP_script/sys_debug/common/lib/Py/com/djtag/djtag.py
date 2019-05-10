#!/usr/bin/python
# -*- coding: latin-1 -*- 
import logging
from config.debug import *
from lib.adaptor import *
#from ctypes import *
from config.JTAGAdaptor import *

class djtag(object):
    switch_port = 0
    port = 0
    jtag_port = 2
    default_ir_len = 9
    default_dr_len = 32
    def __init__(self, jtag = JTAG.Adaptor, p = 0, s_port = 4, jtag_p = 2, method = 1):
        self.method = method
        self.jtag = jtag
        self.port = p
        self.switch_port = s_port
        self.jtag_port = jtag_p
        self.switch(1)

    def destroy(self):
        #self.switch(0)
        pass


    def __shift(self, reg, data, need_update = 0, ir_len = default_ir_len, dr_len = default_dr_len):
        tap_instr = reg
        if 0 != need_update :
            tap_instr = reg | 0x100
        return self.jtag.jtag_shift(tap_instr, ir_len, dr_len, data)

    def __read(self, reg, ir_len = default_ir_len, dr_len = default_dr_len):
        data = 0
        return self.__shift(reg, data, 0, ir_len, dr_len)

    def __write(self, reg, data, ir_len = default_ir_len, dr_len = default_dr_len):
        return self.__shift(reg, data, 1, ir_len, dr_len)

    def switch(self, data):
        if self.method == 1:
            return self.switch_ext(data)
        else :
            return self.switch_api(data)
    
    def switch_ext(self, data):
        ret = self.jtag.t32_ext_djtag_switch(data)
        if adaptor.ADAPTOR_OK != ret :
            logging.warn("Please load the SPRD.t32 first!")
            raise
        return ret
        
    def switch_api(self, data):
        ret = self.jtag.jtag_ap_port(self.switch_port)
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        reg = 0x8
        #data = 0x1
        self.__write(reg, data)
        ret = self.__read(reg)
        '''WHY WHY WHY'''
        while (data != 0) and (data != ret):
            self.__write(reg, data)
            ret = self.__read(reg)
            logging.debug("switch is 0x%08x", ret)
        return adaptor.ADAPTOR_OK

    def switch_sys_dap(self, sys = 0, dap = 0):
        # Switch subsystem and sub DAP
        self.jtag.jtag_ap_trigger_reset()
        wdata = ((sys & 0xFF) << 8) | ((dap & 0xFF))
        self.__write(0x8, wdata)
        logging.debug("switch to sys&dap is 0x%04x", wdata)
        return adaptor.ADAPTOR_OK

    def execute(self, sys = 0, dap = 0, chan = 1, rnw = 1, data = 0, dr_len = default_dr_len, ir_len = default_ir_len):
        if self.method == 1:
            return self.execute_ext(sys, dap, chan, rnw, data, dr_len, ir_len)
        else :
            return self.execute_api(sys, dap, chan, rnw, data, dr_len, ir_len)

    def execute_ext(self, sys = 0, dap = 0, chan = 1, rnw = 1, data = 0, dr_len = default_dr_len, ir_len = default_ir_len):
        return self.jtag.t32_ext_djtag_run(sys, dap, chan, rnw, data, dr_len)

    def execute_api(self, sys = 0, dap = 0, chan = 1, rnw = 1, data = 0, dr_len = default_dr_len, ir_len = default_ir_len):
        logging.debug("subsystem = %d, subdap = %d, chain = %d, ir lenght = %d, dr lenght = %d", sys, dap, chan, ir_len, dr_len)
        ret = self.jtag.jtag_ap_port(self.port)
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        ret = self.switch_sys_dap(sys, dap)
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        if 0 == rnw :
            logging.debug("write 0x%08x", data)
            ret = self.__write(chan, data, ir_len, dr_len)
            self.__read(1)
            logging.debug("read is 0x%08x", self.__read(chan, ir_len, dr_len))
            data = ret
        else:
            data = self.__read(chan, ir_len, dr_len)
            logging.debug("read 0x%08x", data)
        return data
    
    def switch_test(self, sys = 0, dap = 0):
        self.jtag.jtag_ap_port(self.port)
        self.jtag.jtag_ap_trigger_reset()
        default = self.__read(0x8)
        logging.debug("the default is 0x%08x", default)
        wdata = ((sys & 0xFF) << 8) | ((dap & 0xFF))
        self.__write(0x8, wdata)
        readout = self.__read(0x8)
        if default == readout :
            logging.error("Write test error! 0x%08x", readout)
        self.jtag.jtag_ap_trigger_reset()
        readout = self.__read(0x8)
        if default !=  readout:
            logging.error("Switch test error! 0x%08x", readout)
        logging.debug("Switch test pass!")


if __name__ == "__main__" :
    dj = djtag()
    dap = 3
    sys = 0
    chan = 0xD
    wr_test = 0xFAF5A55A
    try:
        dj.switch_test()
        print("0x%08x" %(dj.execute(sys ,dap, 2)))
        print("0x%08x" %(dj.execute(sys ,dap, 1)))
        print("0x%08x" %(dj.execute(sys ,dap, 2)))
        print("0x%08x" %(dj.execute(sys ,dap, chan)))
        dj.execute(sys ,dap, chan, 0, wr_test)
        print("0x%08x" %(dj.execute(sys ,dap, chan)))
        if wr_test != dj.execute(sys ,dap, chan) :
            logging.error("test failed!")
    except:
        pass
    finally:
        dj.destroy()
    print("Test Done")
