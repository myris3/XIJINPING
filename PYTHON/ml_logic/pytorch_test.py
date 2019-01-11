import torch
"""
x = torch.randn(5,5, requires_grad=True)
print(x)
y= x*x
y = y*y*2
print(y.requires_grad)
p=y.mean()
p.backward()
print(p)
print(p.grad)
"""


x = torch.ones(2, 2, requires_grad=True)
print(x)

y = x + 2
print(y)

z = y * y * 3
out = z.mean()

print(z, out)
z = y * y * 3
out = z.mean()

print(z, out)

out.backward()

print(x.grad)

print(y.grad)

print(z.grad)
