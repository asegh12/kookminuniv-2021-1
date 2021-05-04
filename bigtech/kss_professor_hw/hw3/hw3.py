import sys
import heapq
import time
import operator

#문장 trigram 벡터를 생성할 때 feature개수(top_n), trigram 상위 n값을 추출하는 리스트이고 리스트의 index가 id(topk)
#topk를 추출하고 벡터의 내적 시, key-value로 빠르게 접근하기 위하여 topk_dic를 만듬
topk_n = 300000
topk = []
topk_dic = {}

#문장 2개를 입력으로 trigram으로 자르고 코사인 유사도 값을 출력하는 함수
def sen_vector(l1, l2):

    #각 문장의 trigram을 담는 함수
    l1_list={}
    l2_list={}
    #유사도 검사 대상 문장 2개를 trigram으로 자르는 코드
    #l1은 -3인 이유는 마지막에 \n 개행 문자가 붙으므로
    for i in range(len(l1)-3):
        if l1[i:i+3] in l1_list :
            l1_list[l1[i:i+3]] += 1
        else : l1_list[l1[i:i+3]] = 1
    for i in range(len(l2)-3):
        if l2[i:i+3] in l2_list :
            l2_list[l2[i:i+3]] += 1
        else : l2_list[l2[i:i+3]] = 1

    a = dict()
    b = dict()
    a_cnt = 0
    b_cnt = 0
    result = 0
    a_norm = 0
    b_norm = 0

    #topk_dic 을 통해 key-value 쌍으로 빠르게 문장에 대한 vector요소가 있는 지를 탐색
    #각 두 문장의 trigram 중에서 topk의 trigram에 포함된다면 그 값은 코사인 유사도에 필요한 값이므로 추출함.
    for i in l1_list.keys():
        if i in topk_dic : 
            a[i] = l1_list[i]
            a_cnt += 1
    for i in l2_list.keys():
        if i in topk_dic : 
            b[i] = l2_list[i]
            b_cnt += 1
    
    #두 문장의 trigram이 벡터에 포함되지 않을 경우.
    if a_cnt==0 or b_cnt==0 : return 0;
    #두 문장 trigram에 대하여 내적
    else :
        for k, v in a.items():
            for k2, v2 in b.items():
                if(k==k2) : result += v*v2
        for v in a.values():
            a_norm += v*v
        for v in b.values():
            b_norm += v*v
        return result/(((a_norm)**0.5)*(b_norm**0.5))

if __name__ == "__main__":
    if len(sys.argv) != 3 : print("usage : python hw3.py utf.txt KCC_Korean_sentences_UTF8.txt"); sys.exit(1)
    f = open(sys.argv[1], 'r', encoding='UTF-8')

    #문장의 index를 입력받는 변수(), 문장을 저장하는 변수,
    sen_idx = int(input('Input the sentence index : '))
    sen_line = ''
    line_dic = {}
    lines = f.readlines()

    for line in lines:
        line_split = line.split()
        if(len(line_split) != 2) : continue
        #trigram 빈도 계산 결과는 ' '(스페이스)가 '_'로 표현되어 있으므로 ' '으로 변경
        line_dic[line_split[1].replace('_', ' ')] = line_split[0]

    #딕셔너리 형태로 받은 line_dic(trigram 빈도 딕셔너리)에서 상위 topk_n개를 추출하여 리스트로 저장
    topk = heapq.nlargest(topk_n, line_dic, key=line_dic.get)
    #7번째 주석을 참조, key-value를 이용하기 위한 단순 참조용
    for i in topk:
        topk_dic[i] = 1

    f = open(sys.argv[2], 'r', encoding='UTF-8')
    lines = f.readlines()

    start = time.time()
    #입력한 index에 대한 문장을 추출하는 코드. sen_line이 인덱스에 대한 문장
    i = 0
    for line in lines:
        if i == sen_idx:
            sen_line = line
            break
        i += 1
    print('Your sentence : %s'%sen_line)

    #max_dic은 유사도 검사시 0보다 큰 문장들을 저장하며 유사도가 가장 높은 2가지 값을 추출할 때 사용
    max_dic ={}
    for line in lines:
        if(line==sen_line) : continue
        re = sen_vector(sen_line, line)
        # 유사도 검사시 0보다 큰 값은 모두 딕셔너리 형태로 저장한다.
        if 0<re : max_dic[line] = re
    #유사도 검사 결과를 정렬한다.
    max_dic_sort = sorted(max_dic.items(), key=operator.itemgetter(1), reverse=True)
    #상위 2개의 값을 출력한다.
    for i in [0,1]:
        print(max_dic_sort[i][0],max_dic_sort[i][1])
    f.close()
    print(time.time()-start)