import requests, smtplib
from datetime import datetime
from haversine import haversine, Unit

# Longitude and latitude of the SF Exploratorium
VIEWING_DISTANCE = 400
MY_LAT = 37.795080
MY_LONG = -122.396430

lat = MY_LAT+5
long = MY_LONG+5

# Retieve longitude and latitute data of ISS
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
iss_data = response.json()

iss_lat = float(iss_data["iss_position"]["latitude"])
iss_long = float(iss_data["iss_position"]["longitude"])

# Using the haversine formula to calculate how far the ISS is away from you
sf_exp = (MY_LAT, MY_LONG)
iss = (iss_lat, iss_long)
test = (lat, long)
distance_from = haversine(sf_exp, iss, unit=Unit.MILES)

print(f"The Iternational Space Station is {round(distance_from, 2)} miles away from the San Francisco Exploratorium")

parameters = {
    "latitude": MY_LAT,
    "longitude": MY_LONG,
    "formatted": 0
}

# Retrieve sunrise and sunset data of SF
response = requests.get("https://api.sunrise-sunset.org/json?", params=parameters)
response.raise_for_status()
sunrise_sunset_data = response.json()
sunrise = int(sunrise_sunset_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(sunrise_sunset_data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

my_email = "enter your email"
my_password = "enter your password"



# If the ISS is close to my current position
# and it is currently dark
# then send me an email to tell me to look up
if int(distance_from) <= VIEWING_DISTANCE:
    print("The International Space Station is near your house")
    if time_now > sunset or time_now < sunrise:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Suject:LOOK UP!!!\n\nLook Up!!! The International Space Station is near your house"
        )
