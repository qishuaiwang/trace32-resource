
#                TRACE32 Remote API
#      Copyright (c) 1998-2012 Lauterbach GmbH
#                All rights reserved
#
#              Visual Studio Makefile


#
#    Please use Microsoft Visual Studio  nmake
#
#    Select e.g. Start>All Programs>Microsoft Visual Studio 2010>Visual Studio Tools>Visual Studio Command Prompt(2010)
#    in order to open a shell for compiling the 32bit library version (i.e. t32api.dll, t32api.lib, t32api.exp).
#
#    Select e.g. Start>All Programs>Microsoft Visual Studio 2010>Visual Studio Tools>Visual Studio x64 Win64 Command Prompt(2010)
#    in order to open a shell for compiling the 64bit library version (i.e. t32api64.dll, t32api64.lib, t32api64.exp).
#
#
#    Remarks:
#      - recommended libs for 32bit build:
#        ....\Microsoft SDKs\Windows\v7.0A\Lib\User32.Lib
#        ....\Microsoft SDKs\Windows\v7.0A\Lib\WSock32.Lib
#
#      - recommended libs for 64bit build:
#        ....\Microsoft SDKs\Windows\v7.0A\Lib\x64\User32.Lib
#        ....\Microsoft SDKs\Windows\v7.0A\Lib\x64\WSock32.Lib
#


CC = cl /W3 /D_CRT_SECURE_NO_WARNINGS /Gs

!IFDEF DEBUG
OF     = debug
CFLAGS = /Od /Zi /Fd"$(OF)\vc80.pdb" /DDEBUG
LFLAGS = /DEBUG
!ELSE
OF     = release
CFLAGS = /Gd /Ot
LFLAGS =
!ENDIF

!IF "$(T32VC32BUILD)"!=""||"$(T32VC64BUILD)"!=""
# if called by compile.bat or compile64.bat
REMOVERECURSIVELY = RM -rf
!ELSE
REMOVERECURSIVELY = RMDIR /S /Q
!ENDIF

!IF EXIST(release)||EXIST(debug)
!IF EXIST(release)
CLEAN = $(REMOVERECURSIVELY) release
!ENDIF
!IF EXIST(debug)
CLEAN = $(REMOVERECURSIVELY) debug
!ENDIF
!ELSE
CLEAN = @echo nothing to clean
!ENDIF

!IF DEFINED(PLATFORM)
NAME                = t32api64
SUBSYSTEMMINVERSION = 5.02
!ELSE
NAME                = t32api
SUBSYSTEMMINVERSION = 5.00
!ENDIF
SEARCH = {.;..\src}

help:
	@echo.
	@echo. nmake help ... show this help
	@echo.
	@echo. nmake all .... same as "nmake rel"
	@echo.
	@echo. nmake rel .... build t32api/t32api64.dll depending on VS 32bit/64bit shell
	@echo.
	@echo. nmake dbg .... build t32api/t32api64.dll (with debug info)
	@echo.
	@echo. nmake clean .. delete working directories .\release\ and .\debug\
	@echo.
	@echo.

rel: all

dbg:
	nmake DEBUG=1 /NOLOGO all

all: $(OF) $(OF)\$(NAME).dll
	copy $(OF)\$(NAME).dll $(NAME).dll
	copy $(OF)\$(NAME).lib $(NAME).lib
	copy $(OF)\$(NAME).exp $(NAME).exp
	$(REMOVERECURSIVELY) $(OF)

$(OF):
	@if exist release $(REMOVERECURSIVELY) release
	@if exist debug   $(REMOVERECURSIVELY) debug
	MKDIR $@

$(OF)\$(NAME).dll: $(OF)\$(NAME).obj $(OF)\hremote.obj $(OF)\hlinknet.obj
	link  $(LFLAGS) /dll /subsystem:windows,$(SUBSYSTEMMINVERSION) /out:"$@" $** user32.lib wsock32.lib

$(OF)\$(NAME).obj:  $(SEARCH)t32api.c $(SEARCH)t32.h makefile
	$(CC) /c $(CFLAGS) /Fo$@ %s /I..\src

$(OF)\hremote.obj:  $(SEARCH)$$(@B).c $(SEARCH)t32.h makefile
	$(CC) /c $(CFLAGS) /Fo$@ %s /DENABLE_NOTIFICATION /DDLL_BUILD

$(OF)\hlinknet.obj: $(SEARCH)$$(@B).c $(SEARCH)t32.h makefile
	$(CC) /c $(CFLAGS) /Fo$@ %s /DENABLE_NOTIFICATION /DDLL_BUILD

clean: extraclean

extraclean:
	$(CLEAN)


