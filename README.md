# MAED
## About
Check out deployed app on - https://maed-d43.eu-de.mybluemix.net/ <br>
MAED is for searching and posting activities - restaurants, entertainment or events. I created MAED using Python (Django), Javascript, HTML, CSS. MAED stores and retrieves data from Cloudant (noSQL database) and images are stored in AWS S3 (Object Storage). Static content is delivered from NGINX server. This Web app is deployed on IBM Cloud Foundry.
## Testing locally
If you clone this app to your local computer it won't work, because environmental variables (connection to Cloudant, AWS and etc.) are not available on github. If you want to test this app, you can test it on https://maed-d43.eu-de.mybluemix.net/ . For testing it locally contact Tadas Baltaduonis through email - tadasbaltaslt@gmail.com
## Instructions
### Searching for activities
If you want to search for activities (restaurants, entertainment, events) you don't need to login or create an account. Just select a type of activity (restaurants, entertainment or events) and then you can browse, filter or search for activity.
### Posting activities
If you want to try to post new activities, create an account as "Organizer", hover your mouse on the top right of your screen where you will see a profile icon and press on "My Activities". Then press on "Post a new activity", fill out the required fields and press submit. Your activity will be posted and you will be able to edit it on "My Activities" page.
