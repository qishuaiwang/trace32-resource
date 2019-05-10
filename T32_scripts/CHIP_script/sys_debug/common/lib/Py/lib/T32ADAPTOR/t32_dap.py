#!/usr/bin/python
# -*- coding: latin-1 -*- 
import logging
from ctypes import *
from config.debug import *
from lib.T32API.t32 import *
from lib.adaptor import *

import atexit
@atexit.register
def t32_goodbye():
    try:
        pass
    except:
        pass


class t32_dap(adaptor):

    __tap_id = 0

    __dap_id = 0

    __apb_id = 0
    __ahb_id = 0
    __axi_id = 0

    swd = 0
    
    tap_of_dap_jtagap = [-1 for i in range(8)]
    
    latest_tap = -1

    TRST_OUT = (1 << 1)
    SRST_OUT = (1 << 0)

    @staticmethod
    def __get_tap_id():
        ret = t32_dap.__tap_id
        t32_dap.__tap_id+=1
        return ret

    @staticmethod
    def __get_dap_id():
        ret = t32_dap.__dap_id
        t32_dap.__dap_id+=1
        return ret

    @staticmethod
    def __get_apb_id():
        ret = t32_dap.__apb_id
        t32_dap.__apb_id+=1
        return ret

    @staticmethod
    def __get_ahb_id():
        ret = t32_dap.__ahb_id
        t32_dap.__ahb_id+=1
        return ret

    @staticmethod
    def __get_axi_id():
        ret = t32_dap.__axi_id
        t32_dap.__axi_id+=1
        return ret

    def destroy(self):
        if t32.is_icd :
            t32.api.T32_DirectAccessRelease()
        t32.api.T32_Exit()

    def __init__(self, s = 0):
        t32.api.T32_ParamFromUint32.restype = t32.T32_Param
        self.this_handle = t32.handler
        self.tap_of_dap = t32_dap.__get_tap_id()
        self.dap = t32_dap.__get_dap_id()
        t32_dap.swd = s

    def detect_SWD(self):
        '''API'''
        if 0 == t32_dap.swd :
            if 1 :
                res = t32.T32_Param(0)
                if t32.T32_OK == t32.api.T32_DirectAccessGetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_TAP), c_uint(self.tap_of_dap), c_int(t32.T32_DIRECTACCESS_SWD_UNIT32), byref(res)) :
                    if 0 != res.uint32 :
                        t32_dap.swd = 1
                else :
                    return self.__error_handler()
            else :
                debug_port_type = create_string_buffer(32)
                self.send_cmd("EVAL SYStem.CONFIG.DEBUGPORTTYPE()")
                if t32.T32_OK == t32.api.T32_EvalGetString(byref(debug_port_type)) :
                    logging.debug("DEBUGPORTTYPE = %s", debug_port_type.value)
                    if b'SWD' == debug_port_type.value :
                        t32_dap.swd = 1
                else :
                    return self.__error_handler()
            logging.debug("swd = %d", t32_dap.swd)
        return t32_dap.swd

    def tap_config(self, tap_id, the_id, para):
        return t32.api.T32_DirectAccessSetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_TAP), c_uint(tap_id), c_int(the_id), t32.api.T32_ParamFromUint32(c_int(para)))

    def switch_tap_config(self, tap_id):
        return self.tap_config(tap_id, t32.T32_DIRECTACCESS_TAP_CURRENTINSTANCE_UINT32, tap_id)
    
    def debug_port_driver(self, enable):
        '''SYStem.Mode.Prepare, so just return'''
        return
        if enable :
            cmd = c_uint8(t32.T32_TAPACCESS_nENOUT | t32.T32_TAPACCESS_SET_0)
        else :
            cmd = c_uint8(t32.T32_TAPACCESS_nENOUT | t32.T32_TAPACCESS_SET_1)
        val = c_uint8(0)
        return t32.api.T32_TAPAccessDirect(t32.handler, c_int(1), byref(cmd), byref(val))

    def __park_tap_config(self, tap_id, park_stat = t32.T32_TAPSTATE_SELECT_DR_SCAN):
        return self.tap_config(tap_id, t32.T32_DIRECTACCESS_TAP_PARKSTATE_UINT32, park_stat)
    
    def __jtag_ap_tap_config(self, core_port, the_id, para):
        return self.tap_config(self.tap_of_dap_jtagap[core_port], the_id, para)

    def __dap_tap_config(self, the_id, para):
        return self.tap_config(self.tap_of_dap, the_id, para)

    def __dap_config(self, the_id, para):
        return t32.api.T32_DirectAccessSetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_DAP), c_uint(self.dap), c_int(the_id), t32.api.T32_ParamFromUint32(c_int(para)))

    def __dap_apb_config(self, the_id, para):
        return t32.api.T32_DirectAccessSetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_APB), c_uint(self.apb_of_dap), c_int(the_id), t32.api.T32_ParamFromUint32(c_int(para)))

    def __dap_ahb_config(self, the_id, para):
        return t32.api.T32_DirectAccessSetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_AHB), c_uint(self.ahb_of_dap), c_int(the_id), t32.api.T32_ParamFromUint32(c_int(para)))

    def __dap_axi_config(self, the_id, para):
        return t32.api.T32_DirectAccessSetInfo(self.this_handle, c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_AXI), c_uint(self.axi_of_dap), c_int(the_id), t32.api.T32_ParamFromUint32(c_int(para)))

    def __error_handler(self, reterr):
        try:
            t32.api.T32_DirectAccessRelease()
            logging.exception("T32 basic error(%d)!", reterr)
        except:
            pass
        return adaptor.ADAPTOR_ERR

    def reset_tap_with_TRST(self, tap_id):
        '''API'''
        ret = self.switch_tap_config(tap_id)
        if adaptor.ADAPTOR_OK != ret :
            return self.__error_handler(ret)

        ret = t32.api.T32_TAPAccessJTAGResetWithTRST(self.this_handle, c_int(tap_id), c_int(-1), c_int(-1))
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def reset_tap(self, tap_id):
        '''API'''
        ret = self.switch_tap_config(tap_id)
        if adaptor.ADAPTOR_OK != ret :
            return self.__error_handler(ret)

        ret = t32.api.T32_TAPAccessJTAGResetWithTMS(self.this_handle, c_uint(tap_id))
        if t32.T32_OK != ret :
            if 1 :
                return self.__error_handler(ret)
            else :
                logging.error("It's a bug! need to fix it.")
        return adaptor.ADAPTOR_OK

    def dap_init(self, targetsel = None):
        '''API'''
        if t32_dap.swd == 0 :
            ret = self.__park_tap_config(self.tap_of_dap)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
    
            # 1. DAP
            ret = self.__dap_config(t32.T32_DIRECTACCESS_DAP_TAP_INSTANCE_UINT32, self.tap_of_dap)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)

        ret = self.__dap_config(t32.T32_DIRECTACCESS_DAP_SCAN_DAP_OPTION_UINT32, t32.T32_SCAN_DAP_OPTION_OUTBUFFER_IMMEDIATELY)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)

        if targetsel != None :
            ret = self.__dap_config(t32.T32_DIRECTACCESS_DAP_SWDP_TARGETSEL_UINT32, targetsel)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
        
        self.debug_port_driver(1)

        if 1 == t32_dap.swd :
            #Initialize SWD port
            ret = t32.api.T32_DAPAccessInitSWD(self.this_handle, c_uint(self.dap))
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
        else:
            ret = self.reset_tap(self.tap_of_dap)
            if adaptor.ADAPTOR_OK != ret :
                return adaptor.ADAPTOR_ERR
        return adaptor.ADAPTOR_OK

    def dap_apb_init(self):
        '''API'''
        try :
            a = self.apb_of_dap
        except:
            self.apb_of_dap = t32_dap.__get_apb_id()
        ret = self.__dap_apb_config(t32.T32_DIRECTACCESS_APB_DAP_INSTANCE_UINT32, self.dap)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def dap_apb_port(self, port = 1):
        '''API'''
        ret = self.__dap_apb_config(t32.T32_DIRECTACCESS_APB_DAPACCESSPORT_UINT32, port)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def dap_ahb_init(self, CortexM = 1):
        '''API'''
        try :
            a = self.ahb_of_dap
        except:
            self.ahb_of_dap = t32_dap.__get_ahb_id()
        ret = self.__dap_ahb_config(t32.T32_DIRECTACCESS_AHB_DAP_INSTANCE_UINT32, self.dap)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        if CortexM :
            ret = self.__dap_ahb_config(t32.T32_DIRECTACCESS_AHB_CORTEXM_UINT32, 1)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def dap_ahb_port(self, port = 3):
        '''API'''
        ret = self.__dap_ahb_config(t32.T32_DIRECTACCESS_AHB_DAPACCESSPORT_UINT32, port)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def dap_axi_init(self):
        '''API'''
        try :
            a = self.axi_of_dap
        except:
            self.axi_of_dap = t32_dap.__get_axi_id()
        ret = self.__dap_axi_config(t32.T32_DIRECTACCESS_AXI_DAP_INSTANCE_UINT32, self.dap)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def dap_axi_port(self, port = 0):
        '''API'''
        ret = self.__dap_axi_config(t32.T32_DIRECTACCESS_AXI_DAPACCESSPORT_UINT32, port)
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def jtag_ap_port(self, core_port = 0, jtag_port = 2):
        '''API'''
        l_tap = self.latest_tap
        if self.tap_of_dap_jtagap[core_port] < 0 :
            self.tap_of_dap_jtagap[core_port] = t32_dap.__get_tap_id()
            # 2. TAP access JTAGAP
            # 2.1 set the DAP for the JTAGAP_TAP
            ret = self.__jtag_ap_tap_config(core_port, t32.T32_DIRECTACCESS_TAP_DAP_INSTANCE_UINT32, self.dap)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)

            # 2.2 set the JTAG-AP port of DAP
            ret = self.__jtag_ap_tap_config(core_port, t32.T32_DIRECTACCESS_TAP_DAP_ACCESSPORT_UINT32, jtag_port)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)

            # 2.3 set the JTAGAP port of JTAG-AP
            ret = self.__jtag_ap_tap_config(core_port, t32.T32_DIRECTACCESS_TAP_DAP_JTAGACCESSPORTINDEX_UINT32, core_port)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
            
            self.debug_port_driver(1)

            ret = self.reset_tap(self.tap_of_dap_jtagap[core_port])
            if adaptor.ADAPTOR_OK != ret :
                return adaptor.ADAPTOR_ERR

        if l_tap != self.tap_of_dap_jtagap[core_port] :
            self.latest_tap = self.tap_of_dap_jtagap[core_port]

            ret = self.switch_tap_config(self.tap_of_dap_jtagap[core_port])
            if adaptor.ADAPTOR_OK != ret :
                return adaptor.ADAPTOR_ERR

        return adaptor.ADAPTOR_OK
    
    def jtag_ap_tap_system_reset(self, core_port):
        self.jtag_ap_port(core_port)
        val = c_uint8(0)

        cmd = c_uint8(t32.T32_TAPACCESS_nRESET | t32.T32_TAPACCESS_SET_0)
        ret = t32.api.T32_TAPAccessDirect(self.this_handle, c_int(1), byref(cmd), byref(val))
        if t32.T32_OK != ret :
            return self.__error_handler(ret)

        cmd = c_uint8(t32.T32_TAPACCESS_SLEEP_US)
        ret = t32.api.T32_TAPAccessDirect(self.this_handle, c_int(1), byref(cmd), byref(val))
        cmd = c_uint8(100)
        ret = t32.api.T32_TAPAccessDirect(self.this_handle, c_int(1), byref(cmd), byref(val))
        
        cmd = c_uint8(t32.T32_TAPACCESS_nRESET | t32.T32_TAPACCESS_SET_1)
        ret = t32.api.T32_TAPAccessDirect(self.this_handle, c_int(1), byref(cmd), byref(val))
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK
        

    def __dap_write(self, reg, val, is_ap = t32.T32_DAPACCESS_REGISTERSET_DP):
        #logging.debug("w reg = 0x%x, val = 0x%x, is_ap = %d", reg, val, is_ap)
        ret = t32.api.T32_DAPAccessScan(self.this_handle, c_uint(self.dap), c_int(is_ap), c_int(t32.T32_DAPACCESS_RW_WRITE), c_uint32(reg), c_uint32(val), c_uint32(0))
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def __dap_read(self, reg, is_ap = t32.T32_DAPACCESS_REGISTERSET_DP):
        val = c_uint32(0)
        #logging.debug("r reg = 0x%x, is_ap = %d", reg, is_ap)
        ret = t32.api.T32_DAPAccessScan(self.this_handle, c_uint(self.dap), c_int(is_ap), c_int(t32.T32_DAPACCESS_RW_READ), c_uint32(reg), c_uint32(0), byref(val))
        if t32.T32_OK != ret :
            return (adaptor.ADAPTOR_ERR, self.__error_handler(ret))
        return (val.value, adaptor.ADAPTOR_OK)

    def dap_dp_write(self, reg, val):
        '''API'''
        return self.__dap_write(reg>>2, val, t32.T32_DAPACCESS_REGISTERSET_DP)

    def dap_dp_read(self, reg):
        '''API'''
        (data, ret) = self.__dap_read(reg>>2, t32.T32_DAPACCESS_REGISTERSET_DP)
        if adaptor.ADAPTOR_OK != ret:
            logging.error("dap_dp_read error: reg is 0x%08x", reg)
        return data

    def dap_ap_write(self, port, reg, val):
        '''API'''
        ret = self.dap_dp_write(0x8, ((reg>>4)<<4) + ((port)<<24));
        if adaptor.ADAPTOR_OK != ret:
            return ret
        return self.__dap_write(reg>>2, val, t32.T32_DAPACCESS_REGISTERSET_AP)

    def dap_ap_read(self, port, reg):
        '''API'''
        ret = self.dap_dp_write(0x8, ((reg>>4)<<4) + ((port)<<24));
        if adaptor.ADAPTOR_OK != ret:
            return ret
        (data, ret) = self.__dap_read(reg>>2, t32.T32_DAPACCESS_REGISTERSET_AP)
        if adaptor.ADAPTOR_OK != ret:
            logging.error("dap_ap_read error: port is %d, reg is 0x%08x", port, reg)
        return data

    def __dap_ap_access_write(self, ap_type, bus_id, reg, val):
        ret = t32.api.T32_DAPAPAccessReadWrite(self.this_handle, c_int(ap_type), c_uint(bus_id), c_int(t32.T32_DAPAPACCESS_RW_WRITE), c_uint64(reg), byref(c_uint8(val)), c_uint(4), c_uint(4), c_int(0), c_uint32(0))
        if t32.T32_OK != ret :
            return self.__error_handler(ret)
        return adaptor.ADAPTOR_OK

    def __dap_ap_access_read(self, ap_type, bus_id, reg):
        val = c_uint32(0)
        ret = t32.api.T32_DAPAPAccessReadWrite(self.this_handle, c_int(ap_type), c_uint(bus_id), c_int(t32.T32_DAPAPACCESS_RW_READ), c_uint64(reg), byref(val), c_uint(4), c_uint(4), c_int(0), c_uint32(0))
        if t32.T32_OK != ret :
            return (adaptor.ADAPTOR_ERR, self.__error_handler(ret))
        return (val.value, adaptor.ADAPTOR_OK)

    def dap_apb_write(self, reg, val):
        '''API'''
        return self.__dap_ap_access_write(t32.T32_DIRECTACCESS_INSTANCETYPE_APB, self.apb_of_dap, reg, val)

    def dap_apb_read(self, reg):
        '''API'''
        (data, ret) = self.__dap_ap_access_read(t32.T32_DIRECTACCESS_INSTANCETYPE_APB, self.apb_of_dap, reg)
        if adaptor.ADAPTOR_OK != ret:
            logging.error("dap_apb_read error: reg is 0x%08x", reg)
        return data

    def dap_ahb_write(self, reg, val):
        '''API'''
        return self.__dap_ap_access_write(t32.T32_DIRECTACCESS_INSTANCETYPE_AHB, self.ahb_of_dap, reg, val)

    def dap_ahb_read(self, reg):
        '''API'''
        (data, ret) = self.__dap_ap_access_read(t32.T32_DIRECTACCESS_INSTANCETYPE_AHB, self.ahb_of_dap, reg)
        if adaptor.ADAPTOR_OK != ret:
            logging.error("dap_ahb_read error: reg is 0x%08x", reg)
        return data

    def dap_axi_write(self, reg, val):
        '''API'''
        return self.__dap_ap_access_write(t32.T32_DIRECTACCESS_INSTANCETYPE_AXI, self.axi_of_dap, reg, val)

    def dap_axi_read(self, reg):
        '''API'''
        (data, ret) = self.__dap_ap_access_read(t32.T32_DIRECTACCESS_INSTANCETYPE_AXI, self.axi_of_dap, reg)
        if adaptor.ADAPTOR_OK != ret:
            logging.error("dap_axi_read error: reg is 0x%08x", reg)
        return data

    def __dap_jtag_ap_sel(self, ap, sel):
        csw = 0x00
        psel = 0x04
        pre_sel = self.dap_ap_read(ap, psel)
        logging.debug("psel = 0x%08x", pre_sel)
        while (0!=(0xF0000000&self.dap_ap_read(ap, csw))) :
            pass
        ret = self.dap_ap_write(ap, psel, sel)
        if adaptor.ADAPTOR_OK != ret :
            return (adaptor.ADAPTOR_ERR, pre_sel)
        return (adaptor.ADAPTOR_OK, pre_sel)

    def jtag_ap_trigger_reset(self, jtag_port = 2, core_port = 0, reset = SRST_OUT, switch_port = 4):
        '''API'''
        csw = 0x00
        ap = jtag_port
        idr = self.dap_ap_read(ap, 0xFC)
        logging.debug("IDR = 0x%08x", idr)
        if ((idr & 0x0FFFFF0F) != 0x04760000) :
            return adaptor.ADAPTOR_ERR
        logging.debug("csw = 0x%08x", self.dap_ap_read(ap, csw))
        (ret, pre_sel) = self.__dap_jtag_ap_sel(ap, (1 << core_port) | (1 << switch_port))
        #(ret, pre_sel) = self.__dap_jtag_ap_sel(ap, (1 << core_port))
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        data = self.dap_ap_read(ap, csw)
        logging.debug("csw = 0x%08x", data)
        ret = self.dap_ap_write(ap, csw, (data | reset))
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        logging.debug("csw = 0x%08x", self.dap_ap_read(ap, csw))
        #for i in range(0, 1) :
        #    self.dap_ap_write(ap, csw, (data | reset))
        ret = self.dap_ap_write(ap, csw, (data & ~reset))
        if adaptor.ADAPTOR_OK != ret :
            return adaptor.ADAPTOR_ERR
        #for i in range(0, 1) :
        #    self.dap_ap_write(ap, csw, (data & ~reset))
        logging.debug("csw = 0x%08x", self.dap_ap_read(ap, csw))
        (ret, pre_sel) = self.__dap_jtag_ap_sel(ap, pre_sel)
        self.reset_tap(self.tap_of_dap_jtagap[core_port])
        return adaptor.ADAPTOR_OK
    
    def jtag_shift(self, instr, instr_len, data_len, wdata = 0):
        '''API'''
        #logging.debug("instr = 0x%08x wdata = 0x%08x ir = %d dr = %d", instr, wdata, instr_len, data_len)
        status = c_uint8(0)
        data = c_uint32(0)
        tap_instr = c_uint64(instr)
        write_data = c_uint64(wdata)
        if 1 :
            t32.api.T32_BundledAccessAlloc.restype = c_void_p
            t_handle = t32.api.T32_BundledAccessAlloc();
            ret = t32.api.T32_TAPAccessShiftIR(t_handle, c_int(instr_len), byref(tap_instr), byref(status))
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
            ret = t32.api.T32_TAPAccessShiftDR(t_handle, c_int(data_len), byref(write_data), byref(data))
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
            ret = t32.api.T32_BundledAccessExecute(t_handle, self.this_handle)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
            ret = t32.api.T32_BundledAccessFree(t_handle)
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
        else :
            ret = t32.api.T32_TAPAccessShiftIR(t32.T32_DIRECTACCESS_HOLD, c_int(instr_len), byref(tap_instr), byref(status))
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
            ret = t32.api.T32_TAPAccessShiftDR(self.this_handle, c_int(data_len), byref(write_data), byref(data))
            if t32.T32_OK != ret :
                return self.__error_handler(ret)
        return data.value

    def send_cmd(self, cmd):
        '''API'''
        ret = t32.api.T32_Cmd(cmd.encode('latin-1'))
        if t32.T32_OK == ret :
            return adaptor.ADAPTOR_OK
        return self.__error_handler(ret)
    
    def t32_ext_run(self, cmd = "DJTAG.VERSION()", len = 32):
        retval = 0
        temp = c_uint32(0)
        ret = self.send_cmd('EVAL %s' % cmd)
        if adaptor.ADAPTOR_OK != ret :
            return (self.__error_handler(ret), retval)
        if t32.T32_OK == t32.api.T32_EvalGet(byref(temp)) :
            retval = temp.value
        else :
            return (self.__error_handler(ret), retval)
        while (len > 32) :
            self.send_cmd('EVAL (Eval()>>32.)')
            if t32.T32_OK == t32.api.T32_EvalGet(byref(temp)) :
                retval |= (temp.value<<32)
            else :
                return (self.__error_handler(ret), retval)
            len -= 32
        return (adaptor.ADAPTOR_OK, retval)
    
    def t32_ext_djtag_run(self, sys = 0, dap = 0, chan = 1, rnw = 1, data = 0, len = 32):
        DJTAG_SYS_P_MASK=(0xFF)
        DJTAG_SYS_P_OFFSET=(24)
        DJTAG_DAP_P_MASK=(0xFF)
        DJTAG_DAP_P_OFFSET=(16)
        DJTAG_CHAN_P_MASK=(0xFF)
        DJTAG_CHAN_P_OFFSET=(8)
        DJTAG_R_NW_P_MASK=(0x1)
        DJTAG_R_NW_P_OFFSET=(7)
        DJTAG_DR_LEN_P_MASK=(0x7F)
        DJTAG_DR_LEN_P_OFFSET=(0)
        par_one = 0
        par_one |= ((sys&DJTAG_SYS_P_MASK)<<DJTAG_SYS_P_OFFSET)
        par_one |= ((dap&DJTAG_DAP_P_MASK)<<DJTAG_DAP_P_OFFSET)
        par_one |= ((chan&DJTAG_CHAN_P_MASK)<<DJTAG_CHAN_P_OFFSET)
        par_one |= ((rnw&DJTAG_R_NW_P_MASK)<<DJTAG_R_NW_P_OFFSET)
        par_one |= ((len&DJTAG_DR_LEN_P_MASK)<<DJTAG_DR_LEN_P_OFFSET)
        par_two=0x1200
        if rnw == 0 :
            self.send_cmd('D.S AVM:0x%x %%LE %%Quad 0x%x' % (par_two, data))
        (ret, rdata) = self.t32_ext_run("DJTAG.EXECUTE(0x%x,0x%x)" % (par_one, par_two), len)
        return rdata

    def t32_ext_djtag_switch(self, par_one, len = 32):
        (ret, rdata) = self.t32_ext_run("DJTAG.SWITCH(0x%x)" % (par_one), len)
        return ret

