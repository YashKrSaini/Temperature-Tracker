from selenium import webdriver # using library selenium 
from selenium.webdriver.common.keys import Keys
import time

def writeDatabase(cityCode):
    file=open('Database/cityCode.bin','wb') # /home/yashkumar/Desktop/Temperature/ : Linux
    for i in cityCode:
        data=i+':'+str(cityCode[i])+','
        #print(data.encode())
        file.write(data.encode())
    file.close()
    return(0)

def readDatabase():
    file=open('Database/cityCode.bin','rb') # /home/yashkumar/Desktop/Temperature/ : Linux
    data=file.read().decode()
    #print(data)
    dataList=data.split(',')
    l=len(dataList)
    cityCode={}
    for i in range(l-1):
        element=dataList[i].split(":")
        cityCode[element[0]]=int(element[1])
    file.close()
        
    return(cityCode)

def fastTemp(browser,code):
    #https://www.accuweather.com/web-api/three-day-redirect?key=191262&target=
    #https://www.accuweather.com/en/in/gulaothi/191262/weather-forecast/191262
    # /html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]
    site="https://www.accuweather.com/en/in/gulaothi/"+str(code)+"/weather-forecast/"+str(code) # gulaothi here doesnt make any impact as it is depend on the code not the city name written in url
    browser.get(site)
    temp_xpath="/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]"
    temp=browser.find_element_by_xpath(temp_xpath).text
    while len(temp)==0:
        #time.sleep(0.1) , because it takes few seconds to load the page completely
        temp=browser.find_element_by_xpath(temp_xpath).text
    #print(temp)
    #temperature=int(str(temp[0])+str(temp[1]))
    return(temp)

def standardTemp(browser,city):
    site="https://www.accuweather.com/en/search-locations?query="+city
    #Opening Website in Browser
    browser.get(site)
    # xpath of First Result of a city
    #firstResult="/html/body/div/div[5]/div[1]/div[1]/div/a[1]"
    firstResult="/html/body/div/div[4]/div[1]/div[1]/div[2]/a[1]" # updated 
    result=browser.find_element_by_xpath(firstResult)
    site=result.get_attribute('href')
    #print(site)
    rawCode=str(site.split('/')[-1])
    if len(rawCode)==6:
        pass
    else:
        #print(code[-14:-8])
        code=int(rawCode[-14:-8])
    result.click()
    #time.sleep(1)
    # xpath and other location of city tempertaure
    temp_xpath="/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]"
    temp=browser.find_element_by_xpath(temp_xpath).text
    while len(temp)==0:
        temp=browser.find_element_by_xpath(temp_xpath).text
    #temperature=int(str(temp[0])+str(temp[1]))
    return(temp,code)
    #print(city+", Temperature is "+temperature+" degree Celcius.")

def main():
    iTime=time.time()
    cityList=[]
    n=int(input("How many cities temperature you want to find :"))
    for i in range(n):
        cityName=str(input()) # change 09/09/2021 : raw_input
        cityList.append(cityName)
    print('Wait ! It will take few Minutes')
    cityCode=readDatabase()
    browser=webdriver.Firefox()
    for j in range(n):
        try:
            cityName=cityList[j]
            try:
                code=cityCode[cityName]
                temp=fastTemp(browser,code)#left
            except KeyError:
                temp,code=standardTemp(browser,cityName)#return temp and code
                cityCode[cityName]=code
            print(cityName+' :'+temp)
        except:
            print('Error! City not found, '+cityName)
    writeDatabase(cityCode)
    browser.close()
    fTime=time.time()
    print('Time taken -->',fTime-iTime)

main()
