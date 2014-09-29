from libcloudphxx.common import R_d, c_pd, g, p_1000
from numpy import array as arr_t

# p_d, th_d, r_v should contain initial values
#                and are overwritten!
def parcel(p_d, th_d, r_v, w, nt, outfreq, rhs):

  # perfect gas for for dry air
  def rhod_fun(p_d, th_d):
    def T(p_d, th_d):
      return th_d * pow(p_d / p_1000, R_d / c_pd)
    return p_d / R_d / T(p_d, th_d)

  # t=0 stuff
  rhod = rhod_fun(p_d, th_d)
  rhs.init(rhod, th_d, r_v)
  rhs.diag(rhod, th_d, r_v, 0)

  # placing a quick-look gnuplot file in the output directory
  import os, shutil
  shutil.copyfile(os.path.dirname(__file__) + '/quicklook.gpi', rhs.outdir + '/quicklook.gpi')

  # Euler-like integration
  for t in range(nt):
    #TODO: update process name :)

    # first, adjusting thr pressure using hydrostatic law
    p_d += rhs.dt * (-g * rhod * w)

    # computing rhs for th and rv
    dot_th = arr_t([0.])
    dot_rv = arr_t([0.])
    rhod = rhod_fun(p_d, th_d)
    rhs.step(rhod, th_d, r_v, dot_th, dot_rv)

    # applying the rhs
    th_d += rhs.dt * dot_th
    r_v  += rhs.dt * dot_rv
    rhod = rhod_fun(p_d, th_d)

    # doing diagnostics / output
    if ((t+1) % outfreq == 0): #TODO: should be t or t+1?
      rhs.diag(rhod, th_d, r_v, (t+1) * rhs.dt) #TODO: should be t or t+1?
