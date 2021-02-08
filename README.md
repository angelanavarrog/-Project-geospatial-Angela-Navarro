# Project Geospatial

![portada](https://github.com/angelanavarrog/-Project-geospatial-Angela-Navarro/blob/main/images/office.jpg)


## Ojective

The goal of this project is to **propose an office location** where some given criteria are met and where the given company **size is 87 employees**.

## Criteria selecction

For this purpose, I have selected from a dataset that contains information about some companies' offices, the one that meets the following filters:

- **Assumption of number of employees of 90:** Currently, a huge number of companies have implanted a work from home policy but, additionally the company expect to increase their employees number in the future, so being continously changing the location would be counterproductive.

- **Selecttion of New York City** as the place to locate the office as it is the USA city with more ***Starbucks***.

From the original given , the **selected criteria** to determine our location are:

- Proximity to ***Starbucks establishments*** near the office. A 11.5% of the employees satisfies with it.
- Availability of ***Vegan restaurants*** . The CEO of the company is satisfied with this election.
- At least one ***basketball stadium*** within 10 km of the office. The maintenance guy is pleased with it.
- ***Place to go party*** located nearby. The 100% of the company's empoyees  appreciates the election.
- Availability of ***shuttle services for travel***. The KAM team members (23% of the company employees) are satisfied for beeing consired on the election.

## Procedure

The selection began by using ***pymongo library***, so we filter the list of offices by name, city and coordinates of all office whose number of employees were 90.

For other relevant information as the ubication of Starbucks locals, vegan restaurants or places to go party, was necessary to resort to the [APIs in Foursquare](https://developer.foursquare.com/)

Finally, all the relevant information has been reflected on maps. For this aim, it has been indispensable the use of ***folium, cartoframe*** or ***geopandas***.


## Conclusion

After selected an unique location in NYC, could we propose our location as the final ubication of the office? Would our selectd criteria be satisfied?

![office proposal location](https://github.com/angelanavarrog/Geospatial-Project-Angela-Navarro/blob/main/images/office%20location.jpg)
