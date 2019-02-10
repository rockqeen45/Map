import folium
import geopy

lct = geopy.geocoders.Bing("AvX_yIinedyCGOKi-qr4Ly6kSNfXVf08N2LjqQ3rvo9xq7PijJcM7Zr_6-nztXLI")


def add_point(mapa, loki, name):
    """
    Add points to the map.
    """
    mapa.add_child(folium.CircleMarker(location = loki, radius = 1, popup = name, fill_color='gold', color='gold', fill_opacity= 1))


def read_file(file):
    """
    (str) ->(dict)
    Return dict of years, names, places with years as keys and list of names, places as values.
    """
    counter = 0
    lst_of_places = []
    lst_of_names = []
    lst_of_years = []
    
    with open(file, "r") as f:
        for line in f.readlines():
            if counter > 0: 
                l = line.rstrip().split(",")
                lst_of_places.append(l[3])
                lst_of_names.append(l[0])
                lst_of_years.append(l[1])
            counter += 1
    meanings = list(zip(lst_of_names,lst_of_places))
    iter_dict = list(zip(lst_of_years,meanings))
    main_dict = to_edge_dict(iter_dict)
    return main_dict
    

def to_edge_dict(edge_list):
    """
    (list) -> (dict)

    Convert pairs from list to dictionary of values.
    
    >>> to_edge_dict([[1, 2], [3, 4], [1, 5], [2, 4]])
    {1: [2, 5], 3: [4], 2: [4]
    """
    d = {}
    for i,j in edge_list:
        try:
            d[i].append(j)
        except KeyError:
            d[i] = [j]
    return d


def get_films_info(year, country):
    """
    Get ingormation about films from the file and add it to the list. Replace adresses with coordinates.
    """
    str_year = str(year)
    dict_of_films = read_file("locations.csv")
    nice_lst = []
    for tup in dict_of_films[str_year]:
        try:
            if country in tup[1]:
                buffer = []
                buffer.append(tup[0])
                buffer.extend([get_location(tup[1])])
                nice_lst.extend([buffer])
            elif country == "else":
                if ("USA" not in tup[1]) and ("Canada" not in tup[1]):
                    buffer = []
                    buffer.append(tup[0])
                    buffer.extend([get_location(tup[1])])
                    nice_lst.extend([buffer])   
        except:
            pass
    return nice_lst


def get_location(adress):
    """
    (str)-> (list)
    
    Get the coordinates in list from the adress
    
    >>> get_location("Ukraine")
    [49.1602935791016, 31.2781219482422]
    """
    location_1 = lct.geocode(adress)
    return [location_1.latitude, location_1.longitude]


def create_points_group(obj, list_of_films):
    """
    Generate points with given objects and lists.
    """
    for lst in list_of_films:
        try:
            add_point(obj, lst[1], lst[0])
        except:
            pass


mapa = folium.Map(tiles="cartodbdark_matter")

year = input("Give me a year: ")
else_films = get_films_info(year, "else")
usa_films = get_films_info(year, "USA")
canada_films = get_films_info(year, "Canada")

else_f = folium.FeatureGroup(name = "Other Films")
usa_f = folium.FeatureGroup(name = "USA Films")
canada_f = folium.FeatureGroup(name = "Canada Films")


create_points_group(else_f, else_films)
create_points_group(usa_f, usa_films)
create_points_group(canada_f, canada_films)


mapa.add_child(else_f)
mapa.add_child(usa_f)
mapa.add_child(canada_f)
mapa.add_child(folium.LayerControl())
mapa.save('Karta.html')



















    
