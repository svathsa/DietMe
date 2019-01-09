from django.shortcuts import render
from .forms import UserInputForm
from .models import UserInput
from django.http import HttpResponseRedirect
import sys
import os




nutrition_fax = {'https://www.epicurious.com/recipes/food/views/roast-sausage-and-fennel-with-orange': [229.21, 104.07000000000001, 131.626], 'https://www.epicurious.com/recipes/food/views/antipasto-pasta-with-sausage-artichoke-hearts-and-sun-dried-tomatoes': [69.28, 89.52250000000001, 76.73325], 'https://www.epicurious.com/recipes/food/views/turkey-posole-51255500': [336.66999999999996, 356.75000000000006, 239.325], 'https://www.epicurious.com/recipes/food/views/cheesy-kale-and-mushroom-strata': [317.375, 307.145, 185.421], 'https://www.epicurious.com/recipes/food/views/pasta-with-sausage-and-arugula': [259.66, 197.13, 156.71300000000002], 'https://www.epicurious.com/recipes/food/views/citrus-shrimp-rice-bowls': [206.44, 158.91, 0.0], 'https://www.epicurious.com/recipes/food/views/chicken-soup-with-charred-cabbage': [558.01, 161.82000000000002, 88.633], 'https://www.epicurious.com/recipes/food/views/coconut-apple-ginger-dal': [299.2925, 69.6525, 27.214000000000002], 'https://www.epicurious.com/recipes/food/views/charred-steak-and-broccolini-with-cheese-sauce': [180.7825, 154.00500000000002, 136.57225000000003], 'https://www.epicurious.com/recipes/food/views/one-dish-baked-chicken-with-tomatoes-and-olives': [632.42, 110.14999999999999, 109.14066666666666], 'https://www.epicurious.com/recipes/food/views/ancho-chile-pork-tenderloin-with-brussels-sprouts-and-squash': [258.17499999999995, 193.235, 365.977], 'https://www.epicurious.com/recipes/food/views/chicken-pot-tot-hotdish': [613.09, 129.44, 76.5625], 'https://www.epicurious.com/recipes/food/views/pasta-with-delicata-squash-and-sage-brown-butter': [9.845, 18.445, 22.596], 'https://www.epicurious.com/recipes/food/views/herbed-chickpeas': [578.08, 112.64, 6.610666666666666], 'https://www.epicurious.com/recipes/food/views/smoky-beans-and-greens-on-toast': [507.37, 315.34000000000003, 103.702], 'https://www.epicurious.com/recipes/food/views/slow-roasted-salmon-with-cherry-tomatoes-and-couscous-395923': [333.2799999999999, 123.80000000000001, 228.6115], 'https://www.epicurious.com/recipes/food/views/simple-one-skillet-chicken-alfredo-pasta': [104.83250000000001, 199.12250000000003, 140.51999999999998], 'https://www.epicurious.com/recipes/food/views/salmon-salad-with-beans-15631': [242.3675, 107.01249999999999, 57.864916666666666], 'https://www.epicurious.com/recipes/food/views/istanbul-style-wet-burger-islak-burger': [393.45750000000004, 232.94, 176.29800000000003], 'https://www.epicurious.com/recipes/food/views/turkey-for-twenty': [997.6399999999999, 273.375, 99.23150000000001], 'https://www.epicurious.com/recipes/food/views/roasted-cauliflower-with-parmesan-panko-crumble': [187.655, 366.445, 223.433], 'https://www.epicurious.com/recipes/food/views/crispy-chicken-and-potatoes-with-cabbage-slaw': [233.8675, 205.42750000000004, 87.962], 'https://www.epicurious.com/recipes/food/views/nextover-chicken-tacos-with-quick-refried-beans': [248.505, 199.3475, 241.35300000000004], 'https://www.epicurious.com/recipes/food/views/shrimp-poached-in-coconut-milk-with-fresh-herbs-yerra-moolee': [365.99500000000006, 183.71, 629.5975000000001], 'https://www.epicurious.com/recipes/food/views/silky-pork-and-cumin-stew': [612.185, 124.44, 74.675], 'https://www.epicurious.com/recipes/food/views/slow-cooked-chicken-stew-with-kale': [684.5699999999999, 421.6450000000001, 210.74666666666667], 'https://www.epicurious.com/recipes/food/views/slow-cooked-halibut-with-garlic-cream-and-fennel': [162.57000000000002, 68.57, 105.09], 'https://www.epicurious.com/recipes/food/views/curried-chickpea-and-lentil-dal': [591.1550000000001, 159.425, 88.89099999999998], 'https://www.epicurious.com/recipes/food/views/warm-spiced-saucy-lamb-stew': [463.445, 199.335, 101.57749999999999], 'https://www.epicurious.com/recipes/food/views/ham-hock-and-white-bean-stew': [338.2799999999999, 268.31499999999994, 145.03799999999998], 'https://www.epicurious.com/recipes/food/views/oxtail-and-red-wine-stew': [282.81750000000005, 204.385, 159.352], 'https://www.epicurious.com/recipes/food/views/roast-fish-with-cannellini-beans-and-green-olives': [317.60499999999996, 95.01499999999999, 117.66999999999999], 'https://www.epicurious.com/recipes/food/views/herby-pasta-with-garlic-and-green-olives': [118.93749999999999, 43.222500000000004, 94.83825], 'https://www.epicurious.com/recipes/food/views/roast-chicken-legs-with-lots-of-garlic': [43.379999999999995, 147.87, 37.474000000000004], 'https://www.epicurious.com/recipes/food/views/baked-pasta-alla-norma': [233.89499999999995, 205.535, 95.69075000000001], 'https://www.epicurious.com/recipes/food/views/butternut-squash-steaks-with-brown-buttersage-sauce': [526.04, 98.25999999999999, 85.73800000000001], 'https://www.epicurious.com/recipes/food/views/oven-polenta-with-roasted-mushrooms-and-thyme': [563.28, 238.15, 107.695], 'https://www.epicurious.com/recipes/food/views/poached-eggs-in-tomato-sauce-with-chickpeas-and-feta-368963': [533.5600000000001, 191.78000000000003, 56.101], 'https://www.epicurious.com/recipes/food/views/vegetarian-three-bean-chili': [375.485, 198.0925, 0.0], 'https://www.epicurious.com/recipes/food/views/pressed-broccoli-rabe-and-mozzarella-sandwiches': [503.855, 80.42250000000001, 69.20724999999999], 'https://www.epicurious.com/recipes/food/views/manchurian-green-beans-with-tofu': [230.3425, 204.08750000000003, 16.1065]}

# Create your views here.
def getinputdata(request):
    if request.method=="POST":
        form = UserInputForm(request.POST)
        if form.is_valid():
            UserInput.objects.all().delete()
            user_input = form.save(commit=False)
            user_input.save()
            prots = user_input.proteins
            carbohydrates = user_input.carbohydrates
            fat = user_input.fat
            user_input_data = [carbohydrates, prots, fat]
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
            return HttpResponseRedirect(res_url)

    else:
        form = UserInputForm()
    return render(request, 'get_data/get_data_form.html', {'form':form})
