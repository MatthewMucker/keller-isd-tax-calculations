# CHANGELOG
# v1 posted 2/6/2025 about 9:15PM

from pyspark.sql import SparkSession 
from pyspark.sql import functions as func

# Start a Spark session
spark = SparkSession.builder.appName("KISD_Property_Taxes").getOrCreate()

# The directory where the source files are found
home_directory = "C:/Users/Matthew/Dropbox/My PC (LAPTOP-OR2SGUNP)/Desktop"

# Read the property data
property_data = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", "|") \
    .csv("file:///" + home_directory + "/PropertyData_2024.txt")

property_data.printSchema()

# Read the location data
location_data = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", "|") \
    .csv("file:///" + home_directory + "/PropertyLocation_2025.txt")

# Because both datasets have a 'City' column, rename one of them to disambiguate
location_data = location_data.withColumn('LocationCity', func.trim(location_data.City))
location_data.printSchema()

# Filter only properties that pay taxes to Keller ISD and join the location data
kisd_properties = property_data.filter(property_data.School == "907").join(location_data, "Account_Num")

# Separate properties into "Keller" and "Non-Keller" properties
keller_properties = kisd_properties.filter(kisd_properties.LocationCity == "KELLER")
non_keller_properties = kisd_properties.filter(kisd_properties.LocationCity != "KELLER")

# Get the total appraised value of all properties. The ratio of appraised value in Keller vs Non-Keller
# should be the same as the ratio of taxes collected in Keller vs Non-Keller
keller_properties_total_value = keller_properties.agg(func.sum("Appraised_Value")).collect()[0][0]
non_keller_properties_total_value = non_keller_properties.agg(func.sum("Appraised_Value")).collect()[0][0]

keller_properties.collect()
non_keller_properties.collect()

# Print some summary information that was useful for debugging
print(f"There are {str(keller_properties.count())} keller properties")
print(f"There are {str(non_keller_properties.count())} non keller properties")

# The interesting stuff
print(f"    Keller value: {str(keller_properties_total_value)}")
print(f"Non Keller value: {str(non_keller_properties_total_value)}")

total_value = keller_properties_total_value + non_keller_properties_total_value
keller_value_percentage = keller_properties_total_value / total_value * 100
non_keller_value_percentage = non_keller_properties_total_value / total_value * 100

print(f"Percentage of Keller ISD taxes from properties in the City of Keller: {str(keller_value_percentage)}")
print(f"Percentage of Keller ISD taxes from properties not in the City of Keller: {str(non_keller_value_percentage)}")