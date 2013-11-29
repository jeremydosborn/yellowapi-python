yellowapi-python
================

Python module for consuming the Yellow Pages "Places" API.

Be sure you read this before getting too far:

http://www.yellowapi.com/branding/

API is accessed in three steps:

1. Create an instance of the YellowAPI class.
2. Call the find_businesses method, and retrieve general business listings.
3. Call the get_business_details method to retrieve specific data fields for each business in #2.

This module usess xml.etree.ElementTree and passes a root object containing the business listings from find_businesses to the get_business_details method. 

The get business_details method then parses the business listings, and returns detailed data for each business in the list.

This module includes the following subset of the API fields available for each business: 

name, street, city, province, postal, phones, logo, url

More fields are available, have a look at http://www.yellowapi.com/docs/places/ for more detail.

Write to jeremy.osborn@gmail.com with questions.

