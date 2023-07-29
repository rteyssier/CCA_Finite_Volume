import numpy as np

gamma = 1.4

def prim_to_cons(w):
    u = 0.*w
    # density
    u[0] = w[0]
    # momentum
    u[1] = w[0]*w[1]
    # total energy
    u[2] = 0.5*w[0]*w[1]**2 + w[2]/(gamma-1)
    return u

def prim_to_flux(w):
    f = 0.*w
    # mass flux
    f[0] = w[0]*w[1]
    # momentum flux
    f[1] = w[0]*w[1]**2+w[2]
    # total energy flux
    f[2] = (0.5*w[0]*w[1]**2 + gamma*w[2]/(gamma-1))*w[1]
    return f

def cons_to_prim(u):
    w = 0.*u
    # density
    w[0] = u[0]
    # velocity
    w[1] = u[1]/u[0]
    # pressure
    w[2] = (gamma-1)*(u[2]-0.5*w[0]*w[1]**2)
    return w

def vs(pstar,dk,vk,pk,ck):
    
    # sound speed
    ak = 2/(gamma+1)/dk
    bk = (gamma-1)/(gamma+1)*pk
    
    # rarefaction
    vraref = 2/(gamma-1)*ck*((pstar/pk)**((gamma-1)/(2*gamma))-1)
    dvraref = (pstar/pk)**(-(gamma+1)/(2*gamma))/(dk*ck)
    
    # shock
    vshock = (pstar-pk)*np.sqrt(ak/(pstar+bk))
    dvshock = (1-(pstar-pk)/(2*(pstar+bk)))*np.sqrt(ak/(pstar+bk))
    
    # choose
    v = np.where(pstar<pk,vraref,vshock)
    dv = np.where(pstar<pk,dvraref,dvshock)
    
    return v, dv

def exact_solution(S,wleft,wright):
    
    # collect left primitive variables
    dl = wleft[0]
    vl = wleft[1]
    pl = wleft[2]

    # collect right primitive variables
    dr = wright[0]
    vr = wright[1]
    pr = wright[2]

    # compute sound speed
    cl = np.sqrt(gamma*pl/dl)
    cr = np.sqrt(gamma*pr/dr)

    # acoustic first guess
    doco = 0.5*(dl*cl+dr*cr)
    pstar = np.maximum(0.5*(pl+pr)+doco*(vl-vr),1e-10)
    
    # raphson-newton iterations
    for iter in range(0,6):
        vstarl, dvstarl = vs(pstar,dl,vl,pl,cl)
        vstarr, dvstarr = vs(pstar,dr,vr,pr,cr)
        f = vr + vstarr - vl + vstarl
        df = dvstarl + dvstarr
        pstar = pstar - f / df
        
    # compute vstar
    vstarl, dvstarl = vs(pstar,dl,vl,pl,cl)
    vstarr, dvstarr = vs(pstar,dr,vr,pr,cr)
    vstar = 0.5*(vl+vr) + 0.5*(vstarr - vstarl)
#    print("p*=",pstar,"v*=",vstar)
    
    # sample solution at x/t=S

    # left to the contact
    if (S < vstar):
        
        # left rarefaction 
        if(pstar < pl):
            Shead = vl - cl
            # left unperturbed state
            if(S < Shead):
                dg = dl
                vg = vl
                pg = pl
            else:
                cstar = cl*(pstar/pl)**((gamma-1)/(2*gamma))
                Stail = vstar - cstar
                # rarefaction fan
                if(S < Stail):
                    dg = dl*(2/(gamma+1)+(gamma-1)/(gamma+1)*(vl-S)/cl)**(2/(gamma-1))
                    vg = (gamma-1)/(gamma+1)*vl + 2/(gamma+1)*(S+cl)
                    pg = pl*(dg/dl)**gamma
                # left star state
                else:
                    dg = dl*(pstar/pl)**(1/gamma)
                    vg = vstar
                    pg = pstar
                    
        # left shock
        else:
            al = 2/(gamma+1)/dl
            bl = (gamma-1)/(gamma+1)*pl
            Sshock = vl - np.sqrt((pstar+bl)/(dl**2*al))
            # left unperturbed state
            if(S < Sshock):
                dg = dl
                vg = vl
                pg = pl
            # left star state
            else:
                dg = dl*((gamma-1)/(gamma+1)+pstar/pl)/(1+(gamma-1)/(gamma+1)*pstar/pl)
                vg = vstar
                pg = pstar

    # right to contact
    else:
        
        # right rarefaction 
        if(pstar < pr):
            Shead = vr + cr
            # right unperturbed state
            if(S > Shead):
                dg = dr
                vg = vr
                pg = pr
            else:
                cstar = cr*(pstar/pr)**((gamma-1)/(2*gamma))
                Stail = vstar + cstar
                # rarefaction fan
                if(S > Stail):
                    dg = dr*(2/(gamma+1)+(gamma-1)/(gamma+1)*(S-vr)/cr)**(2/(gamma-1))
                    vg = (gamma-1)/(gamma+1)*vr + 2/(gamma+1)*(S-cr)
                    pg = pr*(dg/dr)**gamma
                # right star state
                else:
                    dg = dr*(pstar/pr)**(1/gamma)
                    vg = vstar
                    pg = pstar
                    
        # right shock
        else:
            ar = 2/(gamma+1)/dr
            br = (gamma-1)/(gamma+1)*pr
            Sshock = vr + np.sqrt((pstar+br)/(dr**2*ar))
            # right unperturbed state
            if(S > Sshock):
                dg = dr
                vg = vr
                pg = pr
            # right star state
            else:
                dg = dr*((gamma-1)/(gamma+1)+pstar/pr)/(1+(gamma-1)/(gamma+1)*pstar/pr)
                vg = vstar
                pg = pstar
    return dg,vg,pg

def llf(wleft,wright):
    uleft = prim_to_cons(wleft)
    uright = prim_to_cons(wright)
    fleft = prim_to_flux(wleft)
    fright = prim_to_flux(wright)
    sleft = abs(wleft[1])+np.sqrt(gamma*wleft[2]/wleft[0])
    sright = abs(wright[1])+np.sqrt(gamma*wright[2]/wright[0])
    smax = np.maximum(sleft,sright)
    flux = 0.5*(fleft+fright)-0.5*smax*(uright-uleft)
    return flux

def hll(wleft,wright):
    ul = prim_to_cons(wleft)
    ur = prim_to_cons(wright)
    fl = prim_to_flux(wleft)
    fr = prim_to_flux(wright)
    cl = np.sqrt(gamma*wleft[2]/wleft[0])
    cr = np.sqrt(gamma*wright[2]/wright[0])
    sl = np.minimum(wleft[1],wright[1])-np.maximum(cl,cr)
    sr = np.maximum(wleft[1],wright[1])+np.maximum(cl,cr)
    fstar = ((fl*sr-fr*sl)+sl*sr*(ur-ul))/(sr-sl)
    flux = np.where(sl>0,fl,np.where(sr>0,fstar,fr))
    return flux

def hllc(wleft,wright):
    flux = 0.*wleft
    uleft = prim_to_cons(wleft)
    uright = prim_to_cons(wright)
    # left state
    dl = wleft[0]
    vl = wleft[1]
    pl = wleft[2]
    el = uleft[2]
    # right state
    dr = wright[0]
    vr = wright[1]
    pr = wright[2]
    er = uright[2]
    # sound speed
    cl = np.sqrt(gamma*pl/dl)
    cr = np.sqrt(gamma*pr/dr)
    # waves speed
    sl = np.minimum(vl,vr)-np.maximum(cl,cr)
    sr = np.maximum(vl,vr)+np.maximum(cl,cr)
    dcl = dl*(vl-sl)
    dcr = dr*(sr-vr)
    # star state velocity and pressure 
    vstar = (dcl*vl+dcr*vr+pl-pr)/(dcl+dcr)
    pstar = (dcl*pr+dcr*pl+dcl*dcr*(vl-vr))/(dcl+dcr)
    # left and right star states
    dstarl = dl*(sl-vl)/(sl-vstar)
    dstarr = dr*(sr-vr)/(sr-vstar)
    estarl = ((sl-vl)*el-pl*vl+pstar*vstar)/(sl-vstar)
    estarr = ((sr-vr)*er-pr*vr+pstar*vstar)/(sr-vstar)
    # sample godunov state
    dg = np.where(sl>0,dl,np.where(vstar>0,dstarl,np.where(sr>0,dstarr,dr)))
    vg = np.where(sl>0,vl,np.where(vstar>0,vstar ,np.where(sr>0,vstar ,vr)))
    pg = np.where(sl>0,pl,np.where(vstar>0,pstar ,np.where(sr>0,pstar ,pr)))
    eg = np.where(sl>0,el,np.where(vstar>0,estarl,np.where(sr>0,estarr,er)))
    # compute godunov flux
    flux[0] = dg*vg
    flux[1] = dg*vg*vg+pg
    flux[2] = (eg+pg)*vg
    return flux

def exact(wleft,wright):
    flux = 0*wleft        
    for i in range(0,np.size(wleft,1)):
        dg,vg,pg = exact_solution(0,wleft[:,i],wright[:,i])
        wg = np.reshape([dg,vg,pg],(3))
        fg = prim_to_flux(wg)
        flux[:,i] = fg
    return flux




