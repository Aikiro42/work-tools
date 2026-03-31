# CAESAR'S CIPHER

# 0. Construct cipher
offset = 0
print(f"Caesar Shift: {offset}")
cipher = {}
for i in range(26):
  cipher[chr(65 + i)] = chr(65 + ((i + offset) % 26))

# 1. Encrypt plaintext
plaintext = """In an era of constant innovation, the essential nature of secure communication remains vital to national defense and economic stability. Every operation requires careful planning, accurate intelligence, and resilient execution to ensure effective protection against emerging threats."""  # include full alphabet for easier full coverage.
plaintext = plaintext.upper()

ciphertext = ""

for p in plaintext:
  c = cipher.get(p, None)
  if c is None:
    ciphertext += p
  else:
    ciphertext += c
print("\nCIPHERTEXT: ")
print(ciphertext)

# 2. Count letter occurences in ciphertext
counts = {}
for c in ciphertext:
  if c in cipher.keys():
    if c in counts.keys():
      counts[c] += 1
    else:
      counts[c] = 1
  else:
    continue

freqs = {}
i = 0
for c in counts.keys():
  freqs[c] = counts[c]/sum(counts.values())
  i += 1

print("\nCIPHERTEXT FREQUENCIES: ")
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
  print(f"{k}\t{v}")
  ...

# Determine plaintext frequencies
engtbl = """
E	21912
T	16587
A	14810
O	14003
I	13318
N	12666
S	11450
R	10977
H	10795
D	7874
L	7253
U	5246
C	4943
M	4761
F	4200
Y	3853
W	3819
G	3693
P	3316
B	2715
V	2019
K	1257
X	315
Q	205
J	188
Z	128
"""

engcounts = {}
for txt in engtbl.split("\n"):
  # print(txt)
  vals = txt.split("\t")
  if len(vals) != 2: continue
  engcounts[vals[0]] = int(vals[1])

engsum = sum(engcounts.values())

engfreq = {}
for L in engcounts:
  engfreq[L] = engcounts[L]/engsum


print("\nPLAINTEXT FREQUENCIES: ")
print(engfreq.keys())

# Align frequencies
sorted_cipher = [z[0] for z in sorted(counts.items(), key=lambda x: -x[1])]
sorted_plain = ('E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'D', 'L', 'U', 'C', 'M', 'F', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q', 'J', 'Z')
decipher = {}
for c, p in zip(sorted_cipher, sorted_plain):
  decipher[c] = p

print("\nALIGNED FREQUENCIES: ")
for k, v in decipher.items():
  print(f"{k}\t{v}")

deciphertext = ""
for c in ciphertext:
  if c in decipher.keys():
    deciphertext += decipher[c]
  else:
    deciphertext += c


print("\nDECIPHERED: ")
print(deciphertext)