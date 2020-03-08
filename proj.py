import random
cipher = input("Enter the ciphertext: ")

with open("plaintext_dictionary_test1.txt") as test1:
    lst = test1.readlines()[4::4]

dict1 = {}
for line in range(len(lst)):
    dict1[line] =  lst[line].strip()

# print(dict1)

t = random.randint(1, 24)
k = [random.randint(0,26) for i in range(t)]
m = dict1[2]
print("message is: ", m)


#list of letters in the message space
alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
inv_alphabet = {}
for i in range(len(alphabet)):
    inv_alphabet[alphabet[i]] = i

def create_ciphertext(m):
    test_cipher = ""

    for i in range(len(m)):
        alpha = ord(m[i]) - ord('a') + 1
        if m[i] == ' ':
            alpha = 0
        test_cipher += alphabet[(alpha + k[(1 + i) % t]) % 27 ]

    print(k, len(k))
    print(test_cipher)
    return test_cipher

test_cipher1 = create_ciphertext(m)

def invert_cipher1_helper(poss_plaintext, c):
    success = 0
    for t in range(1, 24):
        correct = 0
        for j in range(0, t):
            c_str = ""
            #step of t bc that's when the key repeats
            for i in range(j, len(c), t):
                c_str += c[i]
            poss_plaintext1 = ""
            for i in range(j, len(poss_plaintext), t):
                poss_plaintext1 += poss_plaintext[i]
            if poss_plaintext == poss_plaintext1:
                correct +=1
        success = max(success, correct)
    return success

def invert_cipher1(c):
    success = invert_cipher1_helper(dict1[0], c)
    succ_ind = 0
    for i in range(len(list(dict1.values()))):
        curr = invert_cipher1_helper(dict1[i], c)
        print(curr)
        if curr > success:
            succ_ind = i
            success = curr
    return dict1[succ_ind]

print(invert_cipher1(test_cipher1))