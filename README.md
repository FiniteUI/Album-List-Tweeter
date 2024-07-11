# Album-List-Tweeter
This is a small personal project to tweet out new albums as I listen to them.

I try to listen to a new album about once a week. Since 2018, I've kept a list of albums I've listened to in a google sheet, shown below:
![image](https://github.com/FiniteUI/Album-List-Tweeter/assets/33558498/be465ae4-3ee7-41ea-a2dd-14044e9f48bf)

This project utilizes the Google Sheets API to check for new records and post them to twitter:
![image](https://github.com/FiniteUI/Album-List-Tweeter/assets/33558498/db2d364d-7650-4f43-8a4b-b235e19e7165)

The project mainly utilizes the follow python packages:
- GSpread, for interacting with the Google Sheets API: https://github.com/burnash/gspread
- Twikit, for posting to Twitter without having to use the limited and tempermental API: https://github.com/d60/twikit

The project requires the following files to run:
- A .env file in the main directory with the Twitter credentials, sheet key, and a few other variables. An example is included in the repository: [.env.example](.env.example)
- A Google API service account credentials file, named google-api.json. Instructions for generating one can be found here: https://docs.gspread.org/en/latest/oauth2.html

I currently have the project running on Docker on a personal server.
