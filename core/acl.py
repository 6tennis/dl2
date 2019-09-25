#from core.log import *
import __init__
import sys
from core.ctx import *

_g_line = ""

def acl_func_str(acl):
    s = acl_str(acl)
    exec(s,globals())
    return do_action_control_list, s

def acl_func(acl):
    s = acl_str(acl)
    exec(s,globals())
    return do_action_control_list

def acl_str(acl):
    global _g_line
    aif = []
    aif_list = []
    prepare_list = []


    aifline = -1
    prepareline = -1
    curr = 'none'
    for i in acl:
        if i == "`":
            aifline += 1
            aif.append("")
            curr = 'aif'
        elif i == "#":
            prepareline += 1
            prepare_list.append("")
            curr = 'prepare'
        else:
            if curr == 'aif':
                aif[aifline] += i
            elif curr == 'prepare':
                prepare_list[prepareline] += i

    for i in aif:
        aif_list.append( i.split(',', 1))


    line = ""

    line += "def do_action_control_list(this, e):\n"

    for i in prepare_list:
        line += "    %s\n"%(i.rstrip().replace('\n','\n    '))
    line += '#   ----------------------------------\n'

    for i in aif_list:
        if len(i) == 1:
            line += "    if this.%s():\n"%( i[0].strip() )
            line += "        return '%s'\n"%( i[0].strip() )
            #line_list.append("%s()\n"%i[0])
        elif len(i) == 2:
            condi = i[1].strip().replace("=","==")
            condi = condi.replace("====","==")
            condi = condi.replace("!==","!=")
            condi = condi.replace(">==",">=")
            condi = condi.replace("<==","<=")
            #condi = i[1].strip()
            line += "    if %s :\n"%( condi )
            line += "        if this.%s():\n"%( i[0].strip() )
            line += "            return '%s'\n"%( i[0].strip() )
            #line_list.append( "if %s :\n    %s()\n"%(i[1],i[0]) )

    line += '    return 0'
    #_g_line = line
    return line


if __name__ == "__main__":
    a = 1
    b = 0
    this = 0
    e = 0
    epin = 'a'
    def foo():
        print('foo')


    acl = """
        #if a>b :\n    b=3\n
        `s1,a>b and pin!='sp'
        `s2
        `s3
        #s1 = foo
        #s2 = foo
        #s3 = foo
        #pin = epin
        """

    a = acl_str(acl)
    print(a)
    exit()
    acl_func_str(acl)[0](this, e)
    print(_g_line)
    

