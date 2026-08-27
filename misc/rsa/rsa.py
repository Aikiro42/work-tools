# cryptology
# Info assurance
from math import pow, gcd

p = 73
q = 67
plaintext = 123

n = p*q
print(f"n=pq={n}")

phi_n = (p-1)*(q-1)
print(f"phi(n)=(p-1)(q-1)={phi_n}")

print("Searching for e...")
e = 277
while gcd(phi_n, e) > 1:
  e += 1
print(f"e={e}")

print("Searching for d...")
d = 1
while (e * d) % phi_n != 1:
  d += 1

print(f"d={d}")

def crypt(msg, key, modulus):
  x = msg
  # X * X * x mod n ==(x*x % n)*x %n
  
  for i in range(key-1):
    x = (x * msg) % modulus
  return x

ciphered = crypt(123, e, n)
print(f"Ciphertext 123 -> {ciphered}")
print(f"Deciphered: {crypt(ciphered, d, n)}")