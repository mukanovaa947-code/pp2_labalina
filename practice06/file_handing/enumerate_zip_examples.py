#1
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 88]

for i, name in enumerate(names):
    print(i, name)

for n, s in zip(names, scores):
    print(n, s)