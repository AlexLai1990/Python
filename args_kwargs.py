#refer: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/

# we can use *args to store the upcoming argument in the input
# and those args will be store in a tuple
def test(a, b ,*args):
	print a, b, args
test(1,2,3,4,5,6,"alex",0.9)

# we can use **kwargs to indicate that all uncaptured keyword arguments should be stored in a dictionary called kwargs.
def foo(**kwargs):
	print kwargs
m_dict = {"alex":1, "abc":2}
foo(**m_dict)


