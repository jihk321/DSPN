# from asyncio.windows_events import NULL
# from collections import deque
# from msilib.schema import ComboBox
import sys
# from tkinter import OFF
# from typing import Type
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt
from counting import *
from PannelCalc import *
import pandas as pd
from csv import writer
from coils import *
from subplan import *

from_class = uic.loadUiType("dspncalc.ui")[0]
form_second = uic.loadUiType("subplan.ui")[0]

class SubWindow(QDialog,form_second):

    def __init__(self,parent) :
        super(SubWindow, self).__init__(parent)
        self.initUI()
        self.past_x = None
        self.past_y = None
        
        self.present_x = None
        self.present_y = None

    def initUI(self) :
        self.setupUi(self)
        self.show()

    def mouseMoveEvent(self,event):
    # event.x(),y() : 마우스의 절대좌표 값
        self.draw_Line(event.x(),event.y())
        print(str(event.x()),str(event.y()))
        
    # 마우스 릴리즈 이벤트
    def mouseReleaseEvent(self,event):
    	# event.x(),y() : 마우스의 절대좌표 값
        self.draw_Line(event.x(),event.y())
        self.past_x = None
        self.past_y = None

    def draw_Line(self,x,y):
        if self.past_x is None:
            self.past_x = x
            self.past_y = y
        else:
            self.present_x = x
            self.present_y = y

            painter = QtGui.QPainter(self)
            painter.setPen(QColor(0,0,0))
            painter.drawLine(self.past_x,self.past_y,self.present_x,self.present_y)
            painter.end
            # self.screen.setPixmap(QtGui.QPixmap(self.graphicsView))

