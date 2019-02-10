import folium
import geopy

lct = geopy.geocoders.Bing("AvX_yIinedyCGOKi-qr4Ly6kSNfXVf08N2LjqQ3rvo9xq7PijJcM7Zr_6-nztXLI")


def add_point(mapa, loki, name):
    mapa.add_child(folium.CircleMarker(location = loki, radius = 3, popup = name, fill_color='yellow', color='yellow', fill_opacity= 1))


def read_file(file):
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
            if counter > 1000:
                break

    meanings = list(zip(lst_of_names,lst_of_places))
    iter_dict = list(zip(lst_of_years,meanings))
    main_dict = to_edge_dict(iter_dict)
    return main_dict
    

def to_edge_dict(edge_list):
    """ 
    """
    d = {}
    for i,j in edge_list:
        try:
            d[i].append(j)
        except KeyError:
            d[i] = [j]
    return d


def get_films_info(year):
    """
    """
    str_year = str(year)
    dict_of_films = read_file("locations.csv")
    nice_lst = []
    for tup in dict_of_films[str_year]:
        try:
            buffer = []
            buffer.append(tup[0])
            print(tup[1])
            buffer.extend([get_location(tup[1])])
            nice_lst.extend([buffer])
        except:
            pass
    return nice_lst


def get_location(adress):
    location_1 = lct.geocode(adress)
    return [location_1.latitude, location_1.longitude]




mapa = folium.Map(tiles="cartodbdark_matter")
films_list = get_films_info(input("Give me a year: "))
marker_films = folium.FeatureGroup(name="Mark Films")

for lst in films_list:
    try:
        add_point(marker_films, lst[1], lst[0])
    except:
        pass


mapa.add_child(marker_films)
mapa.add_child(folium.LayerControl())
mapa.save('Karta.html')



















    
