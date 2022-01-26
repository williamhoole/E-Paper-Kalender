from PIL import Image, ImageDraw, ImageFont
import datetime
from datetime import date
import calendar
import requests
from epd7in5_V2 import EPD
import time
 
class Kalender:

    def __init__(self):
        self.width = 480
        self.hight = 800
        self.img = Image.new("RGB",(self.width,self.hight), (255,255,255))
        self.curdate = date.today() 
        self.date = int(self.curdate.strftime('%d'))
        self.month = int(self.curdate.strftime('%m'))
        self.year = int(self.curdate.strftime('%y'))
        self.boarder= 5
        
    
    def DrawKalender(self):
 
        draw = ImageDraw.Draw(self.img)
        boarder = self.boarder
        h_start= int(self.hight/2)
        h_end = int(self.hight-boarder)
        w_start = self.boarder
        w_end = self.width-self.boarder
        stepsizeV = int((self.width-2*boarder)/7)
        stepsizeH = int((h_start-boarder)/6)

        fontdays = ImageFont.truetype('arial.ttf',int(stepsizeH/4))
        fontnum = ImageFont.truetype('arial.ttf',int(stepsizeH/2))
        cols =[]
        rows = []
        days = {0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat'}
        i = 0

        for x in range (boarder,self.width,stepsizeV):   
            line = ((x,h_start),(x,h_end-5))
            draw.line(line,fill=1,width=3)
            cols.append(x+stepsizeV/4)
            if i<7:
                draw.text((x+stepsizeV/2-20,h_start-stepsizeV/2),days[i],fill=(0,0,0),font=fontdays)
                i+=1

        for x in range (h_start,self.hight,stepsizeH):
            line = ((w_start,x),(w_end,x))
            draw.line(line,fill=50, width=3)
            rows.append(x+stepsizeH/4)
        
        monthlen = calendar.monthrange(self.year,self.month)
        k= monthlen[0]+1
        i= 1
        j= 0
        r = rows[j]

        while i<= monthlen[1]:
            c =cols[k]
            if i == self.date:
                draw.rectangle((c,r,c+fontnum.size+5,r+fontnum.size+5),fill = (0,0,0))
                draw.text((c,r),str(i),fill=(255,255,255),font=fontnum)
            else:
                draw.text((c,r), str(i), fill=(0,0,0),font=fontnum)
            i+=1
            k = (k+1)%7
            if not k:
                j+=1
                r = rows[j]
        #self.img.show()

    def DrawHeader(self):
        
        draw = ImageDraw.Draw(self.img)
        days= {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}
        months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        fontdate = ImageFont.truetype('arial.ttf',60)
        fontmonth = ImageFont.truetype('arial.ttf',50)
        day = int(datetime.datetime.today().strftime('%w'))
        month =int(datetime.datetime.today().strftime('%m'))

        draw.text((45,10),f'{str(days[day])} {self.date}',fill=(0,0,0),font=fontdate)
        draw.text((45,85),f'{str(months[month])} 20{self.year}',fill=(0,0,0),font=fontmonth)
        #self.img.show()
        
class Weather:
    def __init__(self):
        self.api_key = "Insert API Key from Open Weathermap"
        self.stadt = "Enter City name"
        self.long = "10.09" # longitude from city
        self.lat ="48.83" # Latitude from city
        self.url = f'https://api.openweathermap.org/data/2.5/onecall?lat={self.lat}&lon={self.long}&exclude=minutely,hourly&appid={self.api_key}&units=metric'
        self.data = requests.get(self.url).json()
        self.img = Image.new("RGB",(480,200), (255,255,255))
        self.fontw = ImageFont.truetype('arial.ttf',20)
        self.fontn = ImageFont.truetype('arial.ttf',30)
    
    def DrawWeatherIcons(self):

        icon0ID = self.data ['current']['weather'][0]['icon']
        icon1ID = self.data ['daily'][0]['weather'][0]['icon']
        icon2ID = self.data ['daily'][1]['weather'][0]['icon']

        wicon0 = Image.open(f'icon/{icon0ID}.png')
        wicon1 = Image.open(f'icon/{icon1ID}.png')
        wicon2 =Image.open(f'icon/{icon2ID}.png')

        wicon0 = wicon0.resize((100,100),Image.ADAPTIVE)
        wicon1 = wicon1.resize((100,100),Image.ADAPTIVE)
        wicon2 = wicon2.resize((100,100),Image.ADAPTIVE)

        self.img.paste(wicon0,(45,50),)
        self.img.paste(wicon1,(190,50))
        self.img.paste(wicon2,(335,50))

        #self.img.show()

    def DrawTemperature(self):
        draw = ImageDraw.Draw(self.img)
        temp0 = self.data ['current']['temp']
        temp1 = self.data ['daily'][0]['temp']['day']
        temp2 = self.data ['daily'][1]['temp']['day']
        draw.text((65,150),f'{str(int(temp0))}°C',fill=(0,0,0),font=self.fontn)
        draw.text((205,150),f'{str(int(temp1))}°C',fill=(0,0,0),font=self.fontn)
        draw.text((350,150),f'{str(int(temp2))}°C',fill=(0,0,0),font=self.fontn)
        
    def DrawWeatherDay(self):
        draw = ImageDraw.Draw(self.img)
        days= {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday',7: 'Sunday', 8:'Monday'}
        day = int(datetime.datetime.today().strftime('%w'))
        
        draw.text((65,25),f'{str(days[day])}',fill=(0,0,0),font=self.fontw)
        draw.text((205,25),f'{str(days[day+1])}',fill=(0,0,0),font=self.fontw)
        draw.text((350,25),f'{str(days[day+2])}',fill=(0,0,0),font=self.fontw)
        
class EPaper(Weather,Kalender):

    def __init__(self):
        Weather.__init__(self)
        Kalender.__init__(self)
        
    def KalenderDisplay():
       while True:
            epd = EPD()
            epd.init()
            epd.Clear()

            kal= Kalender()
            kal.DrawKalender()
            kal.DrawHeader()
        
            weath = Weather()
            weath.DrawWeatherDay()
            weath.DrawTemperature()
            weath.DrawWeatherIcons()
            kal.img.paste(weath.img,(0,150))
            kal.img.show()
            epd.display(epd.getbuffer(kal.img))
            time.sleep(10800)
        

if __name__ == "__main__":
    EPaper.KalenderDisplay()



