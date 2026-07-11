# Phonepe-Pulse-Data-Visualization-and-Exploration

**To check website in My Project**
Link: [phonepe-transaction-insights.streamlit.app](https://phonepe-transaction-insights-uqldsg2o8qxkptzgwlsntu.streamlit.app/)

**Problem Statement**

Retrieve data from the Phonepe Pulse GitHub repository, perform data transformation and cleansing,insert it into a MySQL database, and develop a live geo-visualization dashboard using Streamlit and Plotly in Python.The dashboard will present the data interactively and aesthetically, featuring a minimum of 10 diverse dropdown optionsfor users to select various facts and figures. The solution aims to be secure, efficient, and user-friendly, offering valuable insights and information about the data within the Phonepe Pulse GitHub repository.

**Technology Stack Used:**

1. Python
2. MySQL
3. Streamlit
4. colab
5. Github Cloning
6. Geo Visualisation

**Installation:**

    pip install streamlit pandas plotly scikit-learn numpy

**Import Libraries:**
    
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import numpy as np
    from sklearn.linear_model import LinearRegression
    import os
    import json

**Approach:**

1. Data Extraction: The data is obtained from the PhonePe Pulse GitHub repository using scripting techniques and cloned for further processing [(link)](https://github.com/PhonePe/pulse.git).

2. Data Transformation: Process the cloned data using Python algorithms to transform it into DataFrame format, ensuring it is clean and ready for analysis.

3. Database Integration: The transformed data is inserted into a MySQL database, providing efficient storage and retrieval capabilities.

4. Live Geo Visualization Dashboard: Utilizing Python's Streamlit and Plotly libraries, create an interactive and visually appealing dashboard. This real-time dashboard enables users to explore insights effectively.

5. Database Integration with the Dashboard: Fetch relevant data from the MySQL database and seamlessly integrate it into the dashboard, ensuring that the displayed information is up-to-date and accurate.

6. Visualization: Finally, create a dashboard using Streamlit, incorporating selection and dropdown options. Showcase the output through Geo visualization, bar charts, and a DataFrame table.

**Snapshort**

![image](screenshots/Screenshot%202026-03-25%2021.16.14.png)

Top Chart 

- Transactions

![image](screenshots/Screenshot%202026-03-25%2021.16.56.png)

- User

![image](screenshots/Screenshot%202026-03-25%2021.17.27.png)

Explore Data

- Transactions

![image](screenshots/Screenshot%202026-03-25%2021.18.07.png)

- User

![image](screenshots/Screenshot%202026-03-25%2021.18.07.png)




