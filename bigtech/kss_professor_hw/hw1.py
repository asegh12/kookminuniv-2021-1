import sys
import os
import operator
import random
import time

start = time.time()
uniCnt = {}
biCnt= {}
LastSylCnt = {}
p = {}

# 입력값 처리
#"test-utf8.txt"의 형태는 get-ngram(2)로 추출된 개행된 2음절 파일 
if len(sys.argv) < 3:
    print("python syl_gen_py.py 3/4/5 test-utf8.txt")
    sys.exit(1)
f = open(sys.argv[2], "r", encoding='UTF8')
lines = f.readlines()
n = int(sys.argv[1])

#unigram, bigram, 마지막 음절 계산 - uniCnt, biCnt, LastSylCnt에 딕셔너리 형태로 저장
#음절 출현빈도 1이상이지 않은 경우는 아예 딕셔너리에 저장되지 않으므로 예외상황 처리 완료
for wlist in lines:
    #unigram count
    if wlist[0] in uniCnt :
        uniCnt[wlist[0]] += 1
    else: 
        uniCnt[wlist[0]] = 1
    #bigram count
    if len(wlist)<2 : continue
    if wlist[0]+wlist[1] in biCnt :
        biCnt[wlist[0]+wlist[1]] += 1
    else:
        biCnt[wlist[0]+wlist[1]] = 1
    #Last syl count
    if wlist[1] in ['!', '.', '?']:
        if wlist[0] in LastSylCnt :
            LastSylCnt[wlist[0]] += 1
        else: 
            LastSylCnt[wlist[0]] = 1

#마지막 음절 빈도 상위 5개 추출 -> LastSyl_n에 저장됨
LastSylCnt_sort = sorted(LastSylCnt.items(), key=operator.itemgetter(1), reverse=True)
LastSyl_n = []
last_cnt = 0
for x in LastSylCnt_sort:
    if last_cnt > 4 : break
    LastSyl_n.append(x[0])
    last_cnt += 1

#입력 n에 따른 unigram 빈도 상위 n개 추출 -> uniCnt_n에 저장됨
uniCnt_sort = sorted(uniCnt.items(), key=operator.itemgetter(1), reverse=True)
uniCnt_n = []
for x in range(0, n+1):
    if uniCnt_sort[x][0] == '_' : continue
    if uniCnt_sort[x][0] == '.' : continue
    uniCnt_n.append(uniCnt_sort[x][0])

#추출된 bigram, unigram 빈도수로 확률값을 저장 -> p에 저장됨
for gram in biCnt:
    if len(gram)<2 : continue
    p[gram] = biCnt.get(gram) / uniCnt.get(gram[0])

#첫음절 생성
choice = random.choice(uniCnt_n)
gen=[choice]

#문장생성 시작
while(True):
    #종료조건 10음절이 생성되고 마지막 음절이 LastSyl_n에 포함되거나 '다'가 생성되면 종료
    if(len(gen) >= 10 and (gen[-1]=='다' or gen[-1] in LastSyl_n)) : break

    #다음음절이 나올 딕셔너리를 생성하고 정렬(정렬하는 이유는 상위빈도 3개를 추출하기위해)
    real_gen = {}
    for key, value in p.items():
        if key[0]==choice : real_gen[key] = value
    real_gen_sort = sorted(real_gen.items(), key=operator.itemgetter(1), reverse=True)

    #다음음절 빈도 3개 추출
    real_gen_sort_n = []
    n_idx = 0
    for key in real_gen_sort:
        if n_idx >= 3 : break
        real_gen_sort_n.append(key[0][1])
        n_idx += 1

    #다음음절 빈도상위 3개중에서 랜덤하게 받고 리스트에 추가, 현재음절을 다음음절으로 바꿈.
    choice_next = random.choice(real_gen_sort_n)
    gen.append(choice_next)
    choice = gen[-1]

for i in gen:
    print(i, end='')
print()

f.close()
print(time.time()-start,"초")