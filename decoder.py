import json
from flask import make_response

class Decode :
    def __init__(self) :
        # 제조국가
        self.country = {
            "1": "USA",
            "2": "North America",
            "3": "North America",
            "4": "North America",
            "5": "North America",
            "6": "Oceania",
            "7": "Oceania",
            "8": "South America",
            "9": "South America",
            "0": "South America",
            "A": "Africa",
            "B": "Africa",
            "C": "Africa",
            "D": "Africa",
            "E": "Africa",
            "F": "Africa",
            "G": "Africa",
            "H": "Africa",
            "J": "Japan",
            "K": "Korea",
            "L": "Asia",
            "M": "India",
            "N": "Asia",
            "O": "Asia",
            "P": "Asia",
            "Q": "Asia",
            "R": "Asia",
            "S": "UK",
            "T": "Europe",
            "U": "Europe",
            "V": "Europe",
            "W": "Germany",
            "X": "Europe",
            "Y": "Europe",
            "Z": "Italy"   
        }
        
        # 제조사
        self.manufacturer = {
            "V": "Volkswagen",
            "A": "Audi",
            "B": "BMW", 
            "D": "Mercedes, Benz",
            "P": "Porsche",
            "M": "Hyundai",
            "L": "Daewoo",
            "N": "Kia",
            "P": "Ssangyoung",
            "R": "Ssangyoung",
            "T": "Toyota"
        }
        
        # 차량구분
        self.division = {
            "H": "Sedan", #승용차
            "J": "Van", #승합차
            "F": "Truck", #화물차
            "C": "Special", #특장차
            "B": "Trailer" #트레일러
        }
        
        #차종
        self.model = {
            "A": "Light", #경차
            "B": "Small & Medium", #중소형차
            "C": "Compact", #소형차
            "D": "Semi-mid-size", #준중형차
            "E": "Mid-size", #중형차
            "F": "Semi-full-size", #준대형차
            "G": "Full-size" #대형차
        }
        
        #세부 차종
        self.model_series = {
            "A": "Cargo", #카고
            "B": "Dump", #덤프,
            "H": "Mixer", #믹서
            "L": "Standard", #기본사양
            "M": "Advanced", #고급사양
            "N": "High-end" #최고급사양
        }
        
        #차체 형상
        self.body_style = {
            "1": "limousine", 
            "2": "Number of doors",
            "3": "Number of doors",
            "4": "Number of doors",
            "5": "Number of doors",
            "6": "Coupe",
            "8": "Wagon",
            "0": "Pickup"
        }
        
        #안전장치
        self.safty_belt = {
            "1": "None",
            "2": "Manual",
            "3": "Auto",
            "4": "Airbag"
        }
        
        #배기량
        self.displacement = {
            "A": "1800cc",
            "B": "2000cc",
            "C": "2500cc"
        }

        #보안코드
        self.security_code = {
            "P": "LHD(Left Hand Drive)", 
            "R": "RHD(Right Hand Drive)", 
            "0": "America",
            "1": "America",
            "2": "America",
            "3": "America",
            "4": "America",
            "5": "America",
            "6": "America",
            "7": "America",
            "8": "America",
            "9": "America"
        }

        #생산년도
        self.year = {
            "A": "2010",
            "B": "2011",
            "C": "2012",
            "D": "2013",
            "E": "2014",
            "F": "2015",
            "G": "2016",
            "H": "2017",
            "J": "2018",
            "K": "2019",
            "L": "2020",
        }

        #생산공장
        self.plant = {
            "A": "Asan, Korea",
            "C": "Jeonju, Korea",
            "U": "Ulsan, Korea",
            "M": "India",
            "Z": "Turkey"
        }
        
    def decoder(self, info) :
        info = info.upper()

        try :
            country = self.country[info[0]]
            manufacturer = self.manufacturer[info[1]]
            division = self.division[info[2]]
            model = self.model[info[3]]
            model_series = self.model_series[info[4]]
            body_style = self.body_style[info[5]]
            safty_belt = self.safty_belt[info[6]]
            displacement = self.displacement[info[7]]
            security_code = self.security_code[info[8]]
            year = self.year[info[9]]
            plant = self.plant[info[10]]
            number = info[11:]
            
            result = {
                "제조국": country,
                "제조사": manufacturer,
                "차량구분": division,
                "차종": model,
                "세부차종": model_series,
                "차체형상": body_style,
                "안전장치": safty_belt,
                "배기량": displacement,
                "보안코드": security_code,
                "제작연도": year,
                "생산공장": plant,
                "일련번호": number
            }
                    
            return result
        
        except :
            return f'잘못된 VIN 입력입니다.'