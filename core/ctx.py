if __package__ is None or __package__ == '':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.timer     import *
from core.event     import *
from core.conf      import *
from core.log       import *
from core.condition import *


class Ctx(object):
    def __init__(this):
        this.el = Event.init()
        this.tl = Timer.init()
        this.log = Log.init()

    def __call__(this):
        Event.init(this.el)
        Timer.init(this.tl)
        Log.init(this.log)

Ctx()
