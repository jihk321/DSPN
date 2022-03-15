from pprint import pprint
from tkinter import Y
import pandas as pd

item_type = { 
    "1" : "징크판넬,징크330,징크강판445,다이아몬드평이음,V-45(일반),V-45(A),V-70,지붕,지붕330,V250,V115,부자재",
    "2" : "징크판넬,징크330,징크강판355,징크강판445,다이아몬드평이음,V-45(일반),V-45(A),V-70,지붕,지붕330,V250,V115,부자재",
    "3" : "메탈판넬,메탈용후레싱",#라인메탈패널,메탈용후레싱
    "4" : '노출콘,노출콘후레싱',#노출콘크리트패널,노출콘크리트용 후레싱	
    "5" : '사이딩,다이아몬드평이음,V-45(일반),V-45(A),V-70,지붕,지붕330,V250,V115,부자재',
    "6" : 'V250,V115,부자재', #W-140 사선판 외 일반성형제품및 후레싱	
    "7" : '기와강판,스레트형강판,다이아몬드평이음,지붕개량부자재,부자재,후레싱',
    "8" : '기와강판,스레트형강판,보급징크960,보급징크720,다이아몬드평이음,지붕개량부자재,부자재,후레싱',
    "9" : '벽체,후레싱,부자재',
    "10" : 'V-45(A),V-70,지붕,지붕330,RP1,RP3,V250,V115,V50,OL250,OL330'
}

coil_color = {
    "번호" : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
    31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53],

    "색깔" : ['코르텐블랙','코르텐밤색','헤어진회','헤어연회','헤어검정','헤어골드','빅징크','라인메탈 1.0*0.5','헤어은회','골드메탈',
'콘크리트','메탈스톤녹색','메탈스톤블루','메탈스톤은회','불소골드','백색엠보','우드엠보','진우드엠보','밤색슁글','스패니쉬','진스패니쉬',
'연스패니쉬','멀티동','우드','링클진회','링클브라운','링클검정','링클동색','진밤빅스톤','검정빅스톤','자주빅스톤','군청빅스톤','청색매트',
'군청매트','검정매트','연밤매트','진밤매트','자주매트','아이보리','포스맥원판','갈바','은회','진청','밤색','자주','녹색','단색진회',
'오렌지','청남','크림화이트','베이지','아연','티타늄실버'],

    "타입" : ['프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트',
'프린트','솔리드','프린트','프린트','프린트','프린트','프린트','프린트','프린트','프린트','스톤','스톤','스톤','스톤','빅스톤','빅스톤','빅스톤',
'빅스톤','매트','매트','매트','매트','매트','매트','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드','솔리드'],

    "제품" : [
item_type['1'],item_type['1'],item_type['2'],item_type['1'],item_type['1'],item_type['1'],item_type['1'], # 1~7번
item_type['3'],item_type['3'],item_type['3'],item_type['4'], # 8~11번
item_type['1'],item_type['1'],item_type['1'],item_type['1'],item_type['5'],item_type['5'],item_type['5'],item_type['10'], #12~19번
item_type['8'],item_type['7'],item_type['7'],item_type['7'],item_type['10'],item_type['1'],item_type['2'],item_type['1'], #20~27
item_type['6'],item_type['7'],item_type['7'],item_type['7'],item_type['7'],item_type['7'],item_type['7'],item_type['8'],item_type['7'],item_type['8'],item_type['7'], #28~38
item_type['9'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'],item_type['10'], #39~49
item_type['9'],item_type['9'],item_type['9'],item_type['10']], #50~53번

    "두께" : ['0.5','0.5','0.5','0.5','0.5','0.4','0.5','0.5','0.5','0.55','0.55','0.5','0.5','0.5','0.5','0.4','0.4','0.4','0.4','0.4','0.45','0.45','0.45','0.4','0.4','0.4','0.4','0.4',
    '0.45','0.45','0.45','0.45','0.45','0.45','0.45','0.45','0.45','0.45','0.35','0.45','0.45','0.4','0.4','0.4','0.4','0.4','0.4','0.4','0.4','0.4','0.4','1.0','0.5']
}
color_data = pd.DataFrame(coil_color,columns=['번호','색깔','타입','제품','두께'])

def search_color(product_name): #제품명으로 검색
    search_color = []
    for i in range(0,53,1) :
        if product_name in color_data['제품'][i] :
            search_color.append(color_data['색깔'][i])
    
    return search_color #찾은 색 리스트를 넘겨줌

def search_width(product_name) : 
    size = color_data[color_data['색깔'] == product_name]['두께'].values
    return size


def doorsize(size_x,size_y):
    x,y = int(size_x),int(size_y)

    # for x,y in 
    회배 = ((x * y)/1000000) 
    마감바 = ((x-200)+ (y-100)+ (y-100)) /1000  
    C트랙 = ((x * 2) + 300)/1000
    가이드바 = (y/1000) 
    양개바 = (y/1000)
    편개바 = (size_y + size_y + size_x)/1000
    d_index = [회배]
    data = {"마감바" : 마감바, "C트랙": C트랙, "가이드바": 가이드바, "양개바" :양개바, "편개바" :편개바}

    df = pd.DataFrame(data,index=[회배], columns={"마감바","C트랙","가이드바","양개바","편개바"})
    # df = pd.DataFrame(data)
    
    print(df.T)
# doorsize(3400,3400)

