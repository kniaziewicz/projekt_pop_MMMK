location='29.999,52.2321'

def get_coordinates(self) -> list:

    longitude = location.split(',',1)[0]
    latitude = location.removeprefix(longitude)
    latitude = latitude.strip(',')
    longitude = float(longitude)
    latitude = float(latitude)
    print(longitude)
    print(latitude)
    print(latitude+longitude)
    return [latitude, longitude]

get_coordinates()