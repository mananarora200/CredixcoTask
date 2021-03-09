#Importing Libraries
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import speech_recognition as sr
import urllib
import pydub
import sys 

#Sleep function for fluency
def delay ():
    time.sleep(random.randint(2,3))

#Get the ChromeDriver and open website in a new tab
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(os.getcwd()+"\\chromedriver.exe",options=chrome_options) 
delay()
driver.get("https://safebrowsing.google.com/safebrowsing/report_phish/")

#Here we get the url and optional Description from the args
if len(sys.argv)>2:
    url_text = sys.argv[1]
    driver.find_element_by_id("url").send_keys(url_text)
    Description_text = sys.argv[2]
    driver.find_element_by_id("dq").send_keys(Description_text)
elif len(sys.argv)==2:
    url_text = sys.argv[1]
    driver.find_element_by_id("url").send_keys(url_text)
else:
    print("Please Give url and Description (If any)")
    url_text = "https://SampleUrl.com"
    driver.find_element_by_id("url").send_keys(url_text)
    Description_text = "Sample Description"
    driver.find_element_by_id("dq").send_keys(Description_text)

#change iframe and click the recaptcha checkbox
frames=driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()
driver.find_element_by_class_name("recaptcha-checkbox-border").click()

#change iframe for recaptcha and click on the audio captcha button
driver.switch_to.default_content()
frames=driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()
driver.find_element_by_id("recaptcha-audio-button").click()

#Here we again change the iframe for audio Captcha and get the audio file .mp3 and convert into .wav for SpeechRecognition
driver.switch_to.default_content()
frames= driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()
driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
src = driver.find_element_by_id("audio-source").get_attribute("src")
urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav", format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")

#Get the Key (Text) from the audio.wav
r= sr.Recognizer()
with sample_audio as source:
    audio = r.record(source)
key=r.recognize_google(audio)
print(key)
#Entering the text to the capatcha and Submitting the form
driver.find_element_by_id("audio-response").send_keys(key.lower())
driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
driver.switch_to.default_content()
delay()
driver.find_element_by_id("recaptcha-demo-submit").click()
driver.quit()