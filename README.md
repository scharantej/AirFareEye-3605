## Flask Application Design
### HTML Files
- **index.html**: The main HTML file that displays the form for flight search and the table of results.

### Routes
- **POST /search**:
  - Accepts a POST request with the flight search criteria (origin, destinations, departure date, return date).
  - Calls an external API to retrieve flight data for each destination, excluding results from "Spring Airlines".
  - Captures the cheapest price for each destination and updates the database with this information.
  - Generates an HTML table with the updated flight data and renders it in the **index.html** page.
- **GET /refresh**:
  - Accepts a GET request to periodically refresh the flight data.
  - Calls an external API to retrieve the latest prices for each destination.
  - Updates the database with the new prices.
  - Updates the HTML table on the **index.html** page with the latest flight prices.