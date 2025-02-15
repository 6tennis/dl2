import __init__
from ability.abilitybase import *
from core.ctx import *
import random

class atk(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            if this.host.condition('hp>70%'):
                this.passive = this.host.Passive('%s_atk'%name, v, 'atk')
        elif c == 'hp100':
            if this.host.condition('fullhp'):
                this.passive = this.host.Passive('%s_atk'%name, v, 'atk')
        elif c == 'hit15':
            if this.host.condition('flurry'):
                this.on = 0
                this.passive = this.host.Passive('%s_atk'%name, 0, 'atk')
                this.host.Listener('hit')(this.l_hit)
        else:
            this.passive = this.host.Passive('%s_atk'%name, v, 'atk')


    def l_hit(this, e):
        if this.on :
            if e.hit < 15 :
                this.on = 0
                this.passive.set(0)
        else:
            if e.hit >= 15 :
                this.on = 1
                this.passive.set(this.v)

    def __call__(this):
        if this.passive:
            this.passive()

class atkspd(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp30':
            if this.host.condition('hp<30%'):
                this.passive = this.host.Passive('%s_atk'%name, v[0], 'atk')
                this.passive2 = this.host.Passive('%s_spd'%name, v[1], 'spd')

    def __call__(this):
        if this.passive:
            this.passive()
            this.passive2()

class fs(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_fs'%name, v, 'fs')


    def __call__(this):
        this.passive()


class sd(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            if this.host.condition('hp>70%'):
                this.passive = this.host.Passive('%s_s'%name, v, 's')
        elif c == 'hp100':
            if this.host.condition('fullhp'):
                this.passive = this.host.Passive('%s_s'%name, v, 's')
        else:
            this.passive = this.host.Passive('%s_s'%name, v, 's')


    def __call__(this):
        if this.passive:
            this.passive()


class cc(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            this.condi = 'hp>70%'
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')
        elif c == 'hp100':
            this.condi = 'hp=100%'
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')
        elif c == 'hit15':
            this.condi = 'hit>=15'
            this.on = 0
            this.passive = this.host.Passive('%s_cc'%name, 0, 'cc')
            this.host.Listener('hit')(this.l_hit)
        else:
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')


    def l_hit(this, e):
        if this.on :
            if e.hit < 15 :
                this.on = 0
                this.passive.set(0)
        else:
            if e.hit >= 15 :
                this.on = 1
                this.passive.set(this.v)


    def __call__(this):
        this.passive()


class cd(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            condi = 'hp>70%'
        elif c == 'hp100':
            condi = 'hp=100%'
        this.passive = this.host.Passive('%s_cd'%name, v, 'cd')


    def __call__(this):
        this.passive()


class sp(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'fs':
            this.passive = this.host.Passive('%s_fsp'%name, v, 'fsp')
        elif c == None:
            this.passive = this.host.Passive('%s_sp'%name, v, 'sp')


    def __call__(this):
        this.passive()


class bt(Ability):
    def __init__(this, name, v):
        this.v = v
        this.passive = this.host.Passive('%s_bt'%name, v, 'buff')


    def __call__(this):
        this.passive()


class bk(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_bk'%name, v, 'killer', 'bk')


    def __call__(this):
        this.passive()


class od(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_od'%name, v, 'killer', 'od')


    def __call__(this):
        this.passive()


class prep(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        Timer(this.charge)(0)

    def charge(this, t):
        this.host.charge_p('%s prep'%(this.name), this.v)

class fc(Ability): # force charge
    def __init__(this, name, v='25%'):
        this.name = name
        this.v = v
        this.stack = 3

    def __call__(this):
        this.host.conf['fs']['on_hit'].append(this.charge)
        Conf(this.host.conf).commit()

    def charge(this, t):
        if this.stack > 0:
            this.host.charge_p('%s prep'%(this.name), this.v)
            this.stack -= 1
            if this.stack <= 0:
                i = this.host.conf['fs']['on_hit'].index(this.charge)
                this.host.conf['fs']['on_hit'].pop(i)
                Conf(this.host.conf).commit()




class k(Ability):
    def __init__(this, name, v, c):
        this.v = v
        this.passive = this.host.Passive('%s_%s_killer'%(name, c),
                                            v, 'killer', c)

    def __call__(this):
        this.passive()
killer = k

class k_burn(Ability):
    def __init__(this, name, v):
        this.v = v
        this.passive = this.host.Passive('%s_burn_killer'%(name),
                                            v, 'killer', 'burn')
    def __call__(this):
        this.passive()


class def_c_atk(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Listener('buff')(this.c_atk)
    
    def c_atk(this, e):
        if e.btype == 'def':
            this.host.Selfbuff('def_chain', this.v)(15)

class def_c_energy(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Listener('def')(c_energy)
    
    def c_energy(this, e):
        this.host.Energy.self(1)

class afflic_c_selfatk(Ability):
    def __init__(this, name, v, atype):
        this.name = name
        this.v = v
        this.atype = atype

    def __call__(this):
        this.host.Listener('afflic')(this.c_atk)
    
    def c_atk(this, e):
        if e.atype != this.atype:
            return
        this.host.Selfbuff('afflic_c_%s'%this.atype, this.v)(15)

class afflic_c_teamatk(Ability):
    def __init__(this, name, v, atype):
        this.name = name
        this.v = v
        this.atype = atype

    def __call__(this):
        this.host.Listener('afflic')(this.c_atk)
    
    def c_atk(this, e):
        if e.atype != this.atype:
            return
        this.host.Teambuff('afflic_c_%s'%this.atype, this.v)(15)

class skill_link(Ability):
    def __init__(this, name, v, btype, duration=10):
        from core import env
        this.dst = env.stage['1p']
        this.btype = btype
        this.v = v
        this.duration = duration
        this.t = 0
        this.cding = 0
        this.t_cd = Timer(this.cd)
        this.logcd = Logger('cd')

    def cd(this, t):
        this.cding = 0

    def __call__(this):
        this.dst.conf['x1']['proc'].append(this.check)
        this.dst.conf['x2']['proc'].append(this.check)
        this.dst.conf['x3']['proc'].append(this.check)
        this.dst.conf['x4']['proc'].append(this.check)
        this.dst.conf['x5']['proc'].append(this.check)
        this.dst.conf['fs']['proc'].append(this.check)

    def check(this):
        if this.cding :
            if this.logcd:
                sp = this.dst.s1.sp
                if sp.cur >= sp.max and this.t==0:
                    this.logcd(this.dst.name, 'skill_link cding')
            return
        sp = this.dst.s1.sp
        if sp.cur >= sp.max and this.t==0:
            this.t = 1
            this.dst.Selfbuff('skill_link_%s'%this.btype, this.v, this.btype)\
                                (this.duration)
            this.cding = 1
            this.t_cd(15)
        elif sp.cur < sp.max :
            this.t = 0


class lo(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        Timer(this.trigger)(3)

    def trigger(this, t):
        this.host.Selfbuff('lastoffense', this.v)(15)


class ro(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v
        this.idx = 0

    def __call__(this):
        this.host.Listener('hp<30')(this.ro_atk)
    
    def ro_atk(this, e):
        if this.idx <= 2:
            this.host.Selfbuff('resilient offense', this.v)(-1)
            this.idx+=1


class sts(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)


class sls(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)

class dc(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v
        this.idx = 0
        if v == 1:
            buff = [0.04,0.10,0.20]
        elif v == 2:
            buff = [0.05,0.13,0.25]
        elif v == 3:
            buff = [0.06,0.15,0.30]

    def __call__(this):
        this.host.Listener('dragon')(this.d_atk)
    
    def d_atk(this, e):
        if this.idx <= 2:
            this.host.Selfbuff('dragon_claw', this.buff[this.idx])(-1)
            this.idx+=1

class extra_energy(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        tmp = this.host.Energy.self
        def energy_chain(count):
            if random.random() < this.v :
                count += 1
            tmp(count)
        this.host.Energy.self = energy_chain
