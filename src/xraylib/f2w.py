#
# f2w-package by V. Honkim\"aki
#
# Copyright 2012 European Synchrotron Ratiation Facility
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#  example:
#   >>> import edf                # or however you load the edf-files
#   >>> import f2w                # import the detector classes
#   >>> Det=f2w.Pixium()          # object for the Pixium detector
#   >>> print(Det)                # ...just to see what parameters it holds
#   >>> P=edf.read("pix.edf")     # reading the 2d pattern from the edf-file
#   >>> Det.calibrate(P,[10,130]) # calibrating the center and the tilt using
#                                 # all the data between 10mm < radius < 130mm
#   >>> r,A=Det.integrate(P,1)    # integrates over the whole 2pi
#   >>> r,A=Det.integrate(P,N)    # integrates N pies
#
from numpy import zeros, pi, meshgrid, arange, sqrt, arctan2, isnan, floor, prod,\
                  trunc, nonzero, diff, hstack, vstack, int_, transpose, linalg, \
                  dot, sin, cos

class Detector:
    _R = []
    _T = []
    _updated   = False
    """A general detector object"""
    def setdist(self,D):
       self._distance = D; self._updated = False;
    def setorigin(self,v):
       self._origin = v; self._updated = False;
    def settilt(self,v):
       self._tilt = v; self._updated = False;
    def __str__(self):
       s = 'Distance = ' + repr(self._distance) + 'mm\nOrigin   = ' + repr(self._origin) \
         + 'mm\nTilt     = ' + repr(self._tilt) + 'deg\nPixels   = ' + repr(self._pixels)\
         + '\nPixsize  = ' + repr(self._pixelsize) + 'mm';
       return(s)
    def _calcrt(self):
        if (not self._updated):
           r = pi/180.0/self._distance
           a = self._tilt[0]*r; b = self._tilt[1]*r;
           xv = arange(self._pixels[1])*self._pixelsize[1]-self._origin[1]
           yv = arange(self._pixels[0])*self._pixelsize[0]-self._origin[0]
           x,y = meshgrid(xv,yv)
           self._R = sqrt(x**2+y**2)*(1.0-a*y-b*x); self._T = arctan2(y,x); self._updated = True
           self._R.shape = prod(self._R.shape); self._T.shape = prod(self._T.shape); 
    def integrate(self,Im,n):
       if (not self._updated):
          self._calcrt();
       R = self._R[:]; T = self._T[:]; Imc = Im[:]; Imc.shape = prod(Imc.shape);
       dr = sqrt(self._pixelsize[0]*self._pixelsize[1])
       if (1 < n):
          tpi = 2.0*pi; dp = tpi/n; ip = int_(floor(T/dp+0.5)%n); A = zeros([0,n]);
          for i in range(n):
             j = nonzero(ip == i); a = self._pie(Imc[j],R[j],dr); M = a.shape[0]; m = A.shape[0];
             if (m < M):
                A = vstack((A,zeros([M-m,n])))
             a.shape = M; A[:M,i] = a;
       else:
           A = self._pie(Imc,R,dr);
       m = A.shape[0]; r = arange(m)*dr; r.shape = [m,1]; return(r,A)
    def _pie(self,Im,R,dr):
       mn = prod(Im.shape); j = R.argsort(axis=None); w = R[j]/dr;
       ir = int_(w); w0 = 1.0+ir-w; w1 = 1.0-w0; c0 = w0*Im[j]; c1 = w1*Im[j];
       i = isnan(Im[j]); w0[i] = 0; w1[i] = 0; c0[i] = 0; c1[i] = 0;
       w0 = w0.cumsum(); w1 = w1.cumsum(); c0 = c0.cumsum(); c1 = c1.cumsum();
       i = nonzero(diff(ir)); m = ir[-1]+2; A = zeros([m,1]); C = zeros([m,1]);
       ta = diff(hstack((0,c0[i]))); tc = diff(hstack((0,w0[i]))); j = ir[i]; A[j,0] = ta; C[j,0] = tc;
       ta = diff(hstack((0,c1[i]))); tc = diff(hstack((0,w1[i]))); j += 1; A[j,0] += ta; C[j,0] += tc;
       j = nonzero(C); A[j] = A[j]/C[j]; return(A);
    def calibrate(self,Im,rg):
       D = self._distance; stp = 1; loops = 0; N = 36; dp = 2*pi/N; p = arange(N)*dp-dp/2;
       y = zeros([N,1]); z = zeros([N,1]); dy = zeros([N,1]); dz = zeros([N,1]);
       sc = 2*pi/sqrt(self._pixelsize[0]*self._pixelsize[1]);
       while ((0.1 < stp) and (loops < 30)):
          r,A = self.integrate(Im,N); i = nonzero((rg[0] < r)*(r < rg[1]))[0]; r = r[i,:]; A = A[i,:];
          d = diff(A[:,-1])/diff(r[:,0]); C = vstack((A[:-1,-1],d,d*r[:-1,0]**2/D)).T;
          for j in range(N):
             w = sc*r[:-1,0]/(A[:-1,j]+1); Cs = (C*w[:,[0,0,0]]).T; db = linalg.inv(dot(Cs,C));
             b = dot(db,dot(Cs,A[:-1,j])); y[j] = b[1]/b[0]; z[j] = b[2]/b[0];
             c = hstack((1,-y[j]))/b[0]; c.shape = [1,2]; dy[j] = dot(c,dot(db[[1,0],:][:,[1,0]],c.T));
             c = hstack((1,-z[j]))/b[0]; c.shape = [1,2]; dz[j] = dot(c,dot(db[[2,0],:][:,[2,0]],c.T));
             d = diff(A[:,j])/diff(r[:,0]); C = vstack((A[:-1,j],d,d*r[:-1,0]**2/D)).T;
          y = y/dp; z = z/dp; dy = dy/dp**2; dz = dz/dp**2; C = vstack((cos(p),-sin(p))).T;
          w = (1/dy); Cs = (C*w[:,[0,0]]).T; db = linalg.inv(dot(Cs,C)); c = dot(db,dot(Cs,y));
          stp = sum(c**2); q = c/stp; stp = stp/dot(dot(q.T,db),q); c.shape = 2;
          self.setorigin(self._origin - c); C = vstack((cos(p),-sin(p))).T; w = (1/dz);
          Cs = (C*w[:,[0,0]]).T; db = linalg.inv(dot(Cs,C)); c = dot(db,dot(Cs,z));
          stp2 = sum(c**2); q = c/stp2; stp2 = stp2/dot(dot(q.T,db),q); c.shape = 2;
          self.settilt(self._tilt - c*180/pi); stp = sqrt(stp+stp2); loops += 1;
          print("Step = {0:.3f}".format(stp[0,0]))

class Pixium(Detector):
    """Pixium detector object"""
    def __init__(self):
       self._distance  = 1000
       self._origin    = [147.84,203.28]
       self._tilt      = [0,0]
       self._pixels    = [1920,2640]
       self._pixelsize = [0.154,0.154]
