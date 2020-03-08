import random
cipher = input("Enter the ciphertext: ")

with open("plaintext_dictionary_test1.txt") as test1:
    lst = test1.readlines()[4::4]

dict1 = {}
for line in range(len(lst)):
    dict1[line] =  lst[line].strip()

print(dict1)

t = random.randint(1, 24)
k = [random.randint(0,26) for i in range(t)]
m = dict1[0]

test_cipher = ""
alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]

for i in range(len(m)):
    alpha = ord(m[i]) - ord('a') + 1
    if m[i] == ' ':
        alpha = 0
    test_cipher += alphabet[(alpha + k[(1 + i) % t]) % 27 ]

print(k, len(k))
print(test_cipher)