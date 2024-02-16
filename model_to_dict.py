def convertModelToDict(model_instance):
    model_dict = {
        'name': model_instance.name,
        'url': model_instance.url,
        'ingredients': model_instance.ingredients,
        'image_url': model_instance.image_url,
        'cuisine': model_instance.cuisine,
        'cooking_time': model_instance.cooking_time,
        'directions':model_instance.cooking_directions,
        'nutrition_info' : model_instance.nutrition_info,
        "cooking_notes" : model_instance.cooking_notes
    }
    return model_dict