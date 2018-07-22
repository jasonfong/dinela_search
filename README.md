# DineLA Enhanced Search

Making a better search engine for DineLA restaurant week in Los Angeles. Restaurant week is great and all... but I really wish their website had more search options!

[See the search app here.](https://atomic-elixir-210308.appspot.com/search)

Additional Search Options:
* Menu items

Possible Future Additions:
* Ratings
* Location distance
* Atmosphere tags

# Technology used

This runs as a web app using Google App Engine and Python.
The restaurant menus were only available as images, so some vision machine learning models were needed to extract the menu items.

Tech used: (basically a lot of Google stuff)
* Google App Engine
* Google Cloud Vision API
* Google Search API
* Google Cloud Storage
* Google Datastore
* Django

# How to use this

You can build your own index and run the search UI with the code here!

You do need to engage in a bit of shenangins to get the listing of restaurants. I didn't want to copy that into this repo, so here is how you can get your own copy:

Get the index page by opening the DineLA listing page in Chrome and pasting this into the console:
copy(document.body.innerHTML);

Create a "data" directory in the root of this project and paste the result of the above command into this file:
`data/index.html`

That will provide the listings data used by this app.
