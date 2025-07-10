\# Volleyball Tracker App



This is a simple web app built with Streamlit to track and tally points in a Catholic beach volleyball league.



\## Features



\- Record match results between teams (A, B, C, D)

\- Each game won within a match gives 1 point to the winning team

\- Automatically tally and display total points per team

\- Store and read match data directly from a Google Sheet

\- Persistent backend with Google Sheets as a database

\- Easy to customize and extend



\## Setup



\### Prerequisites



\- Python 3.7 or higher

\- A Google Cloud service account JSON key with access to a Google Sheet

\- Streamlit installed (`pip install streamlit`)

\- Required Python packages: `gspread`, `pandas`



\### Google Sheets Setup



1\. Create a Google Sheet with a tab named `Games`.

2\. Set up columns: Date, Team 1, Team 2, Team 1 Games Won, Team 2 Games Won.

3\. Share the sheet with your Google service account email (found in your JSON key file).



\### Configure Secrets



Create a file `.streamlit/secrets.toml` in your project root and fill it with your Google service account credentials in TOML format, like:



```toml

\[connections.gsheets]

type = "service\_account"

project\_id = "your-project-id"

private\_key\_id = "your-private-key-id"

private\_key = "-----BEGIN PRIVATE KEY-----\\\\nYOUR\_KEY\\\\n-----END PRIVATE KEY-----\\\\n"

client\_email = "your-service-account-email"

client\_id = "your-client-id"

auth\_uri = "https://accounts.google.com/o/oauth2/auth"

token\_uri = "https://oauth2.googleapis.com/token"

auth\_provider\_x509\_cert\_url = "https://www.googleapis.com/oauth2/v1/certs"

client\_x509\_cert\_url = "your-cert-url"



