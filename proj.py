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

def main():
    ### TASK 1 ###
    with open("plaintext_dictionary_test1.txt") as test1:
        lst = test1.readlines()[4::4]

    dict1 = {}
    for line in range(len(lst)):
        dict1[line] =  lst[line].strip()
    # Picking plaintext
    t = random.randint(1, 24)
    k = [random.randint(0,26) for i in range(t)]
    m = dict1[4]
    print("### Testing ###")
    print("message is: ", m)
    # Generating cipher from plaintext
    test_cipher1 = create_ciphertext(m, k, t)
    print("cipher is: ")
    print(test_cipher1 + ":")
    print("### End Testing ###\n")

    cipher = input("Enter the ciphertext: ")

    print("Original plaintext is: ", invert_cipher1(cipher, dict1))

    ### TASK 2 ###
    print("\ntask 2 plaintext")
    #Generating plaintext
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
    #Generating ciphertext from plaintext
    t2 = random.randint(1, 24)
    k2 = [random.randint(0,26) for i in range(t2)]
    c2 = create_ciphertext(task2_plaintext, k2, t2)
    print("cipher for task 2: ", c2)
    print("key len: ", k2, len(k2))
    print("key len guess: ", find_key_length(c2))

    #Taken from: http://www.macfreek.nl/memory/Letter_Distribution
    eng_let_freq_dict = {   ' ': 0.1831686, 'a': 0.0655307, 'b': 0.0127070, 'c': 0.0226508, 'd': 0.0335227, 'e': 0.1021788,
                            'f': 0.0197180, 'g': 0.0163587, 'h': 0.0486220, 'i': 0.0573425, 'j': 0.0011440, 'k': 0.0056916,
                            'l': 0.0335616, 'm': 0.0201727, 'n': 0.0570308, 'o': 0.0620055, 'p': 0.0150311, 'q': 0.0008809,
                            'r' :0.0497199, 's': 0.0532626, 't': 0.0750999, 'u': 0.0229520, 'v': 0.0078804, 'w': 0.0168961,
                            'x': 0.0014980, 'y': 0.0146995, 'z': 0.0005979
                        }
    eng_let_freq = [0.1831686, 0.0655307, 0.0127070, 0.0226508, 0.0335227, 0.1021788, 0.0197180, 0.0163587, 0.0486220, 
                    0.0573425, 0.0011440, 0.0056916, 0.0335616, 0.0201727, 0.0570308, 0.0620055, 0.0150311, 0.0008809,
                    0.0497199, 0.0532626, 0.0750999, 0.0229520, 0.0078804, 0.0168961, 0.0014980, 0.0146995, 0.0005979
                ]
    


#New f(x)s for task 2
def subkey(cipher, t):
    subkeys = ["" for poss_t in range(t)]
    for i in range(len(cipher)):
        subkeys[i % t] += cipher[i]
    return subkeys

#Using Index of Coincidence approach
def coincidence(poss_key):
    num = get_distribution(poss_key)
    upper = sum([x * (x - 1) for x in num])
    lower = len(poss_key) * (len(poss_key) - 1)
    return upper / lower
    
def find_key_length(cipher):
    key_len = 0
    min_key_len = 1
    for i in range(2, 24):
        subkeys = subkey(cipher, i)
        diff = sum([abs(0.0667 - coincidence(poss_key)) for poss_key in subkeys]) / len(subkeys)
        if diff < min_key_len:
            key_len = i
            min_key_len = diff
    
    return key_len

main()