class MainClass(QMainWindow, from_class):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.mainstart() # 구동시 실행 함수
        self.show()

    def mainstart(self): # 첫 실행시 할 작업들
        self.today()
        self.chagetype()
        self.price()
        
    def chagetype(self):
        self.Color_Sort()
        type = ptype(self.comboBox_pannel.currentText())
        # print(type)
        if type == 0 :
            self.chagecoil(0.35,0.35)  # 벽체 
            self.wall_option.setVisible(True)
            self.doublesize.setVisible(True)
            self.PF.setVisible(False)
            self.PF_2.setVisible(False)
            self.comboBox_metal.setVisible(False)
            self.edit_bottomcoil.setVisible(True)
            self.edit_topcoil.setVisible(True)
            self.edit_product2.setVisible(False)
            self.label_product2.setVisible(False)
            self.checkBox_same.setVisible(False)

        elif type == 1 or type == 2 :
            self.chagecoil(0.37,0.35) # 지붕,외벽
            self.wall_option.setVisible(False)
            self.doublesize.setVisible(True)
            self.PF.setVisible(False)
            self.PF_2.setVisible(False)
            self.comboBox_metal.setVisible(False)
            self.edit_bottomcoil.setVisible(True)
            self.edit_topcoil.setVisible(True)
            self.edit_product2.setVisible(False)
            self.label_product2.setVisible(False)
            self.checkBox_same.setVisible(False)

        elif type == 3 :
            self.chagecoil(0.5,0.35) # 징크,메탈
            self.wall_option.setVisible(False)
            self.doublesize.setVisible(True)
            self.PF.setVisible(False)
            self.PF_2.setVisible(False)
            self.comboBox_metal.setVisible(True)
            self.edit_bottomcoil.setVisible(True)
            self.edit_topcoil.setVisible(True)
            self.edit_product2.setVisible(False)
            self.label_product2.setVisible(False)
            self.checkBox_same.setVisible(False)

            
        elif type == 4 :
            self.chagecoil(0.4,0.35) # 사이딩
            self.wall_option.setVisible(False)
            self.doublesize.setVisible(True)
            self.PF.setVisible(False)
            self.PF_2.setVisible(False)
            self.comboBox_metal.setVisible(False)
            self.edit_bottomcoil.setVisible(True)
            self.edit_topcoil.setVisible(True)
            self.edit_product2.setVisible(False)
            self.label_product2.setVisible(False)
            self.checkBox_same.setVisible(False)

        elif type == 5 : #강판
            self.chagecoil('0.4','')
            self.wall_option.setVisible(False)
            self.doublesize.setVisible(False)
            self.PF.setVisible(True)
            self.PF_2.setVisible(True)
            self.comboBox_metal.setVisible(False)
            self.edit_bottomcoil.setVisible(False)
            self.edit_topcoil.setVisible(True)
            self.edit_product2.setVisible(False)
            self.label_product2.setVisible(False)
            self.checkBox_same.setVisible(False)


        else: 
            self.chagecoil('','') # 부자재 
            self.wall_option.setVisible(False)
            self.doublesize.setVisible(False)
            self.PF.setVisible(False)
            self.PF_2.setVisible(False)
            self.comboBox_metal.setVisible(False)
            self.edit_bottomcoil.setVisible(False)
            self.edit_topcoil.setVisible(False)
            self.edit_product2.setVisible(True)
            self.label_product2.setVisible(True)
            self.checkBox_same.setVisible(True)

        # self.price()
        self.PF.setChecked(False)
        self.colorsort.setChecked(False)
        self.doublesize.setChecked(False)
        

    def Color_Sort(self):
        self.comboBox_Color.clear()
        # type = ptype(self.comboBox_pannel.currentText())
        item_name = self.comboBox_pannel.currentText()
        ccc = search_color(item_name)
        for i in range(len(ccc)) :
            self.comboBox_Color.addItem(ccc[i])

    def today(self):
        a = today()
        self.edit_date.setText(a)
        start_num = 1
        if start_num < 9 : 
            order_num = "파" + a + "0" + str(start_num)    
        else : order_num = "파" + a + str(start_num)

        if os.path.isfile("매출정보.csv"):
            order_csv = pd.read_csv('매출정보.csv', names = ['주문번호','구분','거래처명','주소','연락처','비고'])
            find_num = order_csv.loc[(order_csv['주문번호'] == order_num)]
            if find_num.empty : self.edit_order_num.setText(order_num)
            elif not find_num.empty : 
                for i in range(0,99,1):
                    start_num = start_num +1
                    if start_num < 9 : 
                        order_num = "파" + a + "0" + str(start_num)    
                    else : order_num = "파" + a + str(start_num)
                    find_num = order_csv.loc[(order_csv['주문번호'] == order_num)]
                    if find_num.empty : 
                        self.edit_order_num.setText(order_num)
                        return
        else : 
            df = pd.DataFrame(columns={'주문번호','구분','거래처명','주소','연락처','비고'})
            df.to_csv("매출정보.csv",index= False,encoding= 'utf-8-sig')
            self.today()
            

    def price(self): # 단가 계산하는 함수
        try:
            self.errorcode()
            itemname = self.comboBox_pannel.currentText()#상품 종류
            color = self.comboBox_Color.currentText() # 색깔
            price,price1,price2,price4 = 0,0,0,0 #price 1 거래처 별 단가 차등 price2 양면 05T price4 추가 옵션 
            type = ptype(itemname)
            if type < 5 :
                grade = self.comboBox_grade.currentIndex()#단열제 종류
                size = self.comboBox_size.currentIndex()#T수 
                
                price = pcalc(type,grade,size)          #단가계산
                price3, colortype = coilcolor(color,type)
                #price =  price3   #색상 타입별 단가 추가
                if self.C1.isChecked() : price1 = 0  
                elif self.C2.isChecked() : price1 = 400
                elif self.C3.isChecked() : price1 = 800
                elif self.C4.isChecked() : price1 = 1000

                if self.onecolor.isChecked() or self.onecolor_2.isChecked() : price4 = 200
                if self.onecolor_3.isChecked() or self.onecolor_4.isChecked() : price4 = 400
                # print("거래처 별 단가 추가 값",price1)
                if self.doublesize.isChecked(): # 양면 05T 체크되었는지 확인 
                    if type == 0 or type ==1 : price2 = 5000
                    elif type == 3 : price2 = 2500
                    elif type == 2 :
                        if colortype == "단색" : price2 = 5000
                        elif colortype == "프린트" : price2 = 7000 
                pricetext = f"기본단가 :{price}원, 거래처 추가금 : {price1}원, 양면 05T 추가금 : {price2}원, 코일 색 추가금 : {price3}, 일면 은,백색추가 {price4}"
                self.error.append(str(pricetext))
                # print("기본 단가 : {price}  거래처 별 추가 단가 {price1} : 양면 05T 추가금 : {price2} 코일 색 추가금 {price3}",price,price1,price2,price3)
                price = price + price1 + price2 + price3 + price4 
            if type == 5 : 
                if self.edit_topcoil.text() != "":
                    top = self.edit_topcoil.text()
                    if self.C1.isChecked() : rate = 1  
                    elif self.C2.isChecked() : rate = 2
                    elif self.C3.isChecked() : rate = 3
                    elif self.C4.isChecked() : rate = 4
                    else : rate = 0
                    if self.PF.isChecked() : itemname = itemname + "(PF)"
                    # price,price1,price2,price3 = coilpricecalc(itemname,color,top,rate)
                    price = coilpricecalc(itemname,color,top,0,0,rate)
                    # pricetext = f"상판가격 :{price1} / 색상가격 : {price2} / 기타비용 :{price3} / 총 가격 : {price}"
                    # self.error.append(str(pricetext))
                else: return 
            self.edit_price.setText(str(price))
            if type > 5 : # 부자재, 도어/창호
                self.edit_price.clear()


        except Exception as ex: 
            print(f"price함수에서 {ex}에러 발생")
            self.edit_price.clear()

    def calc(self): # TableWidget에 적기
        if self.errorcode():
            sort = self.comboBox_type.currentText() #구분
            product = self.comboBox_pannel.currentText() #품목
            itemnum = ptype(product)
            items = itemtype(product) #상품구분 
            grade = self.comboBox_grade.currentText() #보드
            size = self.comboBox_size.currentText() #상세품목 
            color = self.comboBox_Color.currentText() #규격
            topmm = self.edit_topcoil.text() #상판
            bomm = self.edit_bottomcoil.text()#하판
            length = self.edit_length.text()#길이
            numbers = self.edit_number.text()#수량 
            product2 = self.edit_product2.text() #품목2
            if product == "메탈판넬": 
                stardard = self.comboBox_metal.currentText()
                length = float(length)
                length = str(hundup(length))
            else : stardard = self.comboBox_stand.currentText()  #규격2
            if product == "벽체" :
                if self.onecolor.isChecked(): color = "한면백색"
                elif self.onecolor_2.isChecked(): color = "한면은회"
                elif self.onecolor_3.isChecked(): color = "양면은회"
                elif self.onecolor_4.isChecked(): color = "양면백색"
            
            etc = self.edit_etc2.text() #비고 
            clientnum = 0 

            if self.C1.isChecked() : clientnum = 1
            elif self.C2.isChecked() : clientnum = 2
            elif self.C3.isChecked() : clientnum = 3
            elif self.C4.isChecked() : clientnum = 4
            price = self.edit_price.text() #가격
            if itemnum < 5 : 
                self.wlog(sort,items,product,size,product2,color,topmm,bomm,grade,stardard,length,numbers,etc,clientnum,price)
                self.edit_length.setFocus()
                self.totallist()
            if itemnum == 5:
                if self.PF.isChecked() : product = product + "(PF)"
                elif self.PF_2.isChecked() : product = product + "(PC)"
                self.wlog(sort,items,"강판",product,product2,color,topmm,bomm,bomm,stardard,length,numbers,etc,clientnum,price)
                self.edit_length.setFocus()
                self.totallist()
            if itemnum > 5 : #부자재 , 도어/창호 
                items = itemtype(product2) #상품구분 
                self.wlog(sort,items,product,"",product2,length,"",'','',stardard,'',numbers,etc,clientnum,price)
                self.edit_product2.setFocus()
                if product2 == "PVC까치발" or product2 == "캐노피삼각대" :
                    self.ggachibolt(sort,clientnum)
                    
            self.edit_length.clear()
            self.edit_number.clear()
            self.edit_product2.clear()            

    def wlog(self,sort,items,product,size,product2,color,topmm,bomm,grade,stardard,length,numbers,etc,clientnum,price): # 로그에 항목 입력
        global logx,logy

        logitems = [sort,items,product,size,product2,color,topmm,bomm,grade,stardard,length,numbers,etc,clientnum,price]
        for i in logitems:
            self.log.setItem(logx,logy,QtWidgets.QTableWidgetItem(str(logitems[logy])))
            logy = logy + 1
        logy = 0
        logx = logx + 1 

        self.log.resizeColumnsToContents()
        self.log.resizeRowsToContents()

    def errorcode(self):
        self.error.clear()
        itemname = self.comboBox_pannel.currentText()
        item_type = ptype(itemname)
        try:
            if item_type <= 5:
                color_now = self.comboBox_Color.currentText()
                top_now = float(self.edit_topcoil.text())
                if color_now == "밤색" : self.edit_topcoil.setText(str(0.4))
                elif color_now == "포스맥원판" or color_now == "갈바" :
                    if top_now < 0.45 :  self.edit_topcoil.setText(str(0.45))
                elif color_now == "티타늄실버" :
                    if top_now < 0.5 : self.edit_topcoil.setText(str(0.5))
                elif color_now == "아연" :
                    if top_now < 1.0 : self.edit_topcoil.setText(str(1.0))

        except Exception as ex: 
            print(f"errorcode함수에서 {ex}에러 발생")
            return True

        if self.edit_client.text() == '' : 
            self.error.append("거래처 미표기")
            return False
        # if self.edit_topcoil.text() == '' : self.error.append("상판 길이 미표기")
        if self.edit_number.text() == '' : 
            self.error.append("수량 없음")
            return False
        if self.error.toPlainText() == '' : 
            return True

    def excel(self):
        # make_item(logx)
        global logx
        order_number = self.edit_order_num.text() # 주문번호
        clientname = self.edit_client.text() # 거래처 명
        wdate = WritingDate() # 작성일wdate
        column_list = ['주문번호','작성일','거래처','구분','상품구분','품목','상세품목','품목2','규격','상판','하판','보드','규격2','길이','수량','비고','등급','판매비용']
        df = pd.DataFrame(columns={'주문번호','작성일','거래처','거래처코드','구분','출고일','상품구분','품목','상세품목','판넬두께','품목2','규격','판넬색상','상판','하판','보드','규격2','구분2','순번','규격3','길이','수량','면적/중량','단위','비고','등급','단가참조(판넬)','단가참조(절곡)','단가참조(기타)','판매비용'})
        for i in range(0,logx,1):
            table = {'주문번호':order_number,'작성일':wdate,'거래처':clientname}
            for k in range(0,15,1):
                a = self.log.item(i,k).text()
                table[column_list[k+3]] = a    
            # aemp.append(aemp_2)
            # dataframe.append({'주문번호':order_number,'작성일':wdate,'거래처':clientname,'구분':table[0],'상품구분':table[1],'품목':table[2],'상세품목':table[3],'품목2':table[4],'규격':table[5],'상판':table[6],'하판':table[7],'보드':table[8],'규격2':table[9],'길이':table[10],'수량':table[11],'비고':table[12],'등급':table[13],'판매단가':table[14]},ignore_index=True)
            df.loc[i] = table    
        df = df[['주문번호','작성일','거래처','거래처코드','구분','출고일','상품구분','품목','상세품목','판넬두께','품목2','규격','판넬색상','상판','하판','보드','규격2','구분2','순번','규격3','길이','수량','면적/중량','단위','비고','등급','단가참조(판넬)','단가참조(절곡)','단가참조(기타)','판매비용']]
        # print(df.columns)
        # df.fillna('') # NAN 데이터 공백으로 처리
        data_info = self.NewOrder()

        # df['거래처코드'] = '=IFERROR(VLOOKUP([@거래처],거래처[[거래처명]:[거래처코드2]],10,FALSE),"코드확인")'
        # df['판넬두께'] = '=IFERROR(LEFT([@상세품목],FIND("T",[@상세품목],1)-1),"-")'
        # df['판넬색상'] = '=IF(OR([@품목]="칼라코일",[@품목]="부자재",[@품목]="도어/창호",[@품목]="철자재"),"",(LEFT([@규격],5)))'
        # df['색상'] = '=IFERROR(IF(OR([@품목]="부자재",[@품목]="칼라코일",[@품목]="도어/창호",[@품목]="철자재"),VLOOKUP([@품목2],CODE!N:O,2,FALSE),VLOOKUP([@품목]&[@상세품목],CODE!AB:AC,2,FALSE)),"-")'
        # df['규격3'] = '=[@품목2]&" "&[@규격]&" "&[@상판]&" "&[@하판]&" "&[@보드]&" "&[@규격2]&" "&[@구분2]' 
        # df['면적/중량'] = '=IFERROR(IF(OR([@품목]="부자재",[@품목]="도어/창호"),"-",[@수량]*[@[길이(mm)]]/1000),"-")'
        # df['단위'] = '=IFERROR(IF(OR([@품목]="부자재",[@품목]="도어/창호"),VLOOKUP([@품목2],CODE!$N:$P,3,FALSE),VLOOKUP([@상세품목],CODE!N:P,3,FALSE)),"-")'
        # df['단가참조(판넬)'] = '=IFERROR(IF([@품목]="강판",ROUNDUP((VLOOKUP([@상판]&VLOOKUP([@상세품목],생산원가!$F:$G,2,FALSE),생산원가!$H:$I,2,FALSE)*생산원가!$B$3)*VLOOKUP([@상세품목]&[@등급],생산원가!$F:$G,2,FALSE),-2)+VLOOKUP([@규격],생산원가!$A:$B,2,FALSE)+VLOOKUP([@상세품목],생산원가!$A:$B,2,FALSE),ROUNDUP((VLOOKUP([@상판]&VLOOKUP([@품목],생산원가!$F:$G,2,FALSE),생산원가!$H:$I,2,FALSE)*생산원가!$B$3+VLOOKUP([@하판]&VLOOKUP([@품목],생산원가!$F:$H,3,FALSE),생산원가!$H:$I,2,FALSE)*생산원가!$B$3+VLOOKUP([@보드],생산원가!$A:$C,3,FALSE)*[@판넬두께]/100+VLOOKUP([@품목],생산원가!$A:$B,2,FALSE))*VLOOKUP([@등급],생산원가!$A:$B,2,FALSE),-2)+VLOOKUP([@규격],생산원가!A:B,2,FALSE)),"-")'
        # df['단가참조(절곡)'] = '=IFERROR(INDEX(후레싱단가9[[대리점]:[소매]],MATCH([@품목2]&[@규격],후레싱단가9[품목]&후레싱단가9[규격],0),[@등급]),"-")'
        # df['단가참조(기타)'] = '=IFERROR(INDEX(단가표[[1 ]:[5 ]],MATCH([@품목2]&[@규격],단가표[품목]&단가표[규격],0),[@등급]),"-")'
        excelling(logx,clientname,df,data_info)  #엑셀화  
        self.error.append("엑셀 저장 완료")   
        # print(aemp[1]) 


    def Option(self):
        if self.doublesize.isChecked() == True : 
            self.chagecoil(0.5,0.5)
            self.price()
        elif self.doublesize.isChecked() == False:
            # self.chagetype()
            self.price()
        if self.onecolor.isChecked() or self.onecolor_2.isChecked() or self.onecolor_3.isChecked() or self.onecolor_4.isChecked(): self.price()
        if self.paper.isChecked() : 
            self.edit_address_2.setText("복합자재 필요")
            self.paper.setChecked(False)
        
    def chagecoil(self,top,bot):
        self.edit_topcoil.setText(str(top))
        self.edit_bottomcoil.setText(str(bot))

    def NewOrder(self): #새로만들기 버튼 이벤트 
        global logx
        write_content = []
        order_number = self.edit_order_num.text() #주문번호
        proudct_type = self.comboBox_type.currentText() #구분
        client_name = self.edit_client.text() #거래처명
        address = self.edit_address.text() #현장주소
        phone_num = self.edit_phone.text() #연락처
        etc = self.edit_address_2.text() #비고
        write_num = [order_number,proudct_type,client_name,address,phone_num,etc]
        for i in range(len(write_num)):
            write_content.append(write_num[i])
        # write_content.append(order_number)
        # write_content.append(client_name)
        print(write_content)
        with open('매출정보.csv','a', encoding= 'utf-8-sig',newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(write_content)
            # f_object.close()
        self.today() # 주문번호 업데이트
        logx = 0 # 초기화 
        self.allclear() #모든 항목 비우기 
        return write_num

    def renaming(self): 
        self.edit_price.clear()
        door_type = ['방화문','창호','행거도어']
        no_length =['PVC까치발','캐노피삼각대']
        item_name = self.edit_product2.text()
        # print(type(item_name))
        # if door_type in list(item_name) :
        #     if self.comboBox_pannel.currentText() == '부자재':
        #         # self.comboBox_pannel.setCurrentText('도어/창호')
        #         print("부자재가 아님")
        item_name = renamebuja(item_name)
        self.edit_product2.setText(item_name)
        # if no_length in item_name : self.edit_number.setFocus() # 갯수로 포커스 
        # else : self.edit_length.setFocus() # 길이로 포커스 

    def samecolor(self): #추천색상(T수) 체크박스
        color = self.comboBox_sort.currentText()
        color = "*"+ color
        self.edit_length.insert(color)
        self.checkBox_same.setChecked(False)

    def eazybuja(self):
        p_name = self.edit_product2.text() # 부자재 이름
        s_name = self.edit_length.text() # 규격 내용
        if p_name == "물끊기" :
            if s_name == '소': self.edit_length.setText("100*50")
            elif s_name == '대' : self.edit_length.setText("150*50")         
        
        self.edit_number.setFocus() # 수량으로 포커스 
    
    def allclear(self):
        self.edit_address.clear()
        self.edit_phone.clear()
        self.edit_address_2.clear()
        self.edit_client.clear()
        self.edit_sales.clear()
        self.log.clear()

    def showplan(self):
        sub = SubWindow(self)
        # sub.show()
        pass
    
    def find_client(self):
        try:
            input_data = self.edit_client.text() # 현재 입력한 텍스트 값 가져오기
            recom = FindingClient(input_data) # 추천 검색어
            completer = QCompleter(recom,self) # self 추가하니까 되네 시발....
            self.edit_client.setCompleter(completer)
            # box = QVBoxLayout()
            # box.addWidget(self.edit_client)
            # self.setLayout(box)
            # self.show()
            # recom = Recommed(input_data)
        except Exception as ex: print(f"find_client함수에서 {ex}에러 발생")

    def find_buja(self):
        try:
            type = ptype(self.comboBox_pannel.currentText())
            if type == 6 :
                self.error.clear()
                input_data = self.edit_product2.text() # 현재 입력한 텍스트 값 가져오기
                color = self.edit_length.text()
                recom = findbuja(input_data,color) # 추천 검색어
                self.error.append(str(recom))
                # completer = QCompleter(recom,self) #
                # self.edit_length.setCompleter(completer)

        except Exception as ex: print(f"find_buja함수에서 {ex}에러 발생")
    
    def totallist(self):
        global logx
        item_index = [2,3,5,6] #품목,상세품목,규격,상판,길이,갯수
        # total = pd.DataFrame(columns=['품목','사이즈','색상','코일(T)','길이','갯수'])
        total = pd.DataFrame(columns=['품목','사이즈','색상','코일(T)','회배'])
        
        item_type = []

        for s in range(0,logx,1) :
            type = ptype(self.log.item(s,2).text())  # 판넬~벽체있는 항목 인덱스 찾기
            if type <= 5 :
                item_type.append(s)

        for i in item_type :
            mt = [] #딕셔너리
            for k in item_index:
                items = self.log.item(i,k).text()
                mt.append(items) 
            length = float(self.log.item(i,10).text())
            number = float(self.log.item(i,11).text())
            meter = (length/1000)*number # 회배 구하기
            mt.append(meter)
            total.loc[i] = mt
        total_group = total.groupby(['품목','사이즈','색상','코일(T)'])  # 같은 항목 그룹화
        total_sum = total_group['회배'].sum() # 같은 항목 회배수 합
        total_df = total_sum.reset_index() # 합계를 데이터프레임화 
        
        total_num = len(total_df.index)
        total_color,total_coil = "",""
        
        self.comboBox_sort.clear()
        for num in range(0,total_num,1) :
            # total_color.append(total_df['색상'][num])
            total_color = str(total_df['색상'][num])
            total_coil = str(total_df['코일(T)'][num])
            if total_coil == "0.35": self.comboBox_sort.addItem(total_color)
            elif total_coil == "0.37" or total_coil == "0.4" : self.comboBox_sort.addItem(total_color+"040")
            elif total_coil == "0.45" : self.comboBox_sort.addItem(total_color+"045")
            elif total_coil == "0.5" : self.comboBox_sort.addItem(total_color+"050")

    
    def ggachibolt(self,sort,clientnum):
        global logx
        bolt,bolt_num,bolt_index = 0,0,0
        for i in range(0,logx,1):
            isbolt = self.log.item(i,4).text()
            if isbolt == "까치발볼트" :
                bolt,bolt_index = 1,i
            elif isbolt == "PVC까치발" or isbolt == "캐노피삼각대" :
                a = self.log.item(i,11).text()
                bolt_num = bolt_num + 2*(int(a))
        if bolt == 0 : # 볼트가 없을때
            print(bolt_num)
            size = "벽체 T수"
            self.wlog(sort,"상품","부자재","","까치발볼트",size,"","","","","",bolt_num,"너트.와샤포함",clientnum,"")
        elif bolt == 1: #볼트가 있을때
            self.log.setItem(bolt_index,11,QtWidgets.QTableWidgetItem(str(bolt_num)))
    
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = MainClass()
    app.exec_()



