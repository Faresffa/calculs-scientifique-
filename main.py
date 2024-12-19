import numpy
import matplotlib.pyplot as plt
#prend x qui est un seul nombre d    


#def f1(x):
    #return x**2 -8-math.log(x)

#prend x qui est un seul nombre d 
def f(x):
    return x**2 - 8 * numpy.log(x)
#prend un array et renvoie un array 


def solve_equation(f, left, right, precision=10**(-3)) :
    while right - left >= precision :
        middle = (right + left) / 2
        if f (middle) == 0 :
            break
        elif f(left) * f(middle) < 0 :
            right = middle
        elif f(right) * f(middle) < 0 :
            left = middle
        return middle

def plot_fct(f, start, end, step):
    x=numpy.arange(start, end, step)
    y = f(x)
    plt.figure(figsize=(15,6))
    plt.plot(x,y)
    plt.show()
    

    
if __name__ == "__main__":
    plot_fct(f, start=0.01, end=5, step=0.01)
    x = numpy.array([1, 2, 3])
    y = f(x)
    print(y)
    middle = solve_equation(f, left=1, right=2)
    print(middle)
    print(f(middle))
