from numpy import arcsin, array, cos, cross, exp, nonzero, ones, \
		  pi, sin, sqrt

def elcom(hkl,ver,chi):
   y = cross(ver,hkl); y /= sqrt(sum(y**2));
   z = array(hkl); z = z/sqrt(sum(z**2));
   c = cos(pi*chi/180); s = sin(pi*chi/180);
   hz = z[0]*c-y[0]*s; kz = z[1]*c-y[1]*s; lz = z[2]*c-y[2]*s;
   hy = z[0]*s+y[0]*c; ky = z[1]*s+y[1]*c; ly = z[2]*s+y[2]*c;

   s11 = 7.68; s12 = -2.14; s44 = 12.6; sa = s11-s12-s44/2;

   s33 = s12+s44/2+(hz**4+kz**4+lz**4)*sa;
   s23 = s12+(hz**2*hy**2+kz**2*ky**2+lz**2*ly**2)*sa;
   s34 = 2*(hz**3*hy+kz**3*ky+lz**3*ly)*sa;
   return(s33,s23,s34);
   
def bw(hkl,ver,chi,E,T,D):
   s33,s23,s34 = elcom(hkl,ver,chi); d = 5.43/sqrt(sum(array(hkl)**2));
   th = arcsin(6.1993/(E*d)); x = pi*chi/180; sx = sin(x); cx = cos(x);
   a = sx-(s23*sx+s34*cx)/s33; g = cos(x+th)*cos(x-th);
   return(-E*T*(sx+g*a)/(D*sin(th)),th*180/pi);
   
def teff(mu,T,th,chi):
   cp = abs(cos(pi*(th+chi)/180)); cm = abs(cos(pi*(th-chi)/180));
   s = ones(chi.shape); p = ones(chi.shape);
   j = nonzero(abs(chi) < 90-abs(th)); s[j] = -1; p[j] = exp(-mu*T/cm[j]);
   te = p*(1-exp(-mu*T*(1/cp+s/cm)))/(mu*(1+cp*s/cm));
   i = nonzero(abs(cp+s*cm)<1.0e-10); te[i] = T*p[i]/cp[i];
   return(te*cp)

def rint(hkl,ver,chi,E,T,D,mu):
   w,th = bw(hkl,ver,chi,E,T,D);
   t = teff(mu,T,th,chi);
   return(abs(w)*t/T);
