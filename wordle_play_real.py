import matplotlib.pyplot as plt
import random
import numpy as np
import argparse
import copy
import statistics

import time
#from extract_for_wordle import extract_wordlist


parser = argparse.ArgumentParser(description='For test and so on')

def extract_wordlist(try_wordlist, f, word):
    for i, a in enumerate(f):
        if word.count(word[i]) >= 2:
            if a == 2:
                a = 1
        if a == 2:
            try_wordlist = [s for s in try_wordlist if word[i] not in s]

        if a == 1:
            #try_wordlist = try_wordlist[np.where((try_wordlist[:, i] != word[i]))]
            try_wordlist = [s for s in try_wordlist if word[i] != s[i]]

        if a == 0:
            #try_wordlist = try_wordlist[np.where((try_wordlist[:, i] == word[i]))]
            try_wordlist = [s for s in try_wordlist if word[i] == s[i]]

    return try_wordlist


def find_word(word, find, find_word_list):

    for i, (w, a) in enumerate(zip(word, find)):
        """if a == 0:
            find_word_list = find_word_list[np.where(find_word_list[:, i] == w)]"""
    for i, (w, b) in enumerate(zip(word, find)):
        if b == 1:
            new_list = []
            for list in find_word_list:
                if w in list:
                    new_list.append(list)
            find_word_list = new_list


    #word list
    return find_word_list

def return_find(word, find):
    for i in range(4):
        if find[i] == 1:
            find[i] = 2

    for i, w in enumerate(word):
        if w == correct_word[i]:
            find[i] = 0
    for i, w in enumerate(word):
        if w in correct_word and find[i] == 2:
                find[i] = 1

    return find

def test(find, ex_word, try_wordlist):
    #check
    if np.sum(find) == 0:
        if not use_eval:
            print("Congratulation!!!")
        return 0


    # Not a single letter has yet been found.
    if np.sum(find) == 2*4:
        if ex_word != []:
            try_wordlist = extract_wordlist(try_wordlist, find, ex_word)
        num = len(try_wordlist)
        index = random.randint(0,num-1)

    else:
        try_wordlist = extract_wordlist(try_wordlist, find, ex_word)
        try_wordlist = find_word(ex_word, find, try_wordlist)
        num = len(try_wordlist)
        if num == 0:
            print("len Error")
            exit(2)
        elif num == 1:
            index = 0
        else:
            index = random.randint(0, num-1)
    if not use_eval:
        print("lest of vocab", num)



    if use_input:
        while True:
            print("input try word : ")
            try_word = input()
            if try_word == "list":
                print(try_wordlist)
                continue
            try_word = list(try_word)
            if len(try_word) == 4:
                break
            print("word must be 4 characters!")
    else:
        if use_super:
            #Calculate which words are the most narrowly defined.
            if args.cheat:
                min_len = 3000
            else:
                min_len = 40000
            if num == num_valid_wordlist: #first time
                if args.cheat:
                    try_word = list("かいうん")
                else:
                    try_word = list("れんぱつ")
            else:
                try_find = copy.deepcopy(find)
                for i in range(4):
                    if try_find[i] == 1:
                        try_find[i] = 2
                for try_few_word in try_wordlist:
                    try_len = len(extract_wordlist(copy.deepcopy(try_wordlist), try_find, try_few_word))
                    if try_len == 0:
                        continue
                    else:
                        if min_len > try_len:
                            try_word = try_few_word
                            min_len = try_len
                if min_len == 3000 or min_len == 40000:
                    #test
                    min_len = 12000
                    for try_few_word in try_wordlist:
                        try_len = 1
                        for i in range(4):
                            if try_find[i] != 0:
                                try_find[i] = 1
                            try_len *= len(extract_wordlist(copy.deepcopy(try_wordlist), try_find, try_few_word))
                        if try_len == 0:
                            continue
                        else:
                            if min_len > try_len:
                                try_word = try_few_word
                                min_len = try_len
                    #######
                    if min_len == 12000:
                        try_word = try_wordlist[index]
                        if min_len >= 10:
                            global error
                            error += 1
                if not use_eval:
                    print("min_len", min_len)

        else:
            try_word = try_wordlist[index]

        ans = ''
        for s in try_word:
            ans = ans + s
        if not use_eval:
            print(ans)
    if use_test:
        print("input correct : ")
        find = list(input())
        find = [int(a) for a in find]
    else:
        find = return_find(try_word, find)
        if not use_eval:
            print(find)

    return test(find, try_word, try_wordlist)+1


def main():
    avg_prob = 0
    prob_array = []
    faild = 0
    #reset find
    #decide correct word
    #prob
    if use_eval:
        global correct_word
        print("input number of eval : ")
        N = int(input())
        start = time.time()
        for i in range(N):
            #reset find
            find = [2]*4
            #decide correct word
            #correct_word = wordlist[random.randint(0,num_wordlist-1)]
            correct_word = wordlist[i]
            #print("Correct word : ",correct_word)
            #prob
            prob = test(find, [], valid_wordlists)
            if prob > 12:
                faild += 1

            prob_array.append(prob)
            avg_prob += prob
            if prob == 1:
                print("WoW first")
            if N > 9:
                if i%int(N/10) == 0:
                    print(i+1, "回 | avg:", avg_prob/(i+1), ", avg faild:", faild/(i+1))
            else:
                print(i+1, "回 | avg:", avg_prob/(i+1), ", avg faild:", faild/(i+1))
        print("Avg prob : ", avg_prob / N, ", Avg faild:", faild/N)
        end = time.time()
        print("total time : ",end - start)
        #plot
        n, bins, patches = plt.hist(prob_array, bins = max(prob_array), color='b')

        plt.grid(True)

        plt.show()

        mode_index = n.argmax()
        # 最も度数の多い階級
        #print('最も度数の多い階級：(' + str(bins[mode_index]) + ',' + str(bins[mode_index+1]) + ')')
        # 最頻値
        print('最頻値：', statistics.mode(prob_array))

    else :
        find = [2]*4

        print("The number of try until finish : ",test(find, [], valid_wordlists))


if __name__ == '__main__':
    use_test = True
    correct_word = []
    #parser
    parser.add_argument('-t', '--test', help='correct word', default = "")
    parser.add_argument('-i','--input', help='self-input', action = "store_true")
    parser.add_argument('-s', '--super', help='super inference', action = "store_true")
    parser.add_argument('-e', '--eval', help='evaluation', action = "store_true")
    parser.add_argument('-c', '--cheat', help='use cheat', action = "store_true")
    args = parser.parse_args()

    correct_word = list(args.test)
    use_input = args.input
    use_super = args.super
    use_eval = args.eval

    with open('./validguess.txt', 'r') as f:
        valid_wordlist = f.read().split('\n')

    with open('./wordlist.txt', 'r') as f:
        wordlists = f.read().split('\n')

    if correct_word != [] or use_eval:
        use_test = False

    # try
    if args.cheat:
        valid_wordlist = wordlists

    num_wordlist = len(wordlists)
    num_valid_wordlist = len(valid_wordlist)

    wordlists = wordlists
    wordlist = []
    for wl in wordlists:
        wordlist.append(list(wl))
    wordlist = wordlist

    valid_wordlist = valid_wordlist
    valid_wordlists = []
    for valid_wl in valid_wordlist:
        valid_wordlists.append(list(valid_wl))
    valid_wordlists = valid_wordlists

    del wordlists
    del valid_wordlist

    #test
    error = 0

    main()
    print(error)

