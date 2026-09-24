Student Details:

Student: Steffi Sequeira
Branch: Information Technology
Year: Third Year
College: Fr. C. Rodrigues Institute of Technology
Academic Year: 2026–27

1. Overview

This project is an AI-assisted Lost & Found Retrieval System developed to simplify the process of reporting, searching, and identifying lost and found items.

Traditional lost and found systems mainly depend on manual searching and verification. Users have to go through multiple reports and compare item descriptions, locations, and images manually. This can be time-consuming and makes it difficult to identify relevant matches quickly.

The proposed system provides a web-based interface where users can report lost or found items by entering details such as item name, description, location, date, reporter name, contact information, and an optional image.

The system also allows users to browse existing lost and found reports, search reports using item names or locations, and find possible matches for a selected lost item.

The project is implemented using Python and Streamlit. The current prototype focuses on the main lost and found workflow including item reporting, report storage, browsing, searching, and possible match identification.

The project is based on the concept presented in the reference paper, which proposes the use of AI-based image similarity, geographical search, perceptual hashing, and secure ownership verification for automated lost and found retrieval.

2. Application Screenshot

Report an Item

<img width="1110" height="802" alt="image" src="https://github.com/user-attachments/assets/f3419a9c-cef6-4c76-9aa8-cb199e68b420" />


The Report an Item page allows users to report either a lost or found item.

The user can enter the item name, description, location, date, reporter name, and contact information. An image of the item can also be uploaded.

The submitted information is stored as a report and can later be viewed while browsing reports or searching for possible matches.

Browse Lost & Found Reports

<img width="787" height="872" alt="image" src="https://github.com/user-attachments/assets/47204dd8-84a3-4cd3-bf54-e9ef49227491" />

The Browse Lost & Found Reports page displays the available lost and found items.

Users can search and filter reports based on item name and location. Each report displays information such as the item description, location, date, image, reporter name, and contact information.

For example, the application contains a Found report for a Brown wallet reported at Dadar station and a Lost report for a Brown leather wallet reported at Dadar.

Find Possible Matches

<img width="1553" height="852" alt="image" src="https://github.com/user-attachments/assets/ed21a153-27b8-466d-9f93-20fea2f40f53" />


The Find Possible Matches page allows the user to select a previously reported lost item.

The selected item details and image are displayed. When the user selects Find Matching Found Reports, the system searches the available found reports and displays possible matches.

The results are arranged according to the estimated similarity between the lost item and available found reports.

The displayed similarity is only an indication of a possible match and does not represent proof of ownership.

3. Tech Stack

Python – Main programming language used for developing the application.

Streamlit – Used to create the interactive web-based interface.

JSON – Used for storing the Lost & Found report information locally.

Image Processing – Used for handling uploaded item images.

Image Matching – Used to compare image information between reports.

Text Matching – Used to compare item names and descriptions.

Location Matching – Used to compare reported locations and improve matching relevance.

GitHub – Used for source code management and project repository hosting.

Visual Studio Code – Used as the development environment.

4. Architecture

The system follows a simple application workflow:

User

↓

Streamlit Web Interface

↓

Report Item / Browse Reports / Find Matches

↓

Report Storage

↓

Search and Matching Process

↓

Image Matching + Text Matching + Location Matching

↓

Possible Match Results

↓

Reporter Information

↓

Contact and Verification

Main components of the architecture:

Streamlit Interface

Provides the user interface for reporting items, browsing reports, and finding possible matches.

Report Item Module

Collects information such as item name, description, location, date, image, reporter name, and contact information.

Report Storage

Stores the submitted Lost & Found reports locally using JSON-based storage.

Browse Reports Module

Retrieves stored reports and allows users to search and filter available Lost & Found records.

Find Matches Module

Takes a selected lost item and searches the available found reports for possible matches.

Image Module

Handles the uploaded item images and supports image-based comparison.

Text Matching Module

Compares item names and descriptions to identify reports containing similar information.

Location Matching Module

Uses the reported location information to improve the relevance of the matching reports.

Match Results

Displays the found reports that are identified as possible matches for the selected lost item.

5. Working

Step 1 – Report an Item

The user opens the Report an Item section and selects whether the item is Lost or Found.

The user enters the item name, description, location, date, reporter name, contact information, and optionally uploads an image.

Step 2 – Store the Report

After submitting the form, the report information is stored in the application's local data.

The stored information can later be accessed by the Browse Reports and Find Possible Matches sections.

Step 3 – Browse Reports

The user opens the Browse Lost & Found Reports section to view the available reports.

The user can search reports using item names or locations and can filter the available Lost and Found records.

Step 4 – Select a Lost Item

The user opens the Find Possible Matches section and selects a previously reported lost item.

The system displays the selected item's name, description, location, date, and image.

Step 5 – Matching Process

The user clicks Find Matching Found Reports.

The system searches the available found reports and compares the information of the selected lost item with the found items.

The matching process considers information such as item name, description, image information, and location.

Step 6 – Display Possible Matches

The system displays the found reports identified as possible matches.

Example:

Lost Item: Brown leather wallet

Description: Brown

Location: Dadar

Date: 2026-09-24

Possible Found Match: Brown wallet

Location: Dadar station

Date: 2026-09-24

Reporter: Riya

Contact: 448545215

Step 7 – Contact and Verification

After a possible match is identified, the reporter information can be used to contact the person who reported the found item.

The ownership of the item can then be verified before the item is returned.

6. Sample Output

The prototype demonstrates a sample matching scenario between a lost wallet and a found wallet.

Lost Item

Item: Brown leather wallet

Description: Brown

Location: Dadar

Date: 2026-09-24

Found Item

Item: Brown wallet

Description: Brown

Location: Dadar station

Date: 2026-09-24

Reporter: Riya

Contact: 448545215

The system identifies the Brown wallet report as a possible match for the Brown leather wallet.

<img width="1553" height="852" alt="image" src="https://github.com/user-attachments/assets/671edbbc-5ef3-4b98-9de7-af86713b3ef4" />


The output demonstrates how the application can help reduce manual searching by presenting potentially relevant found reports to the user.

7. Reference Paper

Title: Automated Lost & Found Retrieval System Using Deep learning and Geospatial Analysis

Authors: Sheela Chinchmalatpure, Vishakha Deshmukh, Vijay Dharade, Samrudhi Deshmukh, Samruddhi Desai, Aditya Gajare

Department: Artificial Intelligence & Data Science

Institution: Vishwakarma Institute of Technology, Pune, Maharashtra, India

Conference: 2026 International Conference on Emerging Smart Computing and Informatics (ESCI)

Location: Pune, India

Conference Dates: March 11–13, 2026

DOI: 10.1109/ESCI68015.2026.11493387

The reference paper proposes an automated Lost & Found Retrieval System that combines AI-based image similarity, perceptual hashing, geographical search, and secure ownership verification.

The major concepts discussed in the paper include CLIP-based image embeddings, perceptual hashing, latitude and longitude based location search, question-based ownership verification, OTP authentication, fraud detection, and administrative analytics.

The paper evaluates the proposed system using a dataset of 52 objects consisting of rings, watches, jewellery, wallets, and mobile phones. The dataset contains 26 lost items and 26 found items.

The reported evaluation results include image similarity accuracy of 55%–75%, average processing time of 0.11 seconds, false match rate of 10%, OTP verification success rate of 96%, and location matching accuracy of 90%.

Relation of the Project with the Reference Paper

The reference paper presents a complete Lost & Found Retrieval System using advanced image similarity, geospatial filtering, and secure ownership verification.

This project implements a simplified prototype based on the same overall Lost & Found retrieval concept.

The current application focuses on reporting items, storing reports, browsing reports, searching reports, and identifying possible matches.

Advanced features described in the reference paper, such as the complete CLIP-based retrieval pipeline, full geographical coordinate processing, OTP authentication, and administrative analytics, can be incorporated as future enhancements.

8. Demo Walkthrough

9. Open the project in Visual Studio Code.

10. Install the required libraries using:

pip install -r requirements.txt

3. Start the Streamlit application using:

python -m streamlit run app.py

4. Open the application in the browser using:

[http://localhost:8501](http://localhost:8501)

5. Open the Report an Item section.

6. Select Lost or Found.

7. Enter the item details and upload an image if required.

8. Submit the report.

9. Open Browse Lost & Found Reports to view the stored reports.

10. Use the search and filtering options to find a particular item or location.

11. Open Find Possible Matches.

12. Select the required lost item.

13. Click Find Matching Found Reports.

14. View the possible matching found reports.

15. Check the item details, location, image, and reporter information for further verification.

Project Repository

GitHub Repository:

[https://github.com/steffisequeira9/Ai-lost-and-found](https://github.com/steffisequeira9/Ai-lost-and-found)



Run the Project

pip install -r requirements.txt

python -m streamlit run app.py

