import random


#list of letters in the message space
alphabet = [' '] + [chr(i + ord('a')) for i in range(26)]
#mapping of each letter to its number
alphabet_map = {}
for i in range(len(alphabet)):
    alphabet_map[alphabet[i]] = i

def create_ciphertext(m, k, t):
    test_cipher = ""

    for i in range(len(m)):
        alpha = ord(m[i]) - ord('a') + 1
        if m[i] == ' ':
            alpha = 0
        test_cipher += alphabet[(alpha + k[(1 + i) % t]) % 27 ]

    # print(k, len(k))
    # print(test_cipher)
    return test_cipher



def get_distribution(cipher):
    dist = [0 for i in range(len(alphabet))]
    for c in cipher:
        dist[alphabet_map[c]] += 1
    return dist

def invert_cipher1_helper(poss_plaintext, c):
    success = 0
    #Gonna brute force the length of the key
    for t in range(1, 24):
        correct = 0
        for k_i in range(0, t): #each letter in the key
            c_str = ""
            #step of t bc that's when the key repeats
            for i in range(k_i, len(c), t):
                c_str += c[i]
            poss_plaintext1 = ""
            for i in range(k_i, len(poss_plaintext), t):
                #get the t_th letters from the possible plaintext to compare distributions
                poss_plaintext1 += poss_plaintext[i]

            #Get distributions of letters
            if sorted(get_distribution(c_str)) == sorted(get_distribution(poss_plaintext1)):
                correct +=1

        success = max(success, correct)
    return success

def invert_cipher1(c, dict1):
    success = invert_cipher1_helper(dict1[0], c)
    succ_ind = 0
    for i in range(len(list(dict1.values()))):
        curr = invert_cipher1_helper(dict1[i], c)
        if curr > success:
            succ_ind = i
            success = curr
    return dict1[succ_ind]

def create_ciphertext2(m, k, t):
    pass

def main():
    with open("plaintext_dictionary_test1.txt") as test1:
        lst = test1.readlines()[4::4]

    dict1 = {}
    for line in range(len(lst)):
        dict1[line] =  lst[line].strip()

    t = random.randint(1, 24)
    k = [random.randint(0,26) for i in range(t)]
    m = dict1[4]
    print("### Testing ###")
    print("message is: ", m)
    test_cipher1 = create_ciphertext(m, k, t)
    print("cipher is: ", test_cipher1)
    print("### End Testing ###\n")

    cipher = input("Enter the ciphertext: ")

    print("Original plaintext is: ", invert_cipher1(cipher, dict1))

    print("\ntask 2 plaintext")
    with open("word_dictionary_test2.txt") as test2:
        dictionary_2 = [line.strip() for line in test2.readlines()]
        task2_plaintext = ""
        while len(task2_plaintext) <= 500:
            new_word = random.choice(dictionary_2)
            if len(new_word) + len(task2_plaintext) >= 500:
                break
            else:
                task2_plaintext += new_word + ' '
    print(task2_plaintext, len(task2_plaintext))

    t2 = random.randint(1, 24)
    k2 = [random.randint(0,26) for i in range(t)]
    c2 = create_ciphertext(task2_plaintext, k2, t2)
    print("cipher for task 2: ", c2)



main()
