DineLA Enhanced Search

Adding more detailed searching for DineLA:
* Menu items
* Ratings
* Location distance
* Atmosphere tags 

Get the index page by opening the DineLA listing page in Chrome and pasting this into the console:
copy(document.body.innerHTML);

Create a "data" directory in the root of this project and paste the result of the above command into this file:
`data/index.html`

That will provide the listings data used by this app.
