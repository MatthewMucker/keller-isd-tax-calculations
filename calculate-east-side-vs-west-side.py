from pyspark.sql import SparkSession 
from pyspark.sql import functions as func

# Start a Spark session
spark = SparkSession.builder.appName("KISD_Property_Taxes").getOrCreate()

# The directory where the source files are found
home_directory = "C:/Users/Matthew/Dropbox/My PC (LAPTOP-OR2SGUNP)/Desktop"

east_side_cities = ["SOUTHLAKE", "COLLEYVILLE", "WESTLAKE", "NORTH RICHLAND HILLS", "North Richland Hills", "KELLER"]

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
east_side_properties = kisd_properties.where(func.col("LocationCity").isin (east_side_cities))
west_side_properties = kisd_properties.where(func.col("LocationCity").isin (east_side_cities) == False)

# Get the total appraised value of all properties. The ratio of appraised value in Keller vs Non-Keller
# should be the same as the ratio of taxes collected in Keller vs Non-Keller
east_side_properties_total_value = east_side_properties.agg(func.sum("Appraised_Value")).collect()[0][0]
west_side_properties_total_value = west_side_properties.agg(func.sum("Appraised_Value")).collect()[0][0]

east_side_properties.collect()
west_side_properties.collect()

# Print some summary information that was useful for debugging
print(f"There are {str(east_side_properties.count())} east side properties")
print(f"There are {str(west_side_properties.count())} west side properties")

# The interesting stuff
print(f"East side value: {str(east_side_properties_total_value)}")
print(f"West side value: {str(west_side_properties_total_value)}")

total_value = east_side_properties_total_value + west_side_properties_total_value
east_side_percentage = east_side_properties_total_value / total_value * 100
west_side_percentage = west_side_properties_total_value / total_value * 100

print(f"Percentage of Keller ISD taxes from properties in the east side: {str(east_side_percentage)}")
print(f"Percentage of Keller ISD taxes from properties in the west side: {str(west_side_percentage)}")

