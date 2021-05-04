import sys
import os
import time
import random

uni_cnt = {}
bi_cnt = {}
p_cnt = {}
sentence_rice = [
    ["나는", "너는", "노는", "나눈", "내는", "누는", "누난", "난은", "넌은", "눈은", "논은"],
    ["밥을", "법을", "바블", "밤을", "범을", "밥은", "법은", "밥울", "법운", "밥운"],
    ["좋아했다", "조하했다", "조아햇다", "좋아햇따", "조아햇따", "조하해따", "조하햇다", "즣아했다", "졸아했다", "졸아햇다"]
]
sentence_picture = [
    ["사진을", "서진을", "소진을", "사전을", "사진울", "사딘을"],
    ["찍으러", "찍으로", "찍으라", "찍우러", "짝으로", "짝으러"],
    ["공원에", "공원애", "공언에", "공운에", "공뭔에", "곰원에"],
    ["갔다", "갔따", "갓따", "갓다", "겄다", "것따", "깄다", "샀다", "닸다"]
]

#unigram과 bigram을 카운트하는 함수
def get_cnt(alltext):
    textlen = len(alltext)
    for i in range(textlen-1):
        if alltext[i] in uni_cnt : uni_cnt[alltext[i]] += 1
        else : uni_cnt[alltext[i]] = 1

        if alltext[i]+alltext[i+1] in bi_cnt : bi_cnt[alltext[i]+alltext[i+1]] += 1
        else : bi_cnt[alltext[i]+alltext[i+1]] = 1
    #마지막 문자 처리
    if alltext[textlen-1] in uni_cnt : uni_cnt[alltext[textlen-1]] += 1
    else : uni_cnt[alltext[textlen-1]] = 1

#uni_cnt, bi_cnt를 활용하여 확률 계산
def get_per():
    for key, value in bi_cnt.items():
        p_cnt[key] = bi_cnt[key]/uni_cnt[key[0]]

#문장 생성 확률을 계산하는 함수 - 실제 확률은 100000000000을 나눠야함
def get_sentence_probability(gen):
    p = 100000000000
    for i in range(len(gen)-1):
        if gen[i]+gen[i+1] in p_cnt :
            p *= p_cnt[gen[i]+gen[i+1]]
        else :
            p *= 0.0001
    return p

#입력 예제 문장(문제1) 확률 계산 - 실제 확률은 100000000000을 나눠야함
def get_sentence_probability_problem1():
    sentence_list = [
        '나는 밥을 좋아했다', '나는 법을 좋아했다', '너는 밥을 좋아햇다', '노는 법을 조아해따', 
        '사진을 찍으러 공원에 갔다', '사진을 찍으로 공원에 갔다'
        ]
    for stc in sentence_list:
        p = 100000000000
        for i in range(len(stc)-1):
            if stc[i]+stc[i+1] in p_cnt :
                p *= p_cnt[stc[i]+stc[i+1]]
            else : #해당 bigram이 없는 경우라면 굉장히 작은 값으로 곱해줌
                p *= 0.000001
        print("The probability of %s : %e"%(stc, p))

if __name__ == "__main__" :

    start = time.time()
    if len(sys.argv) != 2 :
        print("python hw2.py textfile")
        sys.exit(1)
    f = open(sys.argv[1], 'r', encoding='UTF-8')
    readtext = f.read()
    get_cnt(readtext)
    get_per()
    get_sentence_probability_problem1()
    
    #problem2 - 철자/발음 유사 문장을 구성(밥 문장과 사진 문장)
    stc_rice = {}
    for i in range(len(sentence_rice[0])):
        for j in range(len(sentence_rice[1])):
            for k in range(len(sentence_rice[2])):
                tmp = sentence_rice[0][i]+" "+sentence_rice[1][j]+" "+sentence_rice[2][k]
                stc_rice[tmp] = get_sentence_probability(tmp)

    stc_picture = {}
    for i in range(len(sentence_picture[0])):
        for j in range(len(sentence_picture[1])):
            for k in range(len(sentence_picture[2])): 
                for z in range(len(sentence_picture[3])):
                    tmp = sentence_picture[0][i]+" "+sentence_picture[1][j]+" "+sentence_picture[2][k]+" "+sentence_picture[3][z]
                    stc_picture[tmp] = get_sentence_probability(tmp)

    #출현 확률이 높은 문장순으로 출현해야 하므로 정렬
    sorted_stc_rice =sorted(stc_rice.items(), reverse=True, key= lambda item : item[1])
    sorted_stc_picture = sorted(stc_picture.items(), reverse=True, key= lambda item : item[1])
    
    #문장 출력
    for stc in sorted_stc_rice:
        print(stc[0], stc[1])
    print('---------------------------------------------------------------')
    for stc in sorted_stc_picture:
        print(stc[0], stc[1])
    print(time.time()-start)