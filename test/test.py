@transpile
class ty:
	a:int
	def __init__(self,a):
		self.a=a
@transpile
def foo(a:ty):
	b:ty[int,int]
	pass