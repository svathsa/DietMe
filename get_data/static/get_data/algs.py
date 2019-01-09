from bs4 import BeautifulSoup
import requests
import os.path






#We create an array of the steps involved in the cooking process. Each element in the Array is an array of the words in each step of the url.
def getUrlIngredients(url):
        ings = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        ingredients = soup.find_all(class_="ingredient")
        for step in ingredients:
            words = step.decode_contents()
            words = re.split(',|\s', words)
            ings.append(words)
        return ings

#We create a reference array from the excel sheet
def get_arra_ings_nutrition(df):
    res_arr = []
    for i in df.index:
        string = df['Shrt_Desc'][i]
        arr = re.split(',|\s', string)
        res_arr.append( [arr, df['Carbohydrt_(g)'][i], df['Protein_(g)'][i], df['FA_Sat_(g)'][i]])
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

#we write a function to extract the quantity from a step.
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

#we write a function to find the best matching ingredients string and retuen the output the nutritional array for that ingredient
def getHighestMatchingIngredientsNutrition(df, step):

    arr = polish_step(step)
    referernce_arr = get_arra_ings_nutrition(df)
    highest_score = 0
    highestMatchingNutrition = [0,0,0]
    highestMatchingArray = []
    for ings in referernce_arr:
        score = 0
        for word in ings[0]:
           for wword in arr:
               if wword == word:
                   score+=1
        if score>highest_score:
            highest_score = score
            highestMatchingNutrition = [ings[1], ings[2], ings[3]]

    return highestMatchingNutrition




#We now write a function to get the nutritional value of each recipie
def get_recipie_nutrition(df, url):
    ingredients = getUrlIngredients(url)
    carbs = 0
    prots = 0
    fat = 0
    for step in ingredients:
        quant = get_quant_from_step(step)
        base_nutrition = getHighestMatchingIngredientsNutrition(df, step)
        carbs += quant*base_nutrition[0]
        prots += quant*base_nutrition[1]
        fat += quant*base_nutrition[2]
    recipie_nutrition = [carbs, prots, fat]
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
        e = (nutrition_fax[url][0]-user_input_data[0])**2 + (nutrition_fax[url][1]-user_input_data[1])**2 + (nutrition_fax[url][2]-user_input_data[2])**2
        error[url] = e
    min_error = 99999999
    res_url = ""
    for url in error:
        if error[url] < min_error:
            min_error = error[url]
            res_url = url
    return res_url
