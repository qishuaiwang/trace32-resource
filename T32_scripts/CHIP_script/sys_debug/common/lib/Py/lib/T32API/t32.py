#!/usr/bin/python
# -*- coding: latin-1 -*- import logging
from ctypes import *
#logging.basicConfig(level=logging.DEBUG)

class t32(object):
    api = 0
    handler = 0
    connected = 0
    is_icd = 0
    delet_it = 0

    #from T32.h    
    T32_OK = 0
    #/* error codes by API client */
    T32_ERR_COM_RECEIVE_FAIL        = -1      #/* receiving API response failed */
    T32_ERR_COM_TRANSMIT_FAIL       = -2      #/* sending API message failed */
    T32_ERR_COM_PARA_FAIL           = -3      #/* function parameter error */
    T32_ERR_COM_SEQ_FAIL            = -4      #/* message sequence failed */
    T32_ERR_NOTIFY_MAX_EVENT        = -5      #/* max. notify events exceeded */
    T32_ERR_MALLOC_FAIL             = -6      #/* malloc() failed */
    #/* standard error codes */
    T32_ERR_STD_RUNNING             = 2       #/* target running */
    T32_ERR_STD_NOTRUNNING          = 3       #/* target not running */
    T32_ERR_STD_RESET               = 4       #/* target is in reset */
    T32_ERR_STD_ACCESSTIMEOUT       = 6       #/* access timeout, target running */
    T32_ERR_STD_INVALID             = 10      #/* not implemented */
    T32_ERR_STD_REGUNDEF            = 14      #/* registerset undefined */
    T32_ERR_STD_VERIFY              = 15      #/* verify error */
    T32_ERR_STD_BUSERROR            = 16      #/* bus error */
    T32_ERR_STD_NOMEM               = 22      #/* no memory mapped */
    T32_ERR_STD_RESETDETECTED       = 48      #/* target reset detected */
    T32_ERR_STD_FDXBUFFER           = 49      #/* FDX buffer error */
    T32_ERR_STD_RTCKTIMEOUT         = 57      #/* no RTCK detected */
    T32_ERR_STD_INVALIDLICENSE      = 60      #/* no valid license detected */
    T32_ERR_STD_CORENOTACTIVE       = 64      #/* core has no clock/power/reset in SMP */
    T32_ERR_STD_USERSIGNAL          = 67      #/* user signal */
    T32_ERR_STD_NORAPI              = 83      #/* tried to connect to emu */
    T32_ERR_STD_FAILED              = 113
    T32_ERR_STD_LOCKED              = 123     #/* access locked */
    T32_ERR_STD_POWERFAIL           = 128     #/* power fail */
    T32_ERR_STD_DEBUGPORTFAIL       = 140     #/* debug port fail */
    T32_ERR_STD_DEBUGPORTTIMEOUT    = 144     #/* debug port timeout */
    T32_ERR_STD_NODEVICE            = 147     #/* no debug device */
    T32_ERR_STD_RESETFAIL           = 161     #/* target reset fail */
    T32_ERR_STD_EMUTIMEOUT          = 162     #/* emulator communication timeout */
    T32_ERR_STD_NORTCK              = 164     #/* no RTCK on emulator */
    T32_ERR_STD_ATTACH              = 254     #/* T32_Attach() is missing */
    T32_ERR_STD_FATAL               = 255
    #/* function specific error codes */
    T32_ERR_FN1 = 90
    T32_ERR_FN2 = 91
    T32_ERR_FN3 = 92
    T32_ERR_FN4 = 93
    T32_ERR_GETRAM_INTERNAL         = 0x1000      #/* T32_GetRam failed internally */
    T32_ERR_READREGBYNAME_NOTFOUND  = 0x1010      #/* T32_ReadRegisterByName: register not found */
    T32_ERR_READREGBYNAME_FAILED    = 0x1011      #/* T32_ReadRegisterByName: reading register failed */
    T32_ERR_WRITEREGBYNAME_NOTFOUND = 0x1020      #/* T32_WriteRegisterByName: register not found */
    T32_ERR_WRITEREGBYNAME_FAILED   = 0x1021      #/* T32_WriteRegisterByName: reading register failed */
    T32_ERR_READREGOBJ_PARAFAIL     = 0x1030      #/* T32_ReadRegisterObj: wrong parameters */
    T32_ERR_READREGOBJ_MAXCORE      = 0x1031      #/* T32_ReadRegisterObj: max cores exceeded */
    T32_ERR_READREGOBJ_NOTFOUND     = 0x1032      #/* T32_ReadRegisterObj: register not found */
    T32_ERR_READREGSETOBJ_PARAFAIL  = 0x1033      #/* T32_ReadRegisterSetObj: wrong parameters */
    T32_ERR_READREGSETOBJ_NUMREGS   = 0x1034      #/* T32_ReadRegisterSetObj: number of read registers wrong */
    T32_ERR_WRITEREGOBJ_PARAFAIL    = 0x1040      #/* T32_WriteRegisterObj: wrong parameters */
    T32_ERR_WRITEREGOBJ_MAXCORE     = 0x1041      #/* T32_WriteRegisterObj: max cores exceeded */
    T32_ERR_WRITEREGOBJ_NOTFOUND    = 0x1042      #/* T32_WriteRegisterObj: register not found */
    T32_ERR_WRITEREGOBJ_FAILED      = 0x1043      #/* T32_WriteRegisterObj: writing register failed */
    T32_ERR_SETBP_FAILED            = 0x1050      #/* T32_WriteBreakpoint/T32_WriteBreakpointObj: setting breakpoint failed */
    T32_ERR_READMEMOBJ_PARAFAIL     = 0x1060      #/* T32_ReadMemoryObj: wrong parameters */
    T32_ERR_WRITEMEMOBJ_PARAFAIL    = 0x1070      #/* T32_WriteMemoryObj: wrong parameters */
    T32_ERR_READVAR_ALLOC           = 0x1080      #/* T32_ReadVariable*: mem alloc failed */
    T32_ERR_READVAR_ACCESS          = 0x1081      #/* T32_ReadVariable*: access to symbol failed */
    T32_ERR_READBPOBJ_PARAFAIL      = 0x1091      #/* T32_ReadBreakpointObj: wrong parameters */
    T32_ERR_READBPOBJ_NOTFOUND      = 0x1092      #/* T32_ReadBreakpointObj: breakpoint not found */
    T32_ERR_WRITEBPOBJ_FAILED       = 0x10a1      #/* T32_WriteBreakpointObj: setting BP failed */
    T32_ERR_MMUTRANSLATION_FAIL     = 0x10b0      #/* T32_QueryAddressObjMmuTranslation: translation failed */
    #/* legacy definitions */
    T32_COM_RECEIVE_FAIL    = T32_ERR_COM_RECEIVE_FAIL
    T32_COM_TRANSMIT_FAIL   = T32_ERR_COM_TRANSMIT_FAIL
    T32_COM_PARA_FAIL       = T32_ERR_COM_PARA_FAIL
    T32_COM_SEQ_FAIL        = T32_ERR_COM_SEQ_FAIL
    T32_MAX_EVENT_FAIL      = T32_ERR_NOTIFY_MAX_EVENT
    T32_MALLOC_FAIL         = T32_ERR_MALLOC_FAIL

   
    #/***********************/
    #/* basic API functions */
    #/***********************/
    
    T32_DEV_OS              = 0
    T32_DEV_ICE             = 1
    T32_DEV_ICD             = 1

    #T32EXTERN int  T32_Errno;
    #T32EXTERN int  T32_Config(const char *String1, const char *String2);
    #T32EXTERN int  T32_Init(void);
    #T32EXTERN int  T32_Attach(int DeviceSpecifier);
    #T32EXTERN int  T32_Terminate(int ShellReturnValue);
    #T32EXTERN int  T32_Exit(void);
    #T32EXTERN int  T32_Ping(void);
    #T32EXTERN int  T32_Nop(void);
    #T32EXTERN int  T32_NopEx(int length, int options);
    #T32EXTERN int  T32_NopFail(void);
    #T32EXTERN int  T32_Cmd(const char *Command);
    #T32EXTERN int  T32_Cmd_f(const char *command, ...) ATTRIBUTE_PRINTF(1, 2);
    #T32EXTERN int  T32_CmdWin(uint32_t WindowHandle, const char *Command);
    #T32EXTERN int  T32_Printf(const char *str, ...) ATTRIBUTE_PRINTF(1, 2);
    #T32EXTERN int  T32_Stop(void);
    #T32EXTERN int  T32_GetPracticeState(int *pPracticeState);
    #T32EXTERN int  T32_EvalGet(uint32_t *pEvaluationResult);
    #T32EXTERN int  T32_EvalGetString(char *EvaluationString);
    #T32EXTERN int  T32_GetMessage(char *AreaMessage, uint16_t *pMessageType);
    #T32EXTERN int  T32_GetTriggerMessage(char *TriggerMessage);
    #T32EXTERN int  T32_GetChannelSize(void);
    #T32EXTERN void T32_GetChannelDefaults(void *ParametersOut);
    #T32EXTERN void T32_SetChannel(void *ParametersIn);
    #T32EXTERN int  T32_APILock(int nTimeoutMS);                                                                                               /* preliminary*/
    #T32EXTERN int  T32_APIUnlock(void);
    #T32EXTERN int  T32_GetApiRevision(uint32_t* pRevNum);

    #/*******************************/
    #/* debug related API functions */
    #/*******************************/
    
    
    T32_MEMORY_ACCESS_DATA                   = 0x0000
    T32_MEMORY_ACCESS_PROGRAM                = 0x0001
    T32_MEMORY_ACCESS_USR                    = 0x000f
    T32_MEMORY_ACCESS_VM                     = 0x0010
    T32_MEMORY_ACCESS_ARM_CP0                = 0x0002
    T32_MEMORY_ACCESS_ARM_ICE                = 0x0003
    T32_MEMORY_ACCESS_ARM_ETM                = 0x0004
    T32_MEMORY_ACCESS_ARM_CP14               = 0x0005
    T32_MEMORY_ACCESS_ARM_CP15               = 0x0006
    T32_MEMORY_ACCESS_ARM_ARM                = 0x0007
    T32_MEMORY_ACCESS_ARM_THUMB              = 0x0008
    T32_MEMORY_ACCESS_ARM_PHYSICAL_ARM       = 0x0009
    T32_MEMORY_ACCESS_ARM_PHYSICAL_THUMB     = 0x000a
    T32_MEMORY_ACCESS_ARM_ETB                = 0x000b
    T32_MEMORY_ACCESS_ARM_PHYSICAL_DATA      = 0x000c
    T32_MEMORY_ACCESS_ARM_PHYSICAL_PROGRAM   = 0x000d
    T32_MEMORY_ACCESS_ARM_DAP                = 0x000e
    T32_MEMORY_ACCESS_ARM_USR                = T32_MEMORY_ACCESS_USR
    T32_MEMORY_ACCESS_ARM_DBG                = 0x0011
    T32_MEMORY_ACCESS_ARC_AUX                = 0x0002
    T32_MEMORY_ACCESS_PPC_SPR                = 0x0002
    T32_MEMORY_ACCESS_PPC_DCR                = 0x0003
    T32_MEMORY_ACCESS_X86_LD                 = 0x0002
    T32_MEMORY_ACCESS_X86_LP                 = 0x0003
    T32_MEMORY_ACCESS_X86_IO                 = 0x0004
    T32_MEMORY_ACCESS_X86_MSR                = 0x0005
    T32_MEMORY_ACCESS_XTENSA_DAP             = T32_MEMORY_ACCESS_ARM_DAP
    T32_MEMORY_ACCESS_XTENSA_SPR             = 0x0002
    T32_MEMORY_ACCESS_MMUBYPASS              = 0x8000
    T32_MEMORY_ATTR_WIDTHMASK                = 0x000f
    T32_MEMORY_ATTR_DUALPORT                 = 0x0400
    T32_MEMORY_ATTR_NOINCREMENT              = 0x4000
    
    T32_MAX_EVENTS                           = 4
    T32_E_BREAK                              = 0x00
    T32_E_EDIT                               = 0x01
    T32_E_BREAKPOINTCONFIG                   = 0x02
    T32_E_ONEVENT                            = 0x03
    
    T32_API_RECEIVE                          = 0x01
    T32_API_SYNCREQUEST                      = 0x02
    T32_API_NOTIFICATION                     = 0x06
    T32_API_SYNCACKN                         = 0x12
    T32_API_SYNCBACK                         = 0x22
    
    #/* Flags, which can be used with T32_WriteBreakpoint() / T32_ReadBreakpoint */
    T32_BPCONFIG_PROGRAM                     = 0x001 #/* program breakpoint / execution breakpoint */
    T32_BPCONFIG_SPOT                        = 0x004 #/* spot breakpoint */
    T32_BPCONFIG_READ                        = 0x008 #/* read access breakpoint  */
    T32_BPCONFIG_WRITE                       = 0x010 #/* write access breakpoint */
    T32_BPCONFIG_READWRITE                   = 0x018 #/* read/write access breakpoint */
    T32_BPCONFIG_DELETE                      = 0x100 #/* delete breakpoint */
    T32_BPCONFIG_ALPHA                       = 0x020 #/* Alpha  breakpoint or marker */
    T32_BPCONFIG_BETA                        = 0x040 #/* Beta   breakpoint or marker */
    T32_BPCONFIG_CHARLIE                     = 0x080 #/* Charly breakpoint or marker */
    T32_BPACCESS_DELTA                       = 0x10
    T32_BPACCESS_ECHO                        = 0x20
    T32_BPACCESS_E                           = 0x40
    T32_BPACCESS_ONCHIP                      = 0x80

    T32_PRINTCODE_ASCII                      = 0x41
    T32_PRINTCODE_ASCIIP                     = 0x42
    T32_PRINTCODE_ASCIIE                     = 0x43
    T32_PRINTCODE_CSV                        = 0x44
    T32_PRINTCODE_XML                        = 0x45
    
    class T32_Breakpoint(Structure):
        _fields_ =[('address', c_uint32),
                   ('enabled', c_uint8),
                   ('type', c_uint32),
                   ('auxtype', c_uint32)
                   ];

    #T32EXTERN int  T32_Go(void);
    #T32EXTERN int  T32_Break(void);
    #T32EXTERN int  T32_Step(void);
    #T32EXTERN int  T32_StepMode(int Mode);
    #T32EXTERN int  T32_ResetCPU(void);
    #T32EXTERN int  T32_SetMode(int Mode);
    #T32EXTERN int  T32_GetCpuInfo(char **pCPUString, uint16_t *pFPUType, uint16_t *pEndianess, uint16_t *pReserved);
    #T32EXTERN int  T32_GetState(int *pSystemState);
    #T32EXTERN int  T32_ReadMemory     (uint32_t Address, int Access, uint8_t *pBuffer, int Size);
    #T32EXTERN int  T32_WriteMemory    (uint32_t Address, int Access, const uint8_t *pBuffer, int Size);
    #T32EXTERN int  T32_WriteMemoryPipe(uint32_t Address, int Access, const uint8_t *pBuffer, int Size);
    #T32EXTERN int  T32_ReadMemoryEx   (uint32_t Address, int Segment, int Access, int Attribute, uint8_t *pBuffer, int Size);                 /*undocumented*/
    #T32EXTERN int  T32_WriteMemoryEx  (uint32_t Address, int Segment, int Access, int Attribute, uint8_t *pBuffer, int Size);                 /*undocumented*/
    #T32EXTERN int  T32_SetMemoryAccessClass(const char* Access);
    #T32EXTERN int  T32_GetRam(uint32_t *pStartAddress, uint32_t *pEndAddress, uint16_t *pAccess);
    #T32EXTERN int  T32_GetSource(uint32_t Address, char *SourceFile, uint32_t *pSourceLine);
    #T32EXTERN int  T32_GetSelectedSource(          char *SourceFile, uint32_t *pSourceLine);
    #T32EXTERN int  T32_GetSymbol(const char *SymbolName, uint32_t *pAddress, uint32_t *pSize, uint32_t *pAccess);
    #T32EXTERN int  T32_GetSymbolFromAddress (char* SymbolName, uint32_t Address, int StringLength);
    #T32EXTERN int  T32_ReadVariableString(const char *VariableName, char *StringFromNumeric, int StringLength);
    #T32EXTERN int  T32_ReadVariableValue (const char *VariableName, uint32_t *pValueLower32Bit, uint32_t *pValueUpper32Bit);
    #T32EXTERN int  T32_WriteVariableValue (const char *VariableName, uint32_t ValueLower32Bit, uint32_t ValueUpper32Bit);
    #T32EXTERN int  T32_GetWindowContent(const char *command, char * buffer, uint32_t requested, uint32_t offset, uint32_t print_code);
    #T32EXTERN int  T32_ReadRegisterByName (const char *RegisterName, uint32_t *pValueLower32Bit, uint32_t *pValueUpper32Bit);
    #T32EXTERN int  T32_WriteRegisterByName(const char *RegisterName, uint32_t ValueLower32Bit, uint32_t ValueUpper32Bit);
    #T32EXTERN int  T32_ReadPP(uint32_t *pProgramCounter);
    #T32EXTERN int  T32_ReadRegister (uint32_t MaskLower32Bit, uint32_t MaskUpper32Bit, uint32_t *pBuffer);
    #T32EXTERN int  T32_WriteRegister(uint32_t MaskLower32Bit, uint32_t MaskUpper32Bit, uint32_t *pBuffer);
    #T32EXTERN int  T32_ReadBreakpoint (uint32_t Address, int Access, uint16_t *pBPConfiguration, int Size);
    #T32EXTERN int  T32_WriteBreakpoint(uint32_t Address, int Access, int        BPConfiguration, int Size);
    #T32EXTERN int  T32_GetBreakpointList(int *pNumberFetched, T32_Breakpoint *pBPSettings, int FetchLimit);
    #T32EXTERN int  T32_GetTraceState(int TraceType, int *pTraceState, int32_t *pTraceTotalRecords, int32_t *pCurrentRecordMin, int32_t *pCurrentRecordMax);
    #T32EXTERN int  T32_ReadTrace    (int TraceType, int32_t StartRecord, int NumberOfRecords, uint32_t Mask, uint8_t *pBuffer);
    #T32EXTERN int  T32_GetLastErrorMessage(char *ErrorMessage, uint32_t* pLastError, uint32_t* pInternal);
    ## ifdef ENABLE_NOTIFICATION
    #typedef void (*T32_NotificationCallback_t)();
    #T32EXTERN int T32_NotifyStateEnable(int EventNumber, T32_NotificationCallback_t pFunction);
    #T32EXTERN int T32_NotifyEventEnable(const char* event, T32_NotificationCallback_t pFunction);
    #T32EXTERN int T32_CheckStateNotify(unsigned ParameterOfCallbackFunction);
    ## endif
    #/*** DEPRECATED ***/
    #T32EXTERN int T32_AnaStatusGet(uint8_t * state, int32_t * size, int32_t * min, int32_t * max);
    #T32EXTERN int T32_AnaRecordGet(int32_t record, uint8_t * buffer, int len);
    #/*** DEPRECATED end ***/
    #
    #
    #/***********************************/
    #/*  Object oriented API functions  */
    #/***********************************/
    #
    #/*** Obj Interface naming convention
    #<objtype>:                  Buffer, Address, Register, Memory, Symbol
    #Object types:               T32_<objtype>Obj
    #Object handle types:        T32_<objtype>Handle
    #Allocating objects:         T32_Request<objtype>Obj
    #//                          T32_Request<objtype>Obj<initial>
    #Reallocating objects:       T32_Resize<objtype>Obj
    #Freeing objects:            T32_Release<objtype>Obj
    #//                          T32_ReleaseAllObjects
    #Getting object attributes:  T32_Get<objtype>Obj<attribute>
    #Setting object attributes:  T32_Set<objtype>Obj<attribute>
    #Copying existing object:    T32_Copy<objtype>Obj
    #Copying from/into objects:  T32_Copy<what>From/To<objtype>Obj
    #Reading from target:        T32_Read<objtype>Obj
    #Reading by signifier:       T32_Read<objtype>ObjBy<signifier>
    #Writing to target:          T32_Write<objtype>Obj
    #Getting info from TRACE32:  T32_Query<objtype>Obj
    #Sending info to TRACE32:    T32_Send<objtype>Obj
    #***/

        
    class T32_Object(Structure):
        pass

    T32_Object._fields_ =[('next', POINTER(T32_Object))
                   ];


    #T32EXTERN int T32_ReleaseAllObjects (void);

    #/** Buffer Object **/
    class T32_BufferObj(Structure):
        pass
    
    T32_BufferObj._fields_ =[('next', POINTER(T32_Object)),
                   ('used', c_uint32),
                   ('storage', POINTER(c_uint8)),
                   ('bufsize', c_uint32)
                   ];
    
    #/* Buffer handle */
    #T32_BufferHandle is POINTER(T32_BufferObj)

    #/* request buffer object */
    #T32EXTERN int T32_RequestBufferObj (T32_BufferHandle *pHandle, const int initial_size);
    #T32EXTERN int T32_ReleaseBufferObj (T32_BufferHandle *pHandle);
    #T32EXTERN int T32_ResizeBufferObj  (T32_BufferHandle handle, const int size);
    #
    #/* buffer access functions */
    #T32EXTERN int T32_CopyDataFromBufferObj (uint8_t *localbuffer, int lbsize, T32_BufferHandle handle);
    #T32EXTERN int T32_CopyDataToBufferObj   (T32_BufferHandle handle, int size, const uint8_t *localbuffer);
    #T32EXTERN int T32_GetBufferObjStoragePointer (uint8_t** ppointer, T32_BufferHandle handle);
    #
    #/** Address Object **/

    #/* enumeration for all address types */
    #typedef enum {
    T32_ADDRTYPE_NONE       = 0
    T32_ADDRTYPE_COMMON     = 1
    T32_ADDRTYPE_A32        = 2
    T32_ADDRTYPE_A64        = 3
    T32_ADDRTYPE_MAX        = 4
    #} T32_AddressObjType; //c_uint
    
    #/* memory access attributes */
    T32ADDROBJATTR_EACCESS  = 0x1
    T32ADDROBJATTR_VERIFY   = 0x2
    
    #/* enumeration for MAU sizes (minumum addressable unit) */
    #typedef enum {
    T32_SIZEOFMAU_NOTSET    = 0
    T32_SIZEOFMAU_TARGET    = 1
    T32_SIZEOFMAU_8BIT      = 8
    T32_SIZEOFMAU_12BIT     = 12
    T32_SIZEOFMAU_16BIT     = 16
    T32_SIZEOFMAU_24BIT     = 24
    T32_SIZEOFMAU_32BIT     = 32
    T32_SIZEOFMAU_64BIT     = 64
    T32_SIZEOFMAU_128BIT    = 128
    T32_SIZEOFMAU_256BIT    = 256
    #} T32_SizeOfMauType; //c_uint

    #/* common address elements */
    class T32_AddressObj_Common(Structure):
        pass
    
    T32_AddressObj_Common._fields_ =[('next', POINTER(T32_Object)),
                   ('type', c_uint32), #T32_AddressObjType
                   ('access', (c_char * 16)),
                   ('width', c_uint16),
                   ('core', c_uint16),
                   ('spaceid', c_uint32),
                   ('attr', c_uint32),
                   ('sizeofmau', c_uint32), #T32_SizeOfMauType
                   ('targetsizeofmau', c_uint32) #T32_SizeOfMauType
                   ];

    #/* address type: 32bit address */
    class T32_AddressObj_32bit(Structure):
        pass
    
    T32_AddressObj_32bit._fields_ =[('common', T32_AddressObj_Common),
                   ('address', c_uint32)
                   ];

    #/* address type: 64bit address */
    class T32_AddressObj_64bit(Structure):
        pass
    
    T32_AddressObj_64bit._fields_ =[('common', T32_AddressObj_Common),
                   ('address', c_uint64)
                   ];

    #/* address handle for all address types */
    class T32_AddressObj(Union):
        pass
        
    T32_AddressObj._fields_ =[('common', T32_AddressObj_Common),
                   ('a32', T32_AddressObj_32bit),
                   ('a64', T32_AddressObj_64bit)
                   ];
    
    #/* Address handle */
    #T32_AddressHandle is POINTER(T32_AddressObj)

    #/* request address object */
    #T32EXTERN int T32_RequestAddressObj     (T32_AddressHandle *pHandle);
    #T32EXTERN int T32_RequestAddressObjA32  (T32_AddressHandle *pHandle, const uint32_t address);
    #T32EXTERN int T32_RequestAddressObjA64  (T32_AddressHandle *pHandle, const uint64_t address);
    #T32EXTERN int T32_ReleaseAddressObj     (T32_AddressHandle *pHandle);
    #T32EXTERN int T32_CopyAddressObj        (T32_AddressHandle *pToHandle, T32_AddressHandle fromHandle);
    #
    #T32EXTERN int T32_SetAddressObjAddr32       (T32_AddressHandle handle, uint32_t address);
    #T32EXTERN int T32_GetAddressObjAddr32       (T32_AddressHandle handle, uint32_t *pAddress);
    #T32EXTERN int T32_SetAddressObjAddr64       (T32_AddressHandle handle, uint64_t address);
    #T32EXTERN int T32_GetAddressObjAddr64       (T32_AddressHandle handle, uint64_t *pAddress);
    #T32EXTERN int T32_SetAddressObjAccessString (T32_AddressHandle handle, const char *accessString);
    #T32EXTERN int T32_GetAddressObjAccessString (T32_AddressHandle handle, char* accessString, uint8_t maxlen);
    #
    #T32EXTERN int T32_SetAddressObjWidth            (T32_AddressHandle handle, uint16_t width);
    #T32EXTERN int T32_SetAddressObjCore             (T32_AddressHandle handle, uint16_t core);
    #T32EXTERN int T32_SetAddressObjSpaceId          (T32_AddressHandle handle, uint32_t spaceid);
    #T32EXTERN int T32_SetAddressObjAttr             (T32_AddressHandle handle, uint32_t attributes);
    #T32EXTERN int T32_SetAddressObjSizeOfMau        (T32_AddressHandle handle, T32_SizeOfMauType sizeofmau);
    #T32EXTERN int T32_GetAddressObjSizeOfMau        (T32_AddressHandle handle, T32_SizeOfMauType* pSizeOfMau);
    #T32EXTERN int T32_GetAddressObjTargetSizeOfMau  (T32_AddressHandle handle, T32_SizeOfMauType* pTargetSizeOfMau);
    
    T32_MMUTRANSLATION_TO_PHYSICAL  = 0x1
    T32_MMUTRANSLATION_TO_LOGICAL   = 0x2
    T32_MMUTRANSLATION_TO_LINEAR    = 0x3

    #T32EXTERN int T32_QueryAddressObjMmuTranslation (T32_AddressHandle handle, uint16_t translation);
    #T32EXTERN int T32_QueryAddressObjTargetSizeOfMau(T32_AddressHandle handle);

    #/* enumeration for all register types */
    #typedef enum {
    #// don't reorder this list - it's used on T32 side, too!
    T32_REGTYPE_NONE        = 0
    T32_REGTYPE_COMMON      = 1     #// common register elements
    T32_REGTYPE_R32         = 2     #// 32bit register
    T32_REGTYPE_R64         = 3     #// 64bit register
    T32_REGTYPE_R128        = 4     #// 128bit register
    T32_REGTYPE_R256        = 5     #// 256bit register
    T32_REGTYPE_R512        = 6     #// 512bit register
    #// add new register types here
    T32_REGTYPE_MAX         = 7
    #} T32_RegisterObjType;

    #/* common register elements */
    T32_MAX_REGNAME     = 15
    T32_INVALID_REGID   = (c_uint32(-1))
    class T32_RegisterObj_Common(Structure):
        pass
    
    T32_RegisterObj_Common._fields_ =[('next', POINTER(T32_Object)),
                   ('type', c_uint32), #T32_AddressObjType
                   ('id', c_uint32),
                   ('name', (c_char * (T32_MAX_REGNAME + 1))),
                   ('core', c_uint16)
                   ];

    #/* register type: 32bit register */
    class T32_RegisterObj_32bit(Structure):
        pass
    
    T32_RegisterObj_32bit._fields_ =[('common', T32_RegisterObj_Common),
                   ('value', c_uint32)
                   ];

    #/* register type: 64bit register */
    class T32_RegisterObj_64bit(Structure):
        pass
        
    T32_RegisterObj_64bit._fields_ =[('common', T32_RegisterObj_Common),
                   ('value', c_uint64)
                   ];

    #/* register type: 128bit register */
    class T32_RegisterObj_128bit(Structure):
        pass
    
    T32_RegisterObj_128bit._fields_ =[('common', T32_RegisterObj_Common),
                   ('value', (c_uint32 * 2))
                   ];

    #/* register type: 256bit register */
    class T32_RegisterObj_256bit(Structure):
        pass
        
    T32_RegisterObj_256bit._fields_ =[('common', T32_RegisterObj_Common),
                   ('value', (c_uint32 * 4))
                   ];

    #/* register type: 512bit register */
    class T32_RegisterObj_512bit(Structure):
        pass
    
    T32_RegisterObj_512bit._fields_ =[('common', T32_RegisterObj_Common),
                   ('value', (c_uint32 * 8))
                   ];

    #/* register handle for all register types */
    class T32_RegisterObj(Union):
        pass
    
    T32_RegisterObj._fields_ =[('common', T32_RegisterObj_Common),
                   ('r32', T32_RegisterObj_32bit),
                   ('r64', T32_RegisterObj_64bit),
                   ('r128', T32_RegisterObj_128bit),
                   ('r256', T32_RegisterObj_256bit),
                   ('r512', T32_RegisterObj_512bit)
                   ];
    
    #/* Register handle */
    #T32_RegisterHandle is  POINTER(T32_RegisterObj)

    #/* request register object */
    #T32EXTERN int T32_RequestRegisterObj        (T32_RegisterHandle *pHandle, const T32_RegisterObjType regType);
    #T32EXTERN int T32_RequestRegisterObjR32     (T32_RegisterHandle *pHandle);
    #T32EXTERN int T32_RequestRegisterObjR64     (T32_RegisterHandle *pHandle);
    #T32EXTERN int T32_RequestRegisterObjR128    (T32_RegisterHandle *pHandle);
    #T32EXTERN int T32_RequestRegisterObjR256    (T32_RegisterHandle *pHandle);
    #T32EXTERN int T32_RequestRegisterObjR512    (T32_RegisterHandle *pHandle);
    #T32EXTERN int T32_RequestRegisterObjR32Name (T32_RegisterHandle *pHandle, const char* regName);
    #T32EXTERN int T32_RequestRegisterObjR64Name (T32_RegisterHandle *pHandle, const char* regName);
    #T32EXTERN int T32_RequestRegisterObjR128Name(T32_RegisterHandle *pHandle, const char* regName);
    #T32EXTERN int T32_RequestRegisterObjR256Name(T32_RegisterHandle *pHandle, const char* regName);
    #T32EXTERN int T32_RequestRegisterObjR512Name(T32_RegisterHandle *pHandle, const char* regName);
    #T32EXTERN int T32_ReleaseRegisterObj        (T32_RegisterHandle *pHandle);
    #
    #T32EXTERN int T32_SetRegisterObjName        (T32_RegisterHandle handle, const char* regName);
    #T32EXTERN int T32_GetRegisterObjName        (T32_RegisterHandle handle, char* regName, uint8_t maxlen);
    #T32EXTERN int T32_SetRegisterObjId          (T32_RegisterHandle handle, uint32_t regId);
    #T32EXTERN int T32_GetRegisterObjId          (T32_RegisterHandle handle, uint32_t *pRegId);
    #
    #T32EXTERN int T32_SetRegisterObjValue32     (T32_RegisterHandle handle, uint32_t value);
    #T32EXTERN int T32_GetRegisterObjValue32     (T32_RegisterHandle handle, uint32_t *pValue);
    #T32EXTERN int T32_SetRegisterObjValue64     (T32_RegisterHandle handle, uint64_t value);
    #T32EXTERN int T32_GetRegisterObjValue64     (T32_RegisterHandle handle, uint64_t *pValue);
    #T32EXTERN int T32_SetRegisterObjValueArray  (T32_RegisterHandle handle, uint8_t *pArray, uint8_t maxlen);
    #T32EXTERN int T32_GetRegisterObjValueArray  (T32_RegisterHandle handle, uint8_t *pArray, uint8_t maxlen);
    #
    #T32EXTERN int T32_SetRegisterObjCore      (T32_RegisterHandle handle, uint16_t core);


    #/** RegisterSet Object **/

    T32_MAX_REGISTERS = 200
    class T32_RegisterSetObj(Structure):
        pass
        
    T32_RegisterSetObj._fields_ =[('next', POINTER(T32_Object)),
                   ('nregs', c_uint),
                   ('regs', (POINTER(T32_RegisterObj) * 1))
                   ];

    #/* RegisterSet handle */
    #T32_RegisterSetHandle is POINTER(T32_RegisterSetObj)


    #/* request and release register set object */
    #int T32_RequestRegisterSetObj       (T32_RegisterSetHandle *pHandle, int numRegisters, T32_RegisterObjType regType);
    #int T32_RequestRegisterSetObjR32    (T32_RegisterSetHandle *pHandle, int numRegisters);
    #int T32_RequestRegisterSetObjR64    (T32_RegisterSetHandle *pHandle, int numRegisters);
    #int T32_ReleaseRegisterSetObj       (T32_RegisterSetHandle *pHandle);
    #
    #/* access register set properties */
    #int T32_SetRegisterSetObjNames      (T32_RegisterSetHandle handle, const char **names, int numNames);
    #int T32_SetRegisterSetObjValues32   (T32_RegisterSetHandle handle, const uint32_t *values, int numValues);
    #int T32_GetRegisterSetObjValues32   (T32_RegisterSetHandle handle, uint32_t *values, int numValues);
    #
    #int T32_ReadRegisterSetObj  (T32_RegisterSetHandle handle);
    #int T32_WriteRegisterSetObj (T32_RegisterSetHandle handle);
    #
    #
    #/** Symbol Object **/


    T32_MAX_SYMNAME = 64
    T32_MAX_SYMPATH = 256
    class T32_SymbolObj(Structure):
        pass
    
    T32_SymbolObj._fields_ =[('next', POINTER(T32_Object)),
                   ('name', (POINTER(c_char) * (T32_MAX_SYMNAME + 1))),
                   ('path', (POINTER(c_char) * (T32_MAX_SYMPATH + 1))),
                   ('address', POINTER(T32_AddressObj)),
                   ('size', c_int64)
                   ];
    #/* Symbol handle */
    #T32_SymbolHandle is POINTER(T32_SymbolObj)


    #/* request symbol object */
    #T32EXTERN int T32_RequestSymbolObj        (T32_SymbolHandle *pHandle);
    #T32EXTERN int T32_RequestSymbolObjName    (T32_SymbolHandle *pHandle, const char* symName);
    #T32EXTERN int T32_RequestSymbolObjAddr    (T32_SymbolHandle *pSymHandle, const T32_AddressHandle addrHandle);
    #T32EXTERN int T32_ReleaseSymbolObj        (T32_SymbolHandle *pHandle);
    #
    #/* access object attributes */
    #T32EXTERN int T32_SetSymbolObjName        (T32_SymbolHandle handle, const char* symName);
    #T32EXTERN int T32_GetSymbolObjName        (T32_SymbolHandle handle, char* symName, uint8_t maxlen);
    #T32EXTERN int T32_SetSymbolObjAddress     (T32_SymbolHandle symHandle, T32_AddressHandle addrHandle);
    #T32EXTERN int T32_GetSymbolObjAddress     (T32_SymbolHandle symHandle, T32_AddressHandle* pAddrHandle);
    #T32EXTERN int T32_GetSymbolObjSize        (T32_SymbolHandle symHandle, uint64_t* pSize);
    #
    #/** Breakpoint Object **/

    class T32_BreakpointObj(Structure):
        pass
    
    T32_BreakpointObj._fields_ =[('next', POINTER(T32_Object)),
                   ('address', POINTER(T32_AddressObj)),
                   ('size', c_uint64),
                   ('types', c_uint32),
                   ('impl', c_uint32),
                   ('disabled', c_uint8)
                   ];


    T32_BP_TYPE_PROGRAM = 0x01    #// EMU_BREAKSOFT_TYPE_P
    T32_BP_TYPE_READ    = 0x02    #// EMU_BREAKSOFT_TYPE_R
    T32_BP_TYPE_WRITE   = 0x04    #// EMU_BREAKSOFT_TYPE_W
    T32_BP_TYPE_RW      = 0x06    #// EMU_BREAKSOFT_TYPE_RW
    
    T32_BP_IMPL_AUTO    = 0x00    #// inactive "AUTO" breakpoint
    T32_BP_IMPL_SOFT    = 0x01    #// EMU_BREAKSOFT_TYPE_SOFT
    T32_BP_IMPL_ONCHIP  = 0x02    #// EMU_BREAKSOFT_TYPE_ONCHIP
    T32_BP_IMPL_HARD    = 0x04    #// EMU_BREAKSOFT_TYPE_HARD
    T32_BP_IMPL_MARK    = 0x08    #// EMU_BREAKSOFT_TYPE_MARK

    #/* Breakpoint handle */
    #T32_BreakpointHandle is POINTER(T32_BreakpointObj)


    #/* request breakpoint object */
    #T32EXTERN int T32_RequestBreakpointObj        (T32_BreakpointHandle *pBpHandle);
    #T32EXTERN int T32_RequestBreakpointObjAddr    (T32_BreakpointHandle *pBpHandle, const T32_AddressHandle addrHandle);
    #T32EXTERN int T32_ReleaseBreakpointObj        (T32_BreakpointHandle *pBpHandle);
    #
    #/* breakpoint object access */
    #T32EXTERN int T32_SetBreakpointObjAddress (T32_BreakpointHandle bpHandle, T32_AddressHandle addrHandle);
    #T32EXTERN int T32_GetBreakpointObjAddress (T32_BreakpointHandle bpHandle, T32_AddressHandle* pAddrHandle);
    #T32EXTERN int T32_SetBreakpointObjType    (T32_BreakpointHandle bpHandle, uint32_t   type);
    #T32EXTERN int T32_GetBreakpointObjType    (T32_BreakpointHandle bpHandle, uint32_t* pType);
    #T32EXTERN int T32_SetBreakpointObjImpl    (T32_BreakpointHandle bpHandle, uint32_t   impl);
    #T32EXTERN int T32_GetBreakpointObjImpl    (T32_BreakpointHandle bpHandle, uint32_t* pImpl);
    #T32EXTERN int T32_SetBreakpointObjEnable  (T32_BreakpointHandle bpHandle, uint8_t   enable);
    #T32EXTERN int T32_GetBreakpointObjEnable  (T32_BreakpointHandle bpHandle, uint8_t* pEnable);
    #
    #/** Memory access API **/
    #
    #/* read/write length */

    #T32_Length is c_uint32

    #T32EXTERN int T32_ReadMemoryObj (T32_BufferHandle bufferHandle,
    #    const T32_AddressHandle addressHandle, const T32_Length length);
    #
    #T32EXTERN int T32_WriteMemoryObj (T32_BufferHandle bufferHandle,
    #    const T32_AddressHandle addressHandle, const T32_Length length);
    #
    #/** Register access API **/
    #
    #T32EXTERN int T32_ReadRegisterObj (
    #    T32_RegisterHandle registerHandle);
    #
    #T32EXTERN int T32_WriteRegisterObj (
    #    T32_RegisterHandle registerHandle);
    #
    #/** Symbol access API **/
    #
    #T32EXTERN int T32_QuerySymbolObj (
    #    T32_SymbolHandle symbolHandle);             // symbol to query information
    #
    #/** Breakpoint access API **/
    #
    #T32EXTERN int T32_WriteBreakpointObj          (T32_BreakpointHandle handle, int set);
    #T32EXTERN int T32_QueryBreakpointObjCount     (uint32_t* pCount);
    #T32EXTERN int T32_ReadBreakpointObj           (T32_BreakpointHandle handle);      // by address
    #T32EXTERN int T32_ReadBreakpointObjByIndex    (T32_BreakpointHandle handle, uint32_t index);
    #
    #/*******************************/
    #/*  FDX related API functions  */
    #/*******************************/
    #
    #T32EXTERN int  T32_Fdx_Resolve    (const char *Name);
    #T32EXTERN int  T32_Fdx_Open       (const char *Name, const char *Mode);
    #T32EXTERN int  T32_Fdx_Close      (int Channel);
    #T32EXTERN int  T32_Fdx_Receive    (int Channel, void *pData, int Width, int MaxSize);
    #T32EXTERN int  T32_Fdx_ReceivePoll(int Channel, void *pData, int Width, int MaxSize);
    #T32EXTERN int  T32_Fdx_Send       (int Channel, void *pData, int Width, int Size);
    #T32EXTERN int  T32_Fdx_SendPoll   (int Channel, void *pData, int Width, int Size);
    #
    #/*********************************************/
    #/*  Direct/TAP Access related API functions  */
    #/*********************************************/


    T32_DIRECTACCESS_RELEASE        = c_void_p(0)
    T32_DIRECTACCESS_HOLD           = c_void_p(1)

    T32_TAPACCESSSEND_HEADERSIZE    = 6
    T32_TAPACCESS_MAXBITS           = ( (0x3c00 - T32_TAPACCESSSEND_HEADERSIZE) * 8 )
    T32_TAPACCESS_RELEASE           = T32_DIRECTACCESS_RELEASE
    T32_TAPACCESS_HOLD              = T32_DIRECTACCESS_HOLD

    T32_DIRECTACCESS_INSTANCETYPE_TAP         = 0
    T32_DIRECTACCESS_INSTANCETYPE_DAP         = 1
    T32_DIRECTACCESS_INSTANCETYPE_AHB         = 2
    T32_DIRECTACCESS_INSTANCETYPE_APB         = 3
    T32_DIRECTACCESS_INSTANCETYPE_AXI         = 4
    T32_DIRECTACCESS_INSTANCETYPE_I2C         = 5    #/* preliminary*/


    T32_DIRECTACCESS_TRISTATE_UINT32                                                    = 0
    T32_DIRECTACCESS_SWD_UNIT32                                                         = 2
    T32_DIRECTACCESS_INSTANCE_EXISTS_UNIT32                                             = 3
    
    T32_DIRECTACCESS_XXX_DAP_INSTANCE_UINT32                                            = 300
    T32_DIRECTACCESS_XXX_DAPACCESSPORT_UINT32                                           = 301
    T32_DIRECTACCESS_XXX_SYSPOWERUPREQ_UINT32                                           = 302
    T32_DIRECTACCESS_XXX_BIGENDIAN_UINT32                                               = 303
    
    T32_DIRECTACCESS_TAP_CURRENTINSTANCE_UINT32                                         = 100
    T32_DIRECTACCESS_TAP_IRPRE_UINT32                                                   = 101
    T32_DIRECTACCESS_TAP_IRPOST_UINT32                                                  = 102
    T32_DIRECTACCESS_TAP_DRPRE_UINT32                                                   = 103
    T32_DIRECTACCESS_TAP_DRPOST_UINT32                                                  = 104
    T32_DIRECTACCESS_TAP_PARKSTATE_UINT32                                               = 105
    T32_DIRECTACCESS_TAP_MCTAPSTATE_UINT32                                              = 106
    T32_DIRECTACCESS_TAP_MCTCKLEVEL_UINT32                                              = 107
    T32_DIRECTACCESS_TAP_DAP_INSTANCE_UINT32                                            = T32_DIRECTACCESS_XXX_DAP_INSTANCE_UINT32
    T32_DIRECTACCESS_TAP_DAP_ACCESSPORT_UINT32                                          = T32_DIRECTACCESS_XXX_DAPACCESSPORT_UINT32
    T32_DIRECTACCESS_TAP_DAP_JTAGACCESSPORTINDEX_UINT32                                 = 122
    T32_DIRECTACCESS_TAP_AUTO_MULTICORETAPSTATE_UINT32                                  = 123
    T32_DIRECTACCESS_TAP_SELECT_SHIFT_PATTERN_UINT32                                    = 124
    
    T32_DIRECTACCESS_DAP_TAP_INSTANCE_UINT32                                            = 200
    T32_DIRECTACCESS_DAP_SWDP_TARGETSEL_UINT32                                          = 205
    T32_DIRECTACCESS_DAP_TIMEOUT_UINT32                                                 = 206
    T32_DIRECTACCESS_DAP_SCAN_DAP_OPTION_UINT32                                         = 208
    
    T32_DIRECTACCESS_AHB_DAP_INSTANCE_UINT32                                            = T32_DIRECTACCESS_XXX_DAP_INSTANCE_UINT32
    T32_DIRECTACCESS_AHB_DAPACCESSPORT_UINT32                                           = T32_DIRECTACCESS_XXX_DAPACCESSPORT_UINT32
    T32_DIRECTACCESS_AHB_SYSPOWERUPREQ_UINT32                                           = T32_DIRECTACCESS_XXX_SYSPOWERUPREQ_UINT32
    T32_DIRECTACCESS_AHB_BIGENDIAN_UINT32                                               = T32_DIRECTACCESS_XXX_BIGENDIAN_UINT32
    T32_DIRECTACCESS_AHB_CORTEXM_UINT32                                                 = 310
    
    T32_DIRECTACCESS_APB_DAP_INSTANCE_UINT32                                            = T32_DIRECTACCESS_XXX_DAP_INSTANCE_UINT32
    T32_DIRECTACCESS_APB_DAPACCESSPORT_UINT32                                           = T32_DIRECTACCESS_XXX_DAPACCESSPORT_UINT32
    T32_DIRECTACCESS_APB_SYSPOWERUPREQ_UINT32                                           = T32_DIRECTACCESS_XXX_SYSPOWERUPREQ_UINT32
    T32_DIRECTACCESS_APB_BIGENDIAN_UINT32                                               = T32_DIRECTACCESS_XXX_BIGENDIAN_UINT32
    
    T32_DIRECTACCESS_AXI_DAP_INSTANCE_UINT32                                            = T32_DIRECTACCESS_XXX_DAP_INSTANCE_UINT32
    T32_DIRECTACCESS_AXI_DAPACCESSPORT_UINT32                                           = T32_DIRECTACCESS_XXX_DAPACCESSPORT_UINT32
    T32_DIRECTACCESS_AXI_SYSPOWERUPREQ_UINT32                                           = T32_DIRECTACCESS_XXX_SYSPOWERUPREQ_UINT32
    T32_DIRECTACCESS_AXI_BIGENDIAN_UINT32                                               = T32_DIRECTACCESS_XXX_BIGENDIAN_UINT32
    
    T32_SCAN_DAP_OPTION_OUTBUFFER_IMMEDIATELY                                           = 0x0
    T32_SCAN_DAP_OPTION_OUTBUFFER_DELAYED                                               = 0x1
    T32_SCAN_DAP_OPTION_OUTBUFFER_DEPEND_TO_CONFIG                                      = 0x2
    
    T32_DIRECTACCESS_TIMESTAMPFORMAT_T32                                                = 0x0 #/*preliminary*/
    T32_DIRECTACCESS_TIMESTAMPFORMAT_NS                                                 = 0x1 #/*preliminary*/
    T32_DIRECTACCESS_TIMESTAMPFORMAT_US                                                 = 0x2 #/*preliminary*/
    T32_DIRECTACCESS_TIMESTAMPFORMAT_PS                                                 = 0x3 #/*preliminary*/
    T32_DIRECTACCESS_TIMESTAMPFORMAT_OPT_RAW                                     = 0x80000000 #/*preliminary*/
    
    T32_DAPACCESS_REGISTERSET_DP     = 0
    T32_DAPACCESS_REGISTERSET_AP     = 1
    T32_DAPACCESS_REGISTERSET_IDCODE = 2
    T32_DAPACCESS_REGISTERSET_ABORT  = 3

    T32_DAPACCESS_RW_READ       = 0
    T32_DAPACCESS_RW_READWRITE  = 1
    T32_DAPACCESS_RW_WRITE      = 2
    
    T32_DAPAPACCESS_RW_READ  = 0
    T32_DAPAPACCESS_RW_WRITE = 1
    
    T32_TAPSTATE_RUN_TEST_IDLE   = 12
    T32_TAPSTATE_SELECT_DR_SCAN  = 7
    
    def T32_TAPACCESS_SET(self,x):
        return (2|((x)&1))

    T32_TAPACCESS_SET_LOW            = 2
    T32_TAPACCESS_SET_HIGH           = 3
    T32_TAPACCESS_SET_0              = T32_TAPACCESS_SET_LOW
    T32_TAPACCESS_SET_1              = T32_TAPACCESS_SET_HIGH
    T32_TAPACCESS_TDO                = 0x00
    T32_TAPACCESS_TDI                = 0x04
    T32_TAPACCESS_TMS                = 0x08
    T32_TAPACCESS_TCK                = 0x0c
    T32_TAPACCESS_nTRST              = 0x10
    T32_TAPACCESS_nRESET             = 0x14
    T32_TAPACCESS_nRESET_LATCH       = 0x18
    T32_TAPACCESS_VTREF              = 0x1c
    T32_TAPACCESS_VTREF_LATCH        = 0x20
    T32_TAPACCESS_nENOUT             = 0x24
    T32_TAPACCESS_SHIFT              = 0x30
    T32_TAPACCESS_SHIFTTMS           = 0x40
    T32_TAPACCESS_SHIFTIR            = 0x50
    T32_TAPACCESS_SHIFTDR            = 0x60
    T32_TAPACCESS_SLEEP_MS           = 0x7c
    T32_TAPACCESS_SLEEP              = T32_TAPACCESS_SLEEP_MS
    T32_TAPACCESS_SLEEP_US           = 0x7d
    T32_TAPACCESS_SLEEP_HALF_CLOCK   = 0x7e
    T32_TAPACCESS_SPECIAL            = 0x80

    T32_USERSIGNALEVENT = 67

    T32_DIRECTACCESS_USERSIGNAL_SET_ON                       = c_uint32(0x10000000)
    T32_DIRECTACCESS_USERSIGNAL_SET_OFF                      = c_uint32(0x20000000)
    T32_DIRECTACCESS_USERSIGNAL_GET                          = c_uint32(0x30000000)
    T32_DIRECTACCESS_USERSIGNAL_WAS_TRIGGER                  = c_uint32(0x40000000)
    T32_DIRECTACCESS_USERSIGNAL_ENABLE_EVENT_RISING          = c_uint32(0x50000000)
    T32_DIRECTACCESS_USERSIGNAL_ENABLE_EVENT_FALLING         = c_uint32(0x60000000)
    T32_DIRECTACCESS_USERSIGNAL_DISABLE_EVENT_RISING         = c_uint32(0x80000000)
    T32_DIRECTACCESS_USERSIGNAL_DISABLE_EVENT_FALLING        = c_uint32(0x90000000)
    T32_DIRECTACCESS_USERSIGNAL_GET_NEXT_EVENT               = c_uint32(0xB0000000)
    T32_DIRECTACCESS_USERSIGNAL_GET_EVENT_COUNT              = c_uint32(0xC0000000)
    T32_DIRECTACCESS_USERSIGNAL_CLEAR_EVENT                  = c_uint32(0xD0000000)
    T32_DIRECTACCESS_USERSIGNAL_CLEAR_ALL_EVENTS             = c_uint32(0xE0000000)
    T32_DIRECTACCESS_USERSIGNAL_GET_LAST_ERROR               = c_uint32(0xF0000000)
    T32_DIRECTACCESS_USERSIGNAL_POLL_EVENTS                  = c_uint32(0x11000000)
    T32_DIRECTACCESS_USERSIGNAL_SET_DIRECTION_FROM_TARGET    = c_uint32(0x21000000)
    T32_DIRECTACCESS_USERSIGNAL_SET_DIRECTION_TO_TARGET      = c_uint32(0x31000000)
    T32_DIRECTACCESS_USERSIGNAL_SET_TRIGGER_POLARITY_LOW     = c_uint32(0x41000000)
    T32_DIRECTACCESS_USERSIGNAL_SET_TRIGGER_POLARITY_HIGH    = c_uint32(0x51000000)
    T32_DIRECTACCESS_USERSIGNAL_DISABLE_AND_CLEAR_ALL_EVENTS = c_uint32(0x61000000)
    T32_DIRECTACCESS_USERSIGNAL_ENABLE_EVENT_CHANGE          = c_uint32(0x71000000)
    T32_DIRECTACCESS_USERSIGNAL_DISABLE_EVENT_CHANGE         = c_uint32(0x81000000)


    T32_DIRECTACCESS_USERSIGNAL_RESULT_NA   = c_uint32(0x0000000A)
    T32_DIRECTACCESS_USERSIGNAL_RESULT_ON   = c_uint32(0x00000001)
    T32_DIRECTACCESS_USERSIGNAL_RESULT_OFF  = c_uint32(0x00000000)
    
    T32_DIRECTACCESS_USERSIGNAL_POWER       = c_uint32(0x00000001)
    T32_DIRECTACCESS_USERSIGNAL_RESET       = c_uint32(0x00000002)
    T32_DIRECTACCESS_USERSIGNAL_ENOUT       = c_uint32(0x00000003)
    T32_DIRECTACCESS_USERSIGNAL_TRIGGER     = c_uint32(0x00000004)
    
    T32_DIRECTACCESS_USERSIGNAL_JTAG_TDI    = c_uint32(0x00000010)
    T32_DIRECTACCESS_USERSIGNAL_JTAG_TMS    = c_uint32(0x00000011)
    T32_DIRECTACCESS_USERSIGNAL_JTAG_TCK    = c_uint32(0x00000012)
    T32_DIRECTACCESS_USERSIGNAL_JTAG_TDO    = c_uint32(0x00000013)
    T32_DIRECTACCESS_USERSIGNAL_JTAG_RTCK   = c_uint32(0x00000014)
    T32_DIRECTACCESS_USERSIGNAL_JTAG_TRST   = c_uint32(0x00000015)

    SHIFTRAW_OPTION_NONE             = 0x0000
    SHIFTRAW_OPTION_LASTTMS_ONE      = 0x0008
    SHIFTRAW_OPTION_TMS_ZERO         = SHIFTRAW_OPTION_NONE
    SHIFTRAW_OPTION_TMS_ONE          = 0x0010
    SHIFTRAW_OPTION_TDI_ZERO         = SHIFTRAW_OPTION_NONE
    SHIFTRAW_OPTION_TDI_LASTTDO      = 0x0020
    SHIFTRAW_OPTION_TDI_ONE          = 0x0040

    T32_I2CACCESS_ACTION_WRITE           = 0  #/* preliminary*/
    T32_I2CACCESS_ACTION_READ            = 1  #/* preliminary*/
    T32_I2CACCESS_ACTION_READ_NONAK      = 2  #/* preliminary*/
    
    T32_I2CACCESS_RESULT_OK             = 0  #/* preliminary*/
    T32_I2CACCESS_RESULT_DEVIDNAK       = 2  #/* preliminary*/
    T32_I2CACCESS_RESULT_CMDNAK         = 3  #/* preliminary*/
    T32_I2CACCESS_RESULT_DATANAK        = 4  #/* preliminary*/
    T32_I2CACCESS_RESULT_SDAZERO        = 5  #/* preliminary*/
    T32_I2CACCESS_RESULT_SCLZERO        = 6  #/* preliminary*/
    T32_I2CACCESS_RESULT_NODRIVER       = 7  #/* preliminary*/
    T32_I2CACCESS_RESULT_TIMEOUT        = 8  #/* preliminary*/
    T32_I2CACCESS_RESULT_INVALIDPORT    = 9  #/* preliminary */
    
    T32_I2C_RAWACC_SEND_START      = 0x00000100  #/* preliminary*/
    T32_I2C_RAWACC_SEND_STOP       = 0x00000200  #/* preliminary*/
    T32_I2C_RAWACC_SEND_ACK        = 0x00000400  #/* preliminary*/
    T32_I2C_RAWACC_SEND_IGNNAK     = 0x00000800  #/* preliminary*/
    T32_I2C_RAWACC_RECV_ACK        = 0x00000100  #/* preliminary*/
    T32_I2C_RAWACC_RECV_ERR        = 0x00000200  #/* preliminary*/
    T32_I2C_RAWACC_RECVERR_NOACK   = 0x00010000  #/* preliminary*/
    T32_I2C_RAWACC_RECVERR_ARB     = 0x00020000  #/* preliminary*/
    T32_I2C_RAWACC_RECVERR_TIMEOUT = 0x00030000  #/* preliminary*/

    #define T32_TAPAccessRelease T32_DirectAccessRelease
    #define T32_TAPAccessAlloc T32_BundledAccessAlloc
    #define T32_TAPAccessExecute T32_BundledAccessExecute
    #define T32_TAPAccessFree T32_BundledAccessFree
    #define T32_TAPACCESS_HANDLE T32_BUNDLEDACCESS_HANDLE

    class T32_Param(Union):
        _fields_ =[('uint32', c_uint32),
                   ];
        



    #T32_BUNDLEDACCESS_HANDLE is c_void_p

    #T32EXTERN T32_Param T32_ParamFromUint32(uint32_t value);
    #T32EXTERN T32_BUNDLEDACCESS_HANDLE T32_BundledAccessAlloc(void);
    #T32EXTERN int  T32_BundledAccessExecute(T32_BUNDLEDACCESS_HANDLE Handle, T32_BUNDLEDACCESS_HANDLE SequenceHandle);
    #T32EXTERN int  T32_BundledAccessFree(T32_BUNDLEDACCESS_HANDLE Handle);
    #T32EXTERN int  T32_DirectAccessRelease(void);
    #T32EXTERN int  T32_DirectAccessResetAll(T32_BUNDLEDACCESS_HANDLE Handle);
    #T32EXTERN int  T32_DirectAccessSetInfo(T32_BUNDLEDACCESS_HANDLE Handle, int nInstanceType, unsigned int nInstance, int nInfoID, T32_Param value);
    #T32EXTERN int  T32_DirectAccessGetInfo(T32_BUNDLEDACCESS_HANDLE Handle, int nInstanceType, unsigned int nInstance, int nInfoID, T32_Param *value);
    #T32EXTERN int  T32_DirectAccessGetTimestamp(T32_BUNDLEDACCESS_HANDLE Handle, int Format, uint64_t *result); /* preliminary*/
    #T32EXTERN int  T32_TAPAccessSetInfo(int irpre, int irpost, int drpre, int drpost, int tristate, int tapstate, int tcklevel, int reserved);
    #T32EXTERN int  T32_TAPAccessSetInfo2(T32_BUNDLEDACCESS_HANDLE Handle, int irpre, int irpost, int drpre, int drpost, int tristate, int tapstate, int tcklevel, int reserved);
    #T32EXTERN int  T32_TAPAccessShiftRaw(T32_BUNDLEDACCESS_HANDLE Handle, int NumberOfBits, const uint8_t *pTMSBits,  const uint8_t *pTDIBits, uint8_t *pTDOBits, int Options);
    #T32EXTERN int  T32_TAPAccessShiftIR(T32_BUNDLEDACCESS_HANDLE Handle, int NumberOfBits, const uint8_t *pOutBits,  uint8_t *pInBits);
    #T32EXTERN int  T32_TAPAccessShiftDR(T32_BUNDLEDACCESS_HANDLE Handle, int NumberOfBits, const uint8_t *pOutBits,  uint8_t *pInBits);
    #T32EXTERN int  T32_TAPAccessJTAGResetWithTMS(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nTapInstance);
    #T32EXTERN int  T32_TAPAccessJTAGResetWithTRST(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nTapInstance, int32_t nTRSTAssertTimeUS, int32_t nDelayAfterTRSTReleaseUS);
    #T32EXTERN int  T32_TAPAccessSetShiftPattern(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nTapInstance, uint32_t nReturnIRCount, uint32_t nReturnDRCount, uint32_t nGotoIRCount, uint32_t nGotoDRCount, uint32_t nReturnIR, uint32_t nReturnDR, uint32_t nGotoIR, uint32_t nGotoDR, unsigned int nPattern);
    #T32EXTERN int  T32_TAPAccessDirect(T32_BUNDLEDACCESS_HANDLE Handle, int NumberOfBytes, const uint8_t *pOutBytes, uint8_t *pInBytes);
    #T32EXTERN int  T32_DirectAccessUserSignal(T32_BUNDLEDACCESS_HANDLE Handle, int NumberOfAccesses, const uint32_t *pOutAccesses, uint32_t *pInAccesses);
    #T32EXTERN int  T32_DAPAccessScan(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nDapInstance, int nRegisterSet, int nRW, uint32_t nRegisterAddress, uint32_t nDataIn, uint32_t *pDataOut);
    #T32EXTERN int  T32_DAPAccessInitSWD(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nDapInstance);
    #T32EXTERN int  T32_DAPAPAccessReadWrite(T32_BUNDLEDACCESS_HANDLE Handle, int nAPType, unsigned int nInstance, int nRW, uint64_t nAddress, uint8_t * pData, unsigned int nByteWidth, unsigned int nByteSize, int bNonIncrement, uint32_t nFlags);
    #T32EXTERN int  T32_I2CAccess(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nInstance, uint32_t nAction, uint32_t nDeviceID, const uint8_t* pCommandData, unsigned int nCommandByteLength, uint8_t* pData, unsigned int nDataByteLength); /* preliminary*/
    #T32EXTERN int  T32_I2CRawAccess(T32_BUNDLEDACCESS_HANDLE Handle, unsigned int nInstance, const uint32_t *send, uint32_t *recv, int len);
    #T32EXTERN int  T32_DirectAccessExecuteLua(T32_BUNDLEDACCESS_HANDLE Handle, const char* filename, int mode, const uint8_t* inputBuf, int inputBuflen, uint8_t* outputBuf, int outputBufLen); /* preliminary*/

import platform, os

def t32_load_lib():
    if 0 != t32.api :
        logging.debug("t32 api already loaded!")
        return
    the_path = os.path.split(os.path.realpath(__file__))
    #logging.debug(the_path)
    # auto-detect the correct library
    if (platform.system()=='Windows') or (platform.system()[0:6]=='CYGWIN') :
        if sizeof(c_voidp)==4:
            # WINDOWS 32bit
            t32.api = CDLL(the_path[0] + "\\t32api.dll")
        else:
            # WINDOWS 64bit
            t32.api = CDLL(the_path[0] + "\\t32api64.dll")
    elif platform.system()=='Darwin' :
        # Mac OS X
        t32.api = CDLL(the_path[0] + "/t32api.dylib")
    else :
        if sizeof(c_voidp)==4:
            # Linux 32bit
            t32.api = CDLL(the_path[0] + "/t32api.so")
        else:
            # Linux 64bit
            t32.api = CDLL(the_path[0] + "/t32api64.so")
    return t32.api

import logging
from config.debug import *

def t32_api_test_connect(port="20000", node="localhost", packlen="1024"):
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


if 0 == t32.api :
    #t32.handler = t32.T32_DIRECTACCESS_HOLD
    t32.handler = t32.T32_DIRECTACCESS_RELEASE
    t32_load_lib()

if __name__ == "__main__" :
    t32_api_test_connect("20077")
    t32.api.T32_ParamFromUint32.restype = t32.T32_Param
    TAP_INSTANCE_INDEX = 0
    DAP_INSTANCE_INDEX = 0
    #Setup Debug Port
    if t32.T32_OK != t32.api.T32_Cmd(b"SYStem.JtagClock 1Mhz") :
        logging.error("1")
        raise

    #Reset previous configuration
    if t32.T32_OK != t32.api.T32_DirectAccessResetAll(t32.T32_DIRECTACCESS_HOLD) :
        logging.error("2")
        raise

    #Configure JTAG
    #set park state to Select-DR-Scan
    if (t32.T32_OK != t32.api.T32_DirectAccessSetInfo(t32.T32_DIRECTACCESS_HOLD,
        c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_TAP), c_uint(TAP_INSTANCE_INDEX),
        c_int(t32.T32_DIRECTACCESS_TAP_PARKSTATE_UINT32),
        t32.api.T32_ParamFromUint32(t32.T32_TAPSTATE_SELECT_DR_SCAN))) :
        logging.error("3")
        raise
        
    #Configure DAP
    #set JTAG TAP instance
    if (t32.T32_OK != t32.api.T32_DirectAccessSetInfo(t32.T32_DIRECTACCESS_HOLD,
        c_int(t32.T32_DIRECTACCESS_INSTANCETYPE_DAP), c_uint(DAP_INSTANCE_INDEX),
        c_int(t32.T32_DIRECTACCESS_DAP_TAP_INSTANCE_UINT32),
        t32.api.T32_ParamFromUint32(TAP_INSTANCE_INDEX))) :
        logging.error("4")
        raise
        
    #Enable output of debug port driver
    buffer = c_uint8(t32.T32_TAPACCESS_nENOUT | t32.T32_TAPACCESS_SET_0);
    if (t32.T32_OK != t32.api.T32_TAPAccessDirect(t32.T32_DIRECTACCESS_HOLD, c_int(1), byref(buffer), c_int(0))) :
        logging.error("5")
        raise

    #Reset JTAG
    if (t32.T32_OK != t32.api.T32_TAPAccessJTAGResetWithTMS(t32.T32_DIRECTACCESS_HOLD,
        c_uint(TAP_INSTANCE_INDEX))) :
        logging.error("6")
        raise

    data = c_uint32(0)
    if (t32.T32_OK != t32.api.T32_DAPAccessScan(t32.T32_DIRECTACCESS_HOLD,
        c_uint(0),
        c_int(t32.T32_DAPACCESS_REGISTERSET_DP),
        c_int(t32.T32_DAPACCESS_RW_READ),
        c_uint32(0x1),
        c_uint32(0),
        byref(data))) :
        logging.error("7")
        raise
    
    t32.api.T32_DirectAccessRelease()
    t32.api.T32_Exit()
    print("the CTRLSTAT is 0x%08x" % data.value)
    print("test done")
        
    
    
