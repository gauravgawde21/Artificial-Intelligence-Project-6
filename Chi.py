__author__ = 'gp'

import math
import sys;

class Chi:
    '''
    static double BIGX = 20.0;  /* max value to represent exp(x) */
    '''
    def __init__(self):
        self.BIGX = 20.0;

    def poz(self, z):
        #Maximum meaningful z value
        Z_MAX = 6.0

        if(z == 0.0):
            x = 0.0
        else:
            y =  0.5 * math.fabs(z);
            if ( y >= (Z_MAX * 0.5)):
                x = 1.0
            else:
                if ( y < 1.0 ):
                    w = y * y;
                    x = ((((((((0.000124818987 * w - 0.001075204047) * w + 0.005198775019) * w - 0.019198292004) * w + 0.059054035642) * w - 0.151968751364) * w + 0.319152932694) * w - 0.531923007300) * w + 0.797884560593) * y * 2.0;
                else:
                    y = y - 2.0;
                    x = (((((((((((((-0.000045255659 * y
						+ 0.000152529290) * y - 0.000019538132) * y
						- 0.000676904986) * y + 0.001390604284) * y
						- 0.000794620820) * y - 0.002034254874) * y
						+ 0.006549791214) * y - 0.010557625006) * y
						+ 0.011630447319) * y - 0.009279453341) * y
						+ 0.005353579108) * y - 0.002141268741) * y
						+ 0.000535310849) * y + 0.999936657524;
        if(z > 0.0):
            ret_val = ((x + 1.0) * 0.5)
        else:
            ret_val = ((1.0 - x) * 0.5)
        return ret_val;

    def ex(self, x):
        if(x < -(self.BIGX)):
            ret_val = 0.0;
        else:
            ret_val = math.exp(x)
        return ret_val

    def pochisq(self, x, df):

        #log(sqrt(pi))
        LOG_SQRT_PI = 0.5723649429247000870717135;
        #1 / sqrt(pi)
        I_SQRT_PI   = 0.5641895835477562869480795;
        y = 0;

        if (x <= 0.0 or df  < 1):
            return 1.0;

        a = (0.5 * x);
        even = (df % 2 == 0);
        if (df > 1):
            y = self.ex(-a)

        if (even):
            s = y
        else:
            s = (2.0 * self.poz(-(math.sqrt(x))))

        if( df > 2 ):
            x = 0.5 * (df - 1.0);

            if(even):
                z = 1.0
            else:
                z = 0.5

            if ( a > self.BIGX ):
                if(even):
                    e = 0.0
                else:
                    e = LOG_SQRT_PI

                c = math.log(a);
                while (z <= x):
                    e = math.log(z) + e;
                    s = s + self.ex((c * z) - a - e);
                    z = z + 1.0;
                return s;
            else:
                if(even):
                    e = 1.0
                else:
                    e = (I_SQRT_PI / math.sqrt(a))
                c = 0.0;
                while (z <= x):
                    e = (e * (a / z));
                    c = (c + e);
                    z = (z + 1.0);
                return ((c * y) + s);
        else:
            return s

    def critchi(self, p, df):

        CHI_EPSILON = 0.000001;   # Accuracy of critchi approximation
        CHI_MAX     = 99999.0;    # Maximum chi-square value
        minchisq    = 0.0;
        maxchisq    = CHI_MAX;

        if( p <= 0.0):
            return maxchisq;
        else:
            if(p >= 1.0):
                return 0.0;

        chisqval = (df / math.sqrt(p));    #fair first value

        while ((maxchisq - minchisq) > CHI_EPSILON):
            if (self.pochisq(chisqval, df) < p):
                maxchisq = chisqval;
            else:
                minchisq = chisqval;
            chisqval = ((maxchisq + minchisq) * 0.5);

        return chisqval;

#Acts like main()
class InitProcess:
    def init_app(self):
        chi_obj = Chi();

        df = 1;
        while(df <= 100):
            #print df,"::",round(chi_obj.critchi(0.05,df),2),"::",round(chi_obj.critchi(0.01,df),2);
            df = (df + 1);

init_obj = InitProcess();
init_obj.init_app();