# Zap Scrapper

This is and old project of mine that I'm no longer using.

It's intended to scrap data from the Zap Imoveis' REST API.

It uses a MongoDB container to store the data into the `data` folder.

## Zap imóveis pipeline

* List states (`get_states_list`)
* List cities and regions in each state (`get_cities_and_regions_list`)
* List each neighborhood in each city/region (`get_neighborhoods_list`)
* Use the search (`get_search_results`) to search for results using only the state (`state`) and neighborhood (`neighborhood`) parameters.
* Search for more detail of each result (`get_real_state_details`) using the results ID's

Using the zap.scrapper classes:

* 1 Start one general with the desired states. He will register all necessary scouting locations and will return.
* 2 Start as many scouts as you want. They will list all the regions within these states and schedule fetching jobs for them.
* 3 Start as many fetchers as yoy want. They will randomly perform all unfinished jobs.
