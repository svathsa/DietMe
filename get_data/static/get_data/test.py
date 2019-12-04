import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import re
import socket

from bs4 import BeautifulSoup
import requests
import os.path



df = pd.read_excel('ABBREV.xlsx', sheet_name = 'ABBREV')


#We obtain an array of urls from the urls.py page
urls = []
with open('urls.txt') as f:
    for line in f:
        urls.append(line[:-1])



#We create an array of the steps involved in the cooking process. Each element in the Array is an array of the words in each step of the url.
def getUrlIngredients(url):
        ings = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        ingredients = soup.find_all(class_="ingredient")
        for step in ingredients:
            words = step.decode_contents()
            words = re.split(',|\s|-', words)
            ings.append(words)
        return ings

#We create a reference array from the excel sheet
def get_arra_ings_nutrition(df):
    res_arr = []
    for i in df.index:
        string = df['Shrt_Desc'][i]
        arr = re.split(',|\s|-', string)
        res_arr.append( [arr, df['Carbohydrt_(g)'][i], df['Protein_(g)'][i], df['FA_Sat_(g)'][i], df['Energ_Kcal'][i]])

    return res_arr


#we write a function to process our step
def polish_step(step):
    arr = []
    for word in step:
        word = word.upper()
        if word!='' and word[len(word)-1]=='S':
            word = word[:len(word)-1]
        arr.append(word)

    arra = list(filter(lambda a: a != '', arr))
    return arra

def get_quant_from_step(step):
    quant = 0.0
    for word in step:
        if len(word)==1 and word.isdigit():
            quant = ord(word) - ord('0')
            break
        elif len(word) == 3 and word[0].isdigit() and word[2].isdigit():
            quant = (ord(word[0]) - ord('0')) / (ord(word[2]) - ord('0'))
            break
    return quant

def inarr(word, arr):
    for eachword in arr:
        if word==eachword:
            return True
    return False

def isvalidIngredient(ingredient):
    invalidArr = ["babyfood", "juc", "lo", "cnd", "comm", "human", "past", "sugared", "stabilized", "supp", "frz", "var", "inf", "formula", "shortening", "sprd", "industrial", "usda", "oscar", "cereal", "peel", "frz", "cnd", "juice", "canned", "cured", "powder", "pwdr", "prep", "formulated", "snacks", "bar", "formul", "candie", "frankfurter"]
    for word in ingredient:
        if inarr(word, invalidArr):
            return False
        else:
            return True



#we write a function to find the best matching ingredients string and retuen the output the nutritional array for that ingredient
def getHighestMatchingIngredientsNutrition(df, step):

    arr = polish_step(step)
    referernce_arr = get_arra_ings_nutrition(df)
    highest_score = 0
    len_of_highest_score = 9999999
    highestMatchingNutrition = [0,0,0]
    highestMatchingArray = []
    for ings in referernce_arr:
        score = 0
        if isvalidIngredient(ings[0]):
            for word in ings[0]:
                for wword in arr:
                    if wword == word:
                        score+=1
            if score>highest_score:
                highest_score = score
                len_of_highest_score = len(ings[0])
                highestMatchingNutrition = [ings[1], ings[2], ings[3], ings[4]]
                highestMatchingArray = ings
            elif score == highest_score:
                if len(ings[0]) < len_of_highest_score:
                    len_of_highest_score = len(ings[0])
                    highest_score = score
                    highestMatchingNutrition = [ings[1], ings[2], ings[3], ings[4]]
                    highestMatchingArray = ings

    return highestMatchingArray


def findNum(text):
    for letter in text:
        if letter.isdigit():
            return (ord(letter) - ord("0"))
    return 1
#We now write a function to get the nutritional value of each recipie
def get_recipie_nutrition(df, url):
    ingredients = getUrlIngredients(url)
    carbs = 0
    prots = 0
    fat = 0
    energy = 0
    for step in ingredients:
        base_nutrition = getHighestMatchingIngredientsNutrition(df, step)
        quant = get_quant_from_step(step)
        carbs += quant*base_nutrition[1]
        prots += quant*base_nutrition[2]
        fat += quant*base_nutrition[3]
        energy += quant*base_nutrition[4]
    recipie_nutrition = [carbs, prots, fat, energy]
    return recipie_nutrition

#we collect the nutrition data from all the urls and store it in an Array
def get_nutrition_from_all_urls(df, urls):
    nutrition_fax = {}
    for url in urls:
        nutrition_fax[url] = get_recipie_nutrition(df, url)
    return nutrition_fax

#we write a function to return the url with least error
def get_min_error_url(user_input_data, nutrition_fax):
    error = {}
    for url in nutrition_fax:
        e = ((nutrition_fax[url][0]-user_input_data[0])**2 + (nutrition_fax[url][1]-user_input_data[1])**2 + (nutrition_fax[url][2]-user_input_data[2])**2 + (nutrition_fax[url][3] - user_input_data[3])**2)**0.5
        error[url] = e
    min_error = 99999999
    res_url = ""
    for url in error:
        if error[url] < min_error:
            min_error = error[url]
            res_url = url
    return res_url

print(get_nutrition_from_all_urls(df, urls))
