<h1>
Steps:
</h1>

<h3>
Open Google Cloud Console.
Sign in to Google Cloud Console with your Google account. Select a project

In the upper right corner, select the project you want to associate the new key with or create a new project.
Navigate to creating a service account

In the left menu, go to "IAM & Admin" -> "IAM".
Under "Service accounts", click on "Create Service Account".
Fill in details

Enter a name for your service account.
Click on "Create and Continue".
Choose roles

Here, you can select roles for your service account. It is recommended to start with the "Storage Admin" role to have full access to Cloud Storage objects.
Click on "Continue".
Create a key

On the next screen, click on "Create key".
Choose the key type as "JSON" and click on "Create". A JSON key file will be downloaded automatically to your computer.
Using the key

Download the JSON key file to your computer.
Use this JSON file in your application for authentication and accessing Google Cloud Storage.
</h3>