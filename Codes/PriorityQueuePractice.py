import heapq

heap= []
data = []

class A():
    def __init__(self, name=0):
        self.name = name

li = []

def priority(x):
    return len(x[0])

li.append(('wfewjfawefwaf',A('awefef') ))
li.append(('a', 432))
li.append(('wefkfe', 'wefwwwwwwwe'))

li.sort(key= priority)
li= li[::-1]

print(li)

for val in li:
    if type(val[1]) == type(A()) :
        print(val[1].name)
