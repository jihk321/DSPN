from collections import Counter
import pandas as pd
import numpy as np

Ptype = ["일반벽체", "지붕", "외벽", "징크판넬", "사이딩판넬"]
Pgrade = ["일반", "난연", "준불연", "비난연", "020EPS", "015EPS"]  ##비난연 : 비난연가등급
Psize = ["50T", "75T", "100T", "125T", "150T", "155T", "175", "180T", "200T", "225T", "260T"]
price, coilprice = 0, 1500  # price : 판넬 가격, coilprice : 코일단가
type_5 = ["V250", "V250(PF)", "V115", "V115(PF)", "OL250", "OL250(PF)", "OL330", "OL330(PF)", "보급징크960", "보급징크960(PF)",
          "보급징크720", "보급징크720(PF)", "리얼징크445", "리얼징크355", "팀버패널", "듀얼징크"]  # 강판

normalwall = {
    "일반": [11000, 11700, 12500, 13200, 13900, 14100, 14700, 14800, 15400, 16100, 17200],
    "난연": [12100, 13400, 14700, 16000, 17300, 17500, 18600, 18800, 19900, 21200, 23000],
    "준불연": [12200, 13600, 14900, 16300, 17600, 17900, 19000, 19300, 20300, 21700, 23600],
    "비난연": [12500, 13900, 15400, 16900, 18300, 18600, 19800, 20300, 21300, 22800, 24300],
    "020EPS": [12500, 13900, 15400, 16900, 18300, 18600, 19800, 20100, 21300, 22800, 24800],
    "015EPS": [11700, 12800, 13900, 15000, 16100, 16400, 17200, 17500, 18300, 19400, 21000]
}
normal = pd.DataFrame(normalwall, index=Psize, columns=Pgrade)

roofwall = {
    "일반": [12500, 13200, 14000, 14700, 15400, 15600, 16200, 16300, 16900, 17600, 18700],
    "난연": [13600, 14900, 16200, 17500, 18800, 19000, 20100, 20300, 21400, 22700, 24500],
    "준불연": [13700, 15100, 16400, 17800, 19100, 19400, 20500, 20800, 21800, 23200, 25100],
    "비난연": [14000, 15400, 16900, 18400, 19800, 20100, 21300, 21800, 22800, 24300, 26300],
    "020EPS": [14000, 15400, 16900, 18400, 19800, 20100, 21300, 21600, 22800, 24300, 26300],
    "015EPS": [13200, 14300, 15400, 16500, 17600, 17900, 18700, 19000, 19800, 20900, 22500]
}
roof = pd.DataFrame(roofwall, index=Psize, columns=Pgrade)

outwall = {
    "일반": [12400, 13100, 13900, 14600, 15300, 15500, 16100, 16200, 16800, 17600, 18600],
    "난연": [13500, 14800, 16100, 17400, 18700, 19000, 20000, 20300, 21300, 22600, 24400],
    "준불연": [13600, 15000, 16300, 17700, 19100, 19300, 20400, 20700, 21800, 23100, 25000],
    "비난연": [13900, 15300, 16800, 18300, 19800, 20100, 21200, 21700, 22700, 24200, 26200],
    "020EPS": [13900, 15300, 16800, 18300, 19800, 20100, 21200, 21500, 22700, 24200, 26200],
    "015EPS": [13100, 14200, 15300, 16400, 17600, 17800, 18700, 18900, 19800, 20900, 22400]
}
out = pd.DataFrame(outwall, index=Psize, columns=Pgrade)

zincwall = {
    "일반": [17600, 18300, 19100, 19800, 20600, 20700, 21300, 21500, 22100, 22800, 23900],
    "난연": [18700, 20000, 21300, 22700, 24000, 24300, 25300, 25600, 26600, 27900, 29800],
    "준불연": [18800, 20200, 21600, 23000, 24300, 24600, 25700, 26000, 27100, 28500, 30400],
    "비난연": [19100, 20600, 22100, 23600, 25100, 25400, 26600, 27300, 28100, 29600, 31700],
    "020EPS": [19100, 20600, 22100, 23600, 25100, 25400, 26600, 26900, 28100, 29600, 31700],
    "015EPS": [18300, 19400, 20600, 21700, 22800, 23000, 23900, 24200, 25100, 26200, 27800]
}
zinc = pd.DataFrame(zincwall, index=Psize, columns=Pgrade)

sidingwall = {
    "일반": [0, 14700, 15400, 16100, 16900, 17000, 17600, 17800, 18400, 19100, 20100],
    "난연": [0, 16400, 17700, 18900, 20200, 20500, 21500, 21800, 22800, 24100, 25900],
    "준불연": [0, 16500, 17900, 19200, 20600, 20900, 21900, 22200, 23300, 24700, 26500],
    "비난연": [0, 16900, 18400, 19800, 21300, 21600, 22800, 23300, 24200, 25700, 27800],
    "020EPS": [0, 16900, 18400, 19800, 21300, 21600, 22800, 23100, 24200, 25700, 27800],
    "015EPS": [0, 15800, 16900, 18000, 19100, 19300, 20200, 20400, 21300, 22400, 23900]
}
siding = pd.DataFrame(sidingwall, index=Psize, columns=Pgrade)

colors = {'코르텐블랙': '프린트', '코르텐밤색': '프린트', '헤어진회': '프린트', '헤어연회': '프린트', '헤어골드': '프린트', '빅징크': '프린트', '헤어은회1.0*0.5': '프린트',
          '헤어은회1.0*1.0': '프린트', '골드메탈': '프린트', '콘크리트': '프린트', '메탈스톤녹색': '프린트', '메탈스톤블루': '프린트', '메탈스톤은회': '프린트', '불소골드': '프린트',
          '백색엠보': '단색', '우드엠보': '프린트', '진우드엠보': '프린트', '밤색슁글': '프린트', '스패니쉬': '프린트', '진스패니쉬': '프린트', '연스패니쉬': '프린트',
          '멀티동': '프린트', '우드': '프린트', '링클진회': '스톤', '링클브라운': '스톤', '링클검정': '스톤', '링클동색': '스톤', '진밤빅스톤': '빅스톤',
          '검정빅스톤': '빅스톤', '자주빅스톤': '빅스톤', '군청빅스톤': '빅스톤', '청색매트': '매트', '군청매트': '매트', '검정매트': '매트', '연밤매트': '매트',
          '진밤매트': '매트', '자주매트': '매트', '아이보리': '단색', '포스맥원판': '단색', '갈바': '단색', '은회': '단색', '진청': '단색', '밤색': '단색',
          '자주': '단색', '녹색': '단색', '단색진회': '단색', '오렌지': '단색', '청남': '단색', '크림화이트': '단색', '베이지': '단색', '아연': '단색',
          '티타늄실버': '단색', '헤어검정': '프린트'}
colors_width = {'코르텐블랙': '1219,607', '코르텐밤색': '1219,607', '헤어진회': '1219,607,518', '헤어연회': '1219,607',
                '헤어골드': '1219,607', '빅징크': '1219', '라인메탈 1.0*0.5': '1150', '헤어은회': '1150', '골드메탈': '1150', '콘크리트': '1150',
                '메탈스톤녹색': '1219', '메탈스톤블루': '1219', '메탈스톤실버': '1219', '불소골드': '1219', '백색엠보': '1219', '우드엠보': '1219',
                '진우드엠보': '1219', '밤색슁글': '1219', '스패니쉬': '914,445', '다크스패니쉬': '914', '밝은스패니쉬': '914', '멀티쿠퍼': '914',
                '우드': '1219,157', '링클진회': '1219', '링클브라운': '1219,518,607,300', '링클검정': '1219,300',
                '링클동색': '1219,157,303', '빅스톤다크브라운': '914', '빅스톤검정': '914,518,607,300', '빅스톤자주': '914,518,607,300',
                '빅스톤다크블루': '914', '블루매트': '914', '다크블루매트': '914', '검정매트': '914,518,607', '브라운매트': '914',
                '진밤매트': '914,518,607', '자주매트': '914', '아이보리': '1040', '포스맥원판': '1219', '갈바': '1219',
                '은회': '1219,1105,157', '진청': '1219,1105', '밤색': '1219,1105', '자주': '1219,1105', '녹색': '1219',
                '단색진회': '1219,1105', '오렌지': '1219,1105', '청남': '1219,1105', '크림화이트': '1040', '베이지': '914,303',
                '아연': '1219,135,173.6', '티타늄실버': '1219'}

def coilwidth(length):
    color = colors_width
    match_color = []
    for key, value in color.items():
        if length in value: match_color.append(key)
    return match_color


# print(coilwidth("1219,607"))
CoilWidth_Value = {
    "상판폭": [1040, 1219, 1070, 1219, 1219, 1219, 1219, 1150, 1150, 1150, 1219, 1219, 1219, 1219, 1219, 1219, 1219, 1219,
            1219, 1219, 1219, 1219, 1219, 914, 607, 518, 1219, 1219, 1219, 1219, 1219, 914, 607],
    "하판폭": [1040, 1040, 1070, 1070, 1070, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040, 1040,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
CoilWidth_index = ['벽체', '지붕', '벽체(내화)', 'V-45(내화)', '지붕(내화)', '징크판넬', '징크330', '메탈판넬', '세라믹판넬', '노출콘', 'V-45(일반)',
                   'V-45(A)', 'V-70', 'RP1', 'RP3', '사이딩', '지붕330', '외벽판넬', 'V250', 'V115', 'OL250', 'OL330', '보급징크960',
                   '보급징크720', '리얼징크445', '리얼징크355', 'V250(PF)', 'V115(PF)', 'OL250(PF)', 'OL330(PF)', '보급징크960(PF)',
                   '보급징크720(PF)', '팀버패널']
CoilWidth_columns = ['상판폭', '하판폭']
CoilWidth = pd.DataFrame(CoilWidth_Value, index=CoilWidth_index, columns=CoilWidth_columns)

# print(CoilWidth['상판폭']['V-45(내화)'])
CoilThick_Value = {
    "두께": ['0.4', '0.5', '0.35', '0.5', '0.5', '0.5', '0.45', '0.45', '0.45', '0.5', '0.4', '0.5', '0.4'],
    "폭": ['1219', '1150', '1040', '1219', '1040', '1070', '1070', '1219', '914', '607', '607', '518', '518'],
    "두께&폭": ['0.41219', '0.51150', '0.351040', '0.51219', '0.51040', '0.51070', '0.451070', '0.451219', '0.45914',
             '0.5607', '0.4607', '0.5518', '0.4518'],
    "단중": ['3.27', '4.52', '2.43', '4.7', '4', '4.17', '3.65', '4.2', '3.14', '2.35', '1.635', '2', '1.625']
}
CoilThick_index = ['0.4', '0.5', '0.35', '0.5', '0.5', '0.5', '0.45', '0.45', '0.45', '0.5', '0.4', '0.5', '0.4']
CoilThick_columns = ['두께', '폭', '두께&폭', '단중']
CoilThick = pd.DataFrame(CoilThick_Value, index=CoilThick_index, columns=CoilThick_columns)

# EtcPrice = {
#     "구분" : ['징크판넬','지붕','메탈판넬','사이딩','벽체','외벽판넬','V250','V115','OL250','OL330','V250(PF)','V115(PF)','OL250(PF)','OL330(PF)','보급징크960','보급징크720','보급징크960(PF)','보급징크720(PF)','리얼징크445','리얼징크355','팀버패널','듀얼징크','V-45(A)'],
#     "비용" : ['850','600','850','850','600','600','','','','','700','900','900','900','300','300','1300','1300','','','300','','600']
# }
EtcPrice = {'징크판넬': '850', '지붕': '600', '메탈판넬': '850', '사이딩': '850', '벽체': '600', '외벽판넬': '600', 'V250': '0',
            'V115': '0', 'OL250': '0', 'OL330': '0', 'V250(PF)': '700', 'V115(PF)': '900', 'OL250(PF)': '900','OL330(PF)':'900',
            '보급징크960': '300', '보급징크720': '300', '보급징크960(PF)': '1300', '보급징크720(PF)': '1300', '리얼징크445': '0',
            '리얼징크355': '0', '팀버패널': '300', '듀얼징크': '0', 'V-45(A)': '600'}
# PriceRate = {'관계사':'1.15','0':'1.177','1':'1.25','2':'1.3','3':'1.35','4':'1.4'}

Board_Price = {'일반': '2400', '난연': '4700', '준불연': '4700', '비난연가등급': '5000', '비난연020': '5000', '비난연015': '3750'}  # 보드 단가


def coilcolor(color, type):  # 판넬
    coil = colors[color]
    price = 0
    if type == 0:
        pass
    elif type == 1:  # 지붕
        if coil == "스톤":
            price = 800
        elif coil == "프린트":
            price = 1500
    elif type == 2:  # 외벽
        if coil == "스톤":
            price = 800
        elif coil == "단색":
            price = 5000  # 양면 05T
        elif coil == "프린트":
            price = 7000  # 양면 05T
    elif type == 3:  # 징크
        if coil == "단색":
            price = -2000
        elif coil == "스톤":
            price = -1000
        # elif coil == "메탈세라믹" : price = 1000
        # elif coil == "불소수지" : price = 1000
    elif type == 4:  # 사이딩
        if coil == "우드엠보": price = 1000
    # print("옵션가 ",coil," :",price)
    return price, coil


def coilcolor2(color):  # 강판
    # wrinkle = ['링클브라운','링클진회','링클검정','링클쿠퍼']
    color_type = colors[color]
    
    if color_type == '단색':
        colorprice = 0
        if color == '백색엠보' : colorprice = 1000
        elif color == '포스맥원판' : colorprice = 100
    elif color_type == '프린트':
        colorprice = 2000
        if color == '밤색슁글' : colorprice = 1500
        elif color == '불소골드' : colorprice = 3600
        # elif color == '우드엠보' or color == '진우드엠보' : colorprice = 2000
    elif color_type == '스톤' :
        colorprice = 1800
        if color == '링클브라운' : colorprice = 1000
    return int(colorprice)


def etcprice(name):
    price = EtcPrice[name]
    return price


def tenup(num):  # 십의 자리에서 무조건 올림하는 함수
    num_1 = num // 100  # 몫 값
    if num % 100 == 0: return num
    else:
        num_2 = num_1 + 1
    num_3 = num_2 * 100
    # print(f"num 값 : {num} / 목값 : {num_1} / 올림 후 값 : {num_2} / 상판 x 판매 요율 : {num_3}")
    return int(num_3)


def hundup(num):  # 백의 자리에서 무조건 올림
    num_1 = num // 1000  # 몫 값
    if num % 100 == 0: return num
    else:
        num_2 = num_1 + 1
    num_3 = num_2 * 1000
    # print(f"num 값 : {num} / 목값 : {num_1} / 올림 후 값 : {num_2} / 상판 x 판매 요율 : {num_3}")
    return int(num_3)


def clientrate(name, clientnum):
    pannel = CoilWidth_index[0:17]
    if name in pannel:
        if clientnum == 0 : rate = 1.177
        elif clientnum == 1 : rate = 1.2
        elif clientnum == 2 : rate = 1.25
        elif clientnum == 3 : rate = 1.28
        elif clientnum == 4 : rate = 1.3
    elif name == '리얼징크445' or name == '리얼징크355':
        if clientnum == 0 : rate = 1.15
        elif clientnum == 1 : rate = 1.2
        elif clientnum == 2 : rate = 1.28
        elif clientnum == 3 : rate = 1.4
        elif clientnum == 4 : rate = 1.55
    elif name == '팀버패널':
        if clientnum == 0 : rate = 1.22
        elif clientnum == 1 : rate = 1.45
        elif clientnum == 2 : rate = 1.7
        elif clientnum == 3 : rate = 1.85
        elif clientnum == 4 : rate = 2
    else:
        if clientnum == 0 : rate = 1.177
        elif clientnum == 1 : rate = 1.25
        elif clientnum == 2 : rate = 1.3
        elif clientnum == 3 : rate = 1.35
        elif clientnum == 4 : rate = 1.4
    return rate


def boardcalc(grade, size):
    g_price = int(Board_Price[grade])
    price = ((g_price) * int(size)) / 100
    return price


def coilpricecalc(name, color, top, bot, board, rate):  # 품목명,색상,상판폭,하판폭,보드단가,판매요율
    global coilprice
    n_type = ptype(name)
    # try:
    if top == 0.37 : top = 0.4  # 0.37은 0.4로 계산
    width_top = CoilWidth['상판폭'][name]  # 상판폭 검색
    width_bot = CoilWidth['하판폭'][name]  # 하판폭 검색
    search_width = CoilThick['폭'] == str(width_top)
    search_width2 = CoilThick['폭'] == str(width_bot)
    search_top = CoilThick['두께'] == str(top)
    search_bot = CoilThick['두께'] == str(bot)
    gravity_top = CoilThick[search_width & search_top]['단중'].values  # 상판 단중값
    gravity_bot = CoilThick[search_width2 & search_bot]['단중'].values  # 하판 단중값
    price_top = float(gravity_top) * (coilprice)  # 상판 가격
    price_etc = int(etcprice(name))  # 기타비용
    price_rate = clientrate(name, rate)  # 판매요율
    price_color = coilcolor2(color)  # 색상 가격
    if n_type < 5:  # 판넬 타입
        price_bot = float(gravity_bot) * (coilprice)  # 하판 가격
        price = (price_top + price_bot + board + price_etc) * price_rate + price_color
        print(f"판매 요율 : {price_rate} /상판가격 :{price_top} / 하판가격 : {price_bot} /보드 비용: {board}/ / 기타비용 :{price_etc} / 색상 값 : {price_color} / 총 가격 : {price}")
    elif n_type == 5:
        price = (price_top *price_rate ) + price_color+price_etc
        print(f"상판가격{price_top} 기타가격{price_etc} 판매요율{price_rate} 색상값{price_color}")
    price = tenup(price)
    return int(price)

def ptype(name):
    Item_Type = 0  # 제품 분류  0 일반벽체, 1 지붕 , 2 외벽, 3 징크, 4 사이딩, 5 강판 , 6 부자재(상품), 7 부자재(제품), 8 도어/창호
    if name == "벽체" : Item_Type = 0
    elif name == "지붕" or name == "지붕330" : Item_Type = 1
    elif name == "RP1" or name == "RP3" or name == "V-45(일반)" or name == "V-45(A)" or name == "V-70" : Item_Type = 2
    elif name == "징크판넬" or name == "징크330" or name == "메탈판넬" : Item_Type = 3
    elif name == "사이딩" : Item_Type = 4
    elif name in type_5 : Item_Type = 5  # 강판
    elif name == "부자재" : Item_Type = 6
    elif name == "도어/창호" : Item_Type = 7
    # print(name,"타입",type)
    return Item_Type

def pricechart(): #단가 계산해서 csv저장
    size = [50,75,100,125,150,155,175,180,200,225,260]
    grade = ['일반','난연','준불연','비난연가등급','비난연020','비난연015']
    df = pd.DataFrame()
    for bb in range(len(grade)) :
        price = []
        for i in range(len(size)) :
            board = boardcalc(grade[bb],size[i])
            pp = coilpricecalc('지붕','헤어진회',0.37,0.35,board,1)
            price.append(pp)
        df.insert(bb,grade[bb],price)
    df.to_csv("1.csv",index= False,encoding= 'utf-8-sig')

# pricechart()

def pcalc(type, grade, size):
    global price
    if type == 0:  # 일반벽체
        grade = Pgrade[grade]
        size = Psize[size]
        price = normal[grade][size]
    elif type == 1:  # 지붕
        grade = Pgrade[grade]
        size = Psize[size]
        price = roof[grade][size]
    elif type == 2:  # 외벽
        grade = Pgrade[grade]
        size = Psize[size]
        price = out[grade][size]
    elif type == 3:  # 징크
        grade = Pgrade[grade]
        size = Psize[size]
        price = zinc[grade][size]
    elif type == 4:  # 사이딩
        grade = Pgrade[grade]
        size = Psize[size]
        price = siding[grade][size]
    # print("기본 단가:", price,", ",end="")
    return price


def itemtype(name):
    itemtype_1 = ["벽체", "지붕", "지붕330", "RP1", "RP3", "V-45(일반)", "V-45(A)", " V-70", "징크판넬", "징크330", "메탈판넬", "사이딩",
                  "V250", "V115", "OL250", "OL330", "강판", "부자재"]  # 제품
    sang = ['실리콘', '일자캡', '볼트', '지붕캡', 'PVC까치발', '까치발볼트', '방화문', '창호', '행거도어', '도어/창호','칼라피스','우레탄폼','돔와샤']
    if name in itemtype_1: item = "제품"
    elif name in sang: item = "상품"
    else : item = "제품"
    return item


def FindingSub():
    buja = ['이형후레싱', '유바', '의자베이스', '까데기유바', '엘바', '슁글용마루', '상부용마루', '하부용마루', '코너카바', '앤드캡', '앤드캡대용', '징크앤드캡', '돌출박공',
            '비돌출박공', '돌출물받이', '비돌출물받이', '조인트', '철크로샤', '물끊기', '2단후레슁', '3단후레슁', '캐노피카바', 'PVC까치발', '지붕캡']
    words = Counter(buja).most_common()
    print(words)


def HangerDoor(name, size, meter, client):
    # type 0 = 편개 1 = 양개 meter = 회배수 size = T수 client = 거래처 타입
    client_rate = {'1': 1.3, '2': 1.4, '3': 1.5, '4': 1.6}  # 1 대리점 2 일반물량 3 업자 4 소매
    price_rate = client_rate[client]
    meter = int(meter)
    door_values = {"50T": [220419.5262, 261489.3108, 35648.36923],
                   "75T": [231319.1938, 275243.9938, 37854.52308],
                   "100T": [259714.0492, 318275.6492, 44705.23077]}
    door_columns = ['50T', '75T', '100T']
    door_index = ['편개도어', '양개도어', '회배']

    door = pd.DataFrame(door_values, index=door_index, columns=door_columns)
    if meter == 4:
        price = (door[size][name]) * price_rate
        price = hundup(price)
        print(price)
    elif meter > 4:
        price_up = door[size]['회배']
        price_up = hundup((meter - 4) * price_up) + ((meter - 4) * 10000)
        price = door[size][name] * price_rate
        total_price = hundup(price) + price_up
        print(total_price)


# HangerDoor("편개도어","50T","10","1")

def renamebuja(names):
    r_name = names
    rename = {'스크류볼트': '볼트', '물홈통': '이형후레싱', '받침대': 'PVC까치발', '까치발' : 'PVC까치발', '까치' : 'PVC까치발','코너커버': '코너카바','코너바':'코너카바', '유도모음집': '유도모임통', '반도': '선홈통반도',
              '물받이': '돌출물받이', '엘바': '아연엘바', '캐노피후레싱' :'캐노피카바','조인트바' :'조인트','이형':'이형후레싱'}
    if names in rename:
        name = rename[names]
        return name
    else:
        return r_name

