from functools import reduce

met = {
  'Eric' : ['Jane','John','Mike','Leigh','Todd','Lee','Judy'],
  'Jen' : ['Mark','Mike','Leigh','Jim','Lara','John','Bill'],
  'Terry' : ['Joe','Sara','Reg','Jill','John','Greg','Bryan'],
  'Lara' : ['Pete','Li','Todd','Reg','Jane','Mike','Jen','Ang'],
}
killed = ['Eric', 'Terry']
a = {}
b = met.copy()
for x in killed:
  del b[x]
  a[x] = met[x]
s = set()
for x in a.items():
  s = s.intersection(set(x[1]))
killer = s
for x in b.items():
  s = s.intersection(set(x[1]))
victim = s
print("The killer is {} and the next victim is {}".format(killer, victim))

