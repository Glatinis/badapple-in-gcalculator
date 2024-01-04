from selenium.webdriver import Chrome
from PIL import Image
import numpy as np
import time
import cv2

## INIT ##
driver = Chrome()
# URL = "https://www.google.com"
URL = "https://www.google.com/search?q=calculator"
newCols = 4
newRows = 9

driver.get(URL)
driver.maximize_window()

def setStyle(element, style):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, style)

def setColor(x, y, color, cells):
    setStyle(cells[y][x], f"background-color: {color}")

def duplicate(element):
    driver.execute_script("arguments[0].after(arguments[0].cloneNode(true));", element)
    

driver.find_element_by_xpath('//*[@id="Rzn5id"]/div/a[2]').click()

time.sleep(1)

tbody1 = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody')
tbody2 = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[2]/tbody')
trs1 = tbody1.find_elements_by_tag_name("tr")
trs2 = tbody2.find_elements_by_tag_name("tr")

for i in range(newRows):
    duplicate(trs1[-1])
    duplicate(trs2[-1])


trs1 = tbody1.find_elements_by_tag_name("tr")
trs2 = tbody2.find_elements_by_tag_name("tr")
finalTrs = []

for tr1, tr2 in zip(trs1, trs2):
    finalTrs.append(tr1)
    finalTrs.append(tr2)

finalDivs = []

# Seperate rad and deg
finalTrs.pop(0)
finalDivs.append(driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[1]/div/div/div[1]'))
finalDivs.append(driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[1]/div/div/div[3]'))
finalDivs.append(driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[2]/div/div'))
driver.execute_script("arguments[0].innerHTML = arguments[1];", driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[1]/div/div/div[1]'), "69")
driver.execute_script("arguments[0].innerHTML = arguments[1];", driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[1]/div/div/div[3]'), "69")
driver.execute_script("arguments[0].innerHTML = arguments[1];", driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[2]/div/div'), "69")

x = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]/td[2]')

for i in range(newCols):
    duplicate(x)

reloadedTr = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[3]/div/table[1]/tbody/tr[1]')
reloadedTds = reloadedTr.find_elements_by_tag_name("td")[2:]

for reloadedTd in reloadedTds:
    div = reloadedTd.find_element_by_tag_name("div").find_element_by_tag_name("div")
    finalDivs.append(div)

for tr in finalTrs:
    for i in range(newCols):
        td = tr.find_elements_by_tag_name("td")[-1]
        duplicate(td)
        
    tds = tr.find_elements_by_tag_name("td")
    
    for td in tds:    
        firstDiv = td.find_element_by_tag_name("div")
        finalDiv = firstDiv.find_element_by_tag_name("div")
        driver.execute_script("arguments[0].innerHTML = arguments[1];", finalDiv, "69")
                
        finalDivs.append(finalDiv)

cells = np.array(finalDivs)
cells = np.reshape(cells, (-1, 7 + newCols * 2))

## Main Code ##
# Button = 85 × 36
# Frame = 480 × 360
# Pixels per = 68.5 × 72

BASE = "frames/"
rows = len(cells)
columns = len(cells[0])
btnWidth = 85
btnHeight = 36
frameWidth = 480
frameHeight = 360

xPer = round(btnWidth / (btnWidth * columns / frameWidth), 1)
yPer = round(btnHeight / (btnHeight * rows / frameHeight), 1)
blackThresh = (xPer * yPer * 256 * 3) / 2

def isBlack(color):
    return color <= blackThresh

start = time.time()

for i in range(6572):
    fStart = time.time()
    path = BASE + "frame" + str(i) + ".jpg"
    img = Image.open(path)
    
    for row in range(rows):
        for col in range(columns):
            box = (col * xPer, 
                    row * yPer, 
                    (col + 1) * xPer, 
                    (row + 1) * yPer)
            
            cropped = img.crop(box)
            
            color = np.sum(np.array(cropped))
            
            if isBlack(color):
                setColor(col, row, "black", cells)
            else:
                setColor(col, row, "white", cells)
    
    cv2.imshow("bad window", np.array(img))
    
    if cv2.waitKey(1) == ord('q'):
        break
        
    lapseTime = time.time() - fStart
    print(lapseTime)
    toWait = max(0.6 - lapseTime, 0)
    time.sleep(toWait)
    
    print(f"Lapse Time: {(time.time() - fStart)}")

print(F"Time taken: {time.time() - start}")
cv2.destroyAllWindows()