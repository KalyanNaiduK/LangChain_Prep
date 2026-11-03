from response_format.Country import NamePredictionResults

name_map={}

def Classifier(NamePrediction:NamePredictionResults):
    for prediction in NamePrediction.predictions:
        name = prediction.name
        possible_countries = prediction.country
        top_country = prediction.top_country

        if top_country.country_id.lower() in name_map:
            name_map[top_country.country_id.lower()].append({name: possible_countries})
        else:
            name_map[top_country.country_id.lower()] = [{name: possible_countries}]
        
        
def get_name_map():
    for country, names in name_map.items():
        print(f"Country: {country}")
        for name_info in names:
            for name, countries in name_info.items():
                print(f"  Name: {name}")
                for country in countries:
                    print(f"    Country ID: {country.country_id}, Probability: {country.probability}")