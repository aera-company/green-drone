import math, json, numpy as np
from scipy.optimize import least_squares
import solve_camera as sc
G=list(sc.OBS)
def pts(s,phases):
    out={}; rr=sc.D/2-0.035*sc.D/2
    for g,ph in zip(G,phases):
        o=sc.OBS[g]; cx,cy=o["c"][0]*s*sc.D,o["c"][1]*s*sc.D; arm=math.atan2(-cy,-cx)
        out[g]=(np.array([cx,cy,0.]),np.array([(cx+rr*math.cos(arm+math.radians(ph)+k*math.pi/3),cy+rr*math.sin(arm+math.radians(ph)+k*math.pi/3),0.) for k in range(6)]))
    return out
def res(x):
    cam,s,ph=x[:8],x[8],x[9:12]; r=[]
    mp=pts(s,ph)
    for g,o in sc.OBS.items():
        hub,ends=mp[g]; r+=list(sc.project(hub[None],cam)[0]-np.array(o["hub"]))
        pe=sc.project(ends,cam)
        for p in o["screws"]:
            j=int(np.argmin(np.linalg.norm(pe-np.array(p),axis=1))); r+=list(pe[j]-np.array(p))
    return np.array(r)
best=None
for az0 in (125,140,155):
  for el0 in (30,40,50):
    for f0 in (25,40):
      for p0 in (-30,0,30):
        rr=least_squares(res,[az0,el0,1.1,f0,0,0,-0.1,0,0.65,p0,p0,p0],bounds=([60,5,0.4,15,-.3,-.3,-.3,-20,0.45,-60,-60,-60],[200,80,5,200,.3,.3,.3,20,1.0,60,60,60]))
        if best is None or rr.cost<best.cost: best=rr
names=["az","el","dist","focal","tx","ty","tz","roll","s","phFL","phBL","phFR"]
print("RMS",round(math.sqrt(np.mean(best.fun**2)),2),dict(zip(names,np.round(best.x,2))))
print(np.round(np.linalg.norm(best.fun.reshape(-1,2),axis=1),1))
