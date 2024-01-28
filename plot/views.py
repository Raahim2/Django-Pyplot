from django.shortcuts import render
import matplotlib.pyplot as plt
from array import array
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Create your views here.
def index(request):
    return render(request  , "index.html")

def linear(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        linest=request.POST.get('ls')
        cl=request.POST.get('clr')
        w=request.POST.get('wd')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        

        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy = [int(i) for i in yr.strip('[]').split(',')]

        x = array('i', listx)
        y = array('i', listy)

        fig, ax = plt.subplots()
        ax.plot(x, y , ls=linest , c=cl , linewidth = w)
        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "linear.html")

def scatter(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')
        sz=request.POST.get('size')
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        cl=request.POST.get('clr')
        alp=request.POST.get('alpha')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        cm=request.POST.get('cmp')
        mar=request.POST.get('ms')
        


        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy = [int(i) for i in yr.strip('[]').split(',')]
        sizel = [int(i) for i in sz.strip('[]').split(',')]


        x = array('i', listx)
        y = array('i', listy)

        fig, ax = plt.subplots()
        ax.scatter(x, y ,c=cl, s=sizel , alpha=float(alp) , cmap=cm , marker=mar)
        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "scatter.html")

def bar(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        cl=request.POST.get('clr')
        wd=request.POST.get('wdi')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        hor=request.POST.get('hz')

        listx = [int(i) for i in xr.strip('[]').split(',')]
        

        x = array('i', listx)
        y = yr.split(',')
    

        fig, ax = plt.subplots()
        if(hor=="yes"):
            ax.barh(y, x , color=cl , height=float(wd))
            ax.set(xlabel=xl, ylabel=yl, title=tit)
        else:
            ax.bar(y, x , color=cl , width=float(wd))
            ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "bar.html")

def pie(request):
    if request.method =="POST":

        x=request.POST.get('x')
        yr=request.POST.get('y')
        tit=request.POST.get('title')
        ex=request.POST.get('exp')
        r=request.POST.get('rd')
        legend=request.POST.get('lg')
        per=request.POST.get('pr')
        

        listx = [int(i) for i in x.strip('[]').split(',')]
    
        expl=[float(i) for i in ex.split(',')]

        y = yr.split(',')
        x = array('i', listx)
        
        fig, ax = plt.subplots()
        if(per=="yes"):
            ax.pie(x, labels=y ,explode=expl,  radius=float(r) , autopct="%0.2f%%")
            ax.set(title=tit)
        else:
            ax.pie(x, labels=y  ,explode=expl, radius=float(r))
            ax.set(title=tit)
        if(legend=="yes"):
            ax.legend(loc=2)

        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response

    return render(request  , "pie.html")

def histogram(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        cl=request.POST.get('clr')
        ecl=request.POST.get('eclr')
        lw=request.POST.get('lwd')
        b=request.POST.get('bs')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
        listx = [int(i) for i in xr.strip('[]').split(',')]
       
        x = array('i', listx)
        
        fig, ax = plt.subplots()
        ax.hist(x,  color=cl , linewidth=float(lw), edgecolor=ecl , bins=int(b))

        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()

        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request , "histogram.html")

def stem(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')

    
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')

        tit=request.POST.get('title')

        mrs=request.POST.get('ms')
        
        cl=request.POST.get('clr')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
        
        


        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy = [int(i) for i in yr.strip('[]').split(',')]
    


        x = array('i', listx)
        y = array('i', listy)

        fig, ax = plt.subplots()
        ax.stem(x, y ,linefmt=cl,markerfmt=mrs)
        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "stem.html")
    
def stack(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr1=request.POST.get('y1')
        yr2=request.POST.get('y2')
        yr3=request.POST.get('y3')


        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
    
        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy1 = [int(i) for i in yr1.strip('[]').split(',')]
        listy2 = [int(i) for i in yr2.strip('[]').split(',')]
        listy3 = [int(i) for i in yr3.strip('[]').split(',')]

    


        x = array('i', listx)
        y1 = array('i', listy1)
        y2 = array('i', listy2)
        y3 = array('i', listy3)


        fig, ax = plt.subplots()
        ax.stackplot(x, y1,y2,y3 )
        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "stack.html")
    
def stair(request):
    if request.method =="POST":

        xr=request.POST.get('x')
    
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
    
        listx = [int(i) for i in xr.strip('[]').split(',')]
   

        x = array('i', listx)
       


        fig, ax = plt.subplots()
        ax.stairs(x)
        ax.set(xlabel=xl, ylabel=yl, title=tit)
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "stair.html")

def hex(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')
        
    
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
    
        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy = [int(i) for i in yr.strip('[]').split(',')]

   

        x = array('i', listx)
        y = array('i', listy)

        



        fig, ax = plt.subplots()
        ax.hexbin (x , y , gridsize=20)
        ax.set(xlabel=xl, ylabel=yl, title=tit )
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "hex.html")

def trip(request):
    if request.method =="POST":

        xr=request.POST.get('x')
        yr=request.POST.get('y')
    
        xl=request.POST.get('x-l')
        yl=request.POST.get('y-l')
        tit=request.POST.get('title')
        grid=request.POST.get('gd')
        legend=request.POST.get('lg')
        
    
        listx = [int(i) for i in xr.strip('[]').split(',')]
        listy = [int(i) for i in yr.strip('[]').split(',')]

   

        x = array('i', listx)
        y = array('i', listy)

    


        fig, ax = plt.subplots()
        ax.triplot(x , y )
        ax.set(xlabel=xl, ylabel=yl, title=tit )
        if(grid=="yes"):
            ax.grid()
        if(legend=="yes"):
            ax.legend()
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)

        return response
    return render(request  , "trip.html")
    