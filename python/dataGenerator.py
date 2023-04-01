import pandas as pd
import numpy as np
import random
import mysql.connector
import os

# Set up database connection
mydb = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"),
    database= os.environ.get("DB_DATA")
)

# Create a dictionary of cities and states
Districts = {
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    "Bangalore": "Karnataka",
    "Chennai": "Tamil Nadu",
    "Hyderabad": "Telangana",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Pune": "Maharashtra",
    "Jaipur": "Rajasthan",
    "Surat": "Gujarat",
    "Lucknow": "Uttar Pradesh",
    "Kanpur": "Uttar Pradesh",
    "Nagpur": "Maharashtra",
    "Patna": "Bihar",
    "Bhopal": "Madhya Pradesh",
    "Ludhiana": "Punjab",
    "Agra": "Uttar Pradesh",
    "Nashik": "Maharashtra",
    "Vadodara": "Gujarat",
    "Rajkot": "Gujarat",
    "Varanasi": "Uttar Pradesh",
    "Srinagar": "Jammu and Kashmir",
    "Aurangabad": "Maharashtra",
    "Dhanbad": "Jharkhand",
    "Amritsar": "Punjab",
    "Navi Mumbai": "Maharashtra",
    "Allahabad": "Uttar Pradesh",
    "Ranchi": "Jharkhand",
    "Haora": "West Bengal",
    "Coimbatore": "Tamil Nadu",
    "Jabalpur": "Madhya Pradesh",
    "Gwalior": "Madhya Pradesh",
    "Vijayawada": "Andhra Pradesh",
    "Jodhpur": "Rajasthan",
    "Madurai": "Tamil Nadu",
    "Raipur": "Chhattisgarh",
    "Kota": "Rajasthan",
    "Guwahati": "Assam",
    "Chandigarh": "Chandigarh",
    "Solapur": "Maharashtra",
    "Hubli": "Karnataka",
    "Dharwad": "Karnataka",
    "Bareilly": "Uttar Pradesh",
    "Moradabad": "Uttar Pradesh",
    "Mysore": "Karnataka",
    "Gurgaon": "Haryana",
    "Aligarh": "Uttar Pradesh",
    "Jalandhar": "Punjab",
    "Tiruchirappalli": "Tamil Nadu",
    "Bhubaneswar": "Odisha",
    "Salem": "Tamil Nadu",
    "Warangal": "Telangana",
    "Mirzapur": "Uttar Pradesh",
    "Guntur": "Andhra Pradesh",
    "Bhiwandi": "Maharashtra",
    "Saharanpur": "Uttar Pradesh",
    "Gorakhpur": "Uttar Pradesh",
    "Bikaner": "Rajasthan",
    "Amravati": "Maharashtra",
    "Indore": "Madhya Pradesh",
"Tirupati": "Andhra Pradesh",
"Tiruppur": "Tamil Nadu",
"Meerut": "Uttar Pradesh",
"Kakinada": "Andhra Pradesh",
"Davangere": "Karnataka",
"Akola": "Maharashtra",
"Kurnool": "Andhra Pradesh",
"Belgaum": "Karnataka",
"Bhatpara": "West Bengal",
"Bally": "West Bengal",
"Ulhasnagar": "Maharashtra",
"Sambhal": "Uttar Pradesh",
"Baranagar": "West Bengal",
"Nadiad": "Gujarat",
"Hapur": "Uttar Pradesh",
"Sikar": "Rajasthan",
"Anantapur": "Andhra Pradesh",
"Ichalkaranji": "Maharashtra",
"Ongole": "Andhra Pradesh",
"Bihar Sharif": "Bihar",
"Shimoga": "Karnataka",
"Kottayam": "Kerala",
"Thanjavur": "Tamil Nadu",
"Bhimavaram": "Andhra Pradesh",
"Karaikudi": "Tamil Nadu",
"Sirsa": "Haryana",
"Etawah": "Uttar Pradesh",
"Deoghar": "Jharkhand",
"Madanapalle": "Andhra Pradesh",
"Yavatmal": "Maharashtra",
"Hajipur": "Bihar",
"Bhind": "Madhya Pradesh",
"Shivpuri": "Madhya Pradesh",
"Chhapra": "Bihar",
"Jharsuguda": "Odisha",
"Ballia": "Uttar Pradesh",
"Puri": "Odisha",
"Karimnagar": "Telangana",
"Kavali": "Andhra Pradesh",
"Ganganagar": "Rajasthan",
"Mahesana": "Gujarat",
"Nabha": "Punjab",
"Palwal": "Haryana",
"Kadapa": "Andhra Pradesh",
"Rajapalayam": "Tamil Nadu",
"Sitapur": "Uttar Pradesh",
"Chilakaluripet": "Andhra Pradesh",
"Vaniyambadi": "Tamil Nadu",
"Chikkamagaluru": "Karnataka",
"Rayachoti": "Andhra Pradesh",
"Palani": "Tamil Nadu",
"Jind": "Haryana",
"Nagaon": "Assam",
"Jhunjhunu": "Rajasthan",
"Villupuram": "Tamil Nadu",
"Machilipatnam": "Andhra Pradesh",
"Ranipet": "Tamil Nadu",
"Udupi": "Karnataka",
"Mandya": "Karnataka",
"Suryapet": "Telangana",
"Malout": "Punjab",
"Baleshwar": "Odisha",
"Amalner": "Maharashtra",
"Roorkee": "Uttarakhand",
"Koratla": "Telangana",
"Sivakasi": "Tamil Nadu"
}

# Create a list of cities and states
districts = list(Districts.keys())
states = list(set(Districts.values()))

# Create a dataframe with dummy data
df = pd.DataFrame(columns=['Latitude', 'Longitude', 'District', 'State', 'Pincode', 'Temperature', 'Humidity', 'Air_Quality'])

for i in range(1000):
    # Generate random values for Latitude and Longitude
    lat = np.random.uniform(8.4, 37.6)
    lon = np.random.uniform(68.7, 97.25)
    
    # Randomly select a city and state from the lists
    district = random.choice(districts)
    state = Districts[district]
    
    # Generate a random Pincode
    pincode = random.randint(100000, 999999)
    
    # Generate random values for Temperature, Humidity, and Air_Quality
    temp = np.random.uniform(20, 40)
    hum = np.random.uniform(30, 80)
    air = np.random.uniform(50, 200)
    
    ranges = round(np.random.random() * 1000) / 1000
    
    # Append the data to the dataframe
    df = df.append({'Latitude': lat, 'Longitude': lon, 'District': district, 'State': state, 'Pincode': pincode, 'Temperature': temp, 'Humidity': hum, 'Air_Quality': air, 'Range': ranges}, ignore_index=True)

# Insert the data into the database
mycursor = mydb.cursor()

for index, row in df.iterrows():
    sql = "INSERT INTO record (latitude, longitude, district, state, pincode, temperature, humidity, air_Quality, `range`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (row['Latitude'], row['Longitude'], row['District'], row['State'], row['Pincode'], row['Temperature'], row['Humidity'], row['Air_Quality'], row["Range"])
    mycursor.execute(sql, val)

mydb.commit()


print(mycursor.rowcount, "records inserted.")
