#!/usr/bin/python
# -*- coding: latin-1 -*- 
'''
@author: ken.kuang
'''

import os
import sys

PROGNAME=os.path.basename(__file__)

import atexit
@atexit.register
def debug_tools_goodbye():
    try:
        asic.dj.destroy()
    except:
        pass

def usage():
    print(
          " Syntax: %s ""\r\n"
          "    -h, --help""\r\n"
          "        show this help information""\r\n"
          "    -p project_name, --porj=project_name""\r\n"
          "        use the project_name's ASIC configuration""\r\n"
          %(PROGNAME)
          )



def init_djtag():
    try :
        asic.djtag_config()
        #asic.djtag_dump()
    except:
        asic.dj.destroy()
    global djd,dje
    #short name for use
    djd=asic.djtag_dump
    dje=asic.dj.execute

if __name__ == "__main__" :
    os.environ.setdefault('PYTHONINSPECT', 'x')
    the_path = os.path.split(os.path.realpath(__file__))
    sys.path.append(the_path[0])
    try :
        import rlcompleter
        import readline
        readline.parse_and_bind('tab: complete')
    except:
        pass

    project_name = "SharkLJ1"
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:",["help","proj="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)
    for opt, arg in opts:
        if opt.lower() in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt.lower() in ("-p","--proj"):
            project_name = arg;

    from config.ASIC import *
    asic = ASICConfig(project_name)
    print(
          "init_djtag() for config djtag.""\r\n"
          "    djd - djtag dump""\r\n"
          "    dje - djtag execute""\r\n"
          ">>>>>>"
          )
