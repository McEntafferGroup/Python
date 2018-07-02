from numpy import *
from scipy import io 
from scipy.ndimage.measurements import center_of_mass


def CenterOfMass1(im):
    
    vec = im
    r,c = shape(im)
    
    """break into a bunch of columns"""
    columns = hsplit(vec,c)
    """sum each column"""
    summedx = array([sum(i) for i in columns])
    """find the max"""
    m = max(summedx)
    """WHERE IT AT THO"""
    x = where(summedx==m)
    
    """break into a bunch of rows"""
    rows = hsplit(vec,r)
    """sum each column"""
    summedy = array([sum(i) for i in rows])
    """find the max"""
    m = max(summedy)
    """WHERE IT AT THO"""
    y = where(summedy==m)
    
    return y,x


def CenterOfMass2(im):
    
    vec = im
    rows,cols = shape(im)
    
    y = 0
    x = 0
    
    per = vec/sum(vec)
    
    y,x = center_of_mass(vec)
    
    return y,x

if __name__ == '__main__':
    abc = io.loadmat('C:/Users/PSU_Telemetry/Documents/WORKPLACE(CHRIS)/Python/Test Images/Test Images/gaussLineTest')
    
    abc = abc['gFilter']
    
    y,x = CenterOfMass1(abc)
    
    print('x =',x)
    print('y =',y)
    
    
    
    
    
    
    