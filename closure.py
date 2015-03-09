
# closure, the inside function have closure info to find the local varible in outer function 
def make_printer(msg):
    def printer():
        print msg
    return printer

printer = make_printer('Foo!')
printer()

# decorator
# 1. use function entryExit(f):

def entryExit(f):
    def new_f():
        print "Entering", f.__name__
        f()
        print "Exited", f.__name__
    return new_f

@entryExit
def func1():
    print "inside func1()"

@entryExit
def func2():
    print "inside func2()"

func1()
func2()
print func1.__name__


# 2. use class entryExit(object):

'''
class entryExit(object):
	def __init__(self, f):
		self.f = f

	def __call__(self):
		print "Entering", self.f.__name__
		self.f()
		print "Exited", self.f.__name__

@entryExit
def func1():
    print "inside func1()"

@entryExit
def func2():
    print "inside func2()"
	
	

func1()
func2()
''' 