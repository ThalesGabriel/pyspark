import requests as req
import json

# heat_index_celsius = 0.0


def alternative_flux(t_fahrenheit, local_rh, hi_prev):
    if 80.0 <= t_fahrenheit <= 112.0 and local_rh <= 13.0:
        return hi_prev - (3.25 - 0.25 * local_rh) * (((17.0 - (t_fahrenheit - 95.0)) / 17.0) ** 0.5)
    elif 80.0 <= t_fahrenheit <= 87.0 and local_rh > 85.0:
        return hi_prev + 0.02 * (local_rh - 85.0) * (87.0 - t_fahrenheit)
    else:
        return hi_prev


def hi_prev_recalc(t_fahrenheit, local_rh):
    return -42.379 + 2.04901523 * t_fahrenheit + 10.14333127 * local_rh - 0.22475541 * t_fahrenheit * local_rh - 6.83783 * (
            10.0 ** -3.0) * (t_fahrenheit ** 2.0) - 5.481717 * (10.0 ** -2.0) * (local_rh ** 2.0) + 1.22874 * (
                       10.0 ** -3.0) * (
                   t_fahrenheit ** 2.0) * local_rh + 8.5282 * (10.0 ** -4.0) * t_fahrenheit * (
                       local_rh ** 2.0) - 1.99 * (
                   10.0 ** -6.0) * (t_fahrenheit ** 2.0) * (local_rh ** 2.0)


def celsius_to_fahrenheit(t_celsius):
    return 1.8 * t_celsius + 32.0


def fahrenheit_to_celsius(t_fahrenheit):
    return (t_fahrenheit - 32.0) / 1.8


def heat_index_fahrenheit_alg(t_fahrenheit, local_rh):
    hi_prev = 1.1 * t_fahrenheit - 10.3 + 0.047 * local_rh
    if hi_prev < 80.0:
        return hi_prev
    else:
        hi_prev = hi_prev_recalc(t_fahrenheit, local_rh)
        return alternative_flux(t_fahrenheit, local_rh, hi_prev)


def get_geo_data(latitude, longitude, user):
    return req.get('http://api.geonames.org/findNearByWeatherJSON?lat=' + str(latitude) + '&lng=' + str(
        longitude) + '&username=' + user)

def alert_state(hi_celsius):
    if hi_celsius <=27.0:
        return 'Normal'
    elif 27.1 <= hi_celsius <= 32.0:
        return 'Caution'
    elif 32.1<=hi_celsius<=41.0:
        return 'Extreme Caution'
    elif 41.1<=hi_celsius<=54.0:
        return 'Danger'
    else: return 'Extreme danger'




# heat_index_celsius = fahrenheit_to_celsius(heat_index_fahrenheit_alg(celsius_to_fahrenheit(38), 70))
# print(heat_index_celsius)