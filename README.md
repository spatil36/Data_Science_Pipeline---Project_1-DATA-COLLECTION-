# Social Media Data Science Pipeline (CS 515)

![bu](./bulogo.png)

## Project-1 Implementation
> Investigating The Foremost Factors Determining Artists’ Success

### Group Name
> Chestnut

### Work distribution
### Implementation
- Disha Shetty (dshetty3@binghamton.edu)
- Yashaswi Hasarali (yhasara1@binghamton.edu)
### Documentation
- Om Fale (ofale1@binghamton.edu)


### Introduction

In the ever-evolving landscape of the music industry, our project delves into the intricate dynamics that define an artist's journey in this era of unprecedented change. Leveraging a fusion of social media analysis and data science methodologies, we tap into the expansive realms of Reddit and Spotify. Through Reddit, a diverse online community, we unravel fan discussions, reviews, and opinions, discerning patterns in engagement and sentiment. Simultaneously, we harness Spotify's vast streaming data, offering insights into play counts, follower growth, and playlist placements. Join us on this exploration as we gather real-time music-related data, unveiling the pulse of emerging trends and popular artists within a specified timeframe.

### System Architecture Diagram implemeted for this project

![bu](/ArchitectureDiagram.png)

### Data Sources
- Reddit API, Spotify API

### Pre-requisites

<code>Install Python3</code>
<code>Install MongoDB</code>
<code>Install MongoDB Compass</code>

#### How to Run the code

<h4> Please follow these steps for installation and running the code </h4>


<code> 1. Install faktory client</code>

     pip install faktory

<code> Install faktory server </code>
    
     Download the faktory from - https://github.com/contribsys/faktory/releases
     # DEB distros like Ubuntu
     dpkg -i <filename.deb>
     # RPM distros like CentOS
     yum install <filename.rpm>


<code> 2. Make sure the path inside Procfile changed to your path </code>

    client: <path to fclient.py> fclient.py
    
    worker: <path to fworker.py> fworker.py


<code> 2. Install Mongo db </code>

     pip install pymongo

     sudo apt-get install gnupg curl
     
     echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

     sudo apt-get update

     sudo apt-get install -y mongodb-org

     sudo systemctl start mongod

     sudo systemctl daemon-reload

     sudo systemctl status mongod

     sudo systemctl enable mongod

     sudo systemctl stop mongod

     mongod

<code> To run MongoDB </code>     

     sudo systemctl start mongod

     sudo systemctl stop mongod

     suod mongod
     
<code> If issue: Kill the process ID which is in use for port 27017 </code> 

     ps -ef | grep mongod

     sudo lsof -i :27017

     sudo fuser -k 27017/tcp

else

     sudo rm /tmp/mongodb-27017.sock
    
<code> Start the scheduling for calls every 1hr </code>

     source /home/dshetty3/project-1-implementation-chestnut/socialMediaProject1/bin/activate
     foreman start

<code> To see the faktory process website </code>

     xdg-open http://localhost:7420

<img src="/Faktory.gif" alt="Demo GIF" width="900"/>
     

<code> To call spotify APIs and save into the database </code>

     python3 spotify.py

<code> To see the latest plots </code>

    Please run the file plotting_of_project_1.ipynb


### System requirement

| Name | Requirement |
| ------ | ------ |
| Memory | 8Gb |
| OS | Linux |

#### References 

[1] Reddit API Documentation. https://www.reddit.com/dev/api/

[2] Spotify API Documentation. https://developer.spotify.com/documentation/web-api

[3] Matplotlib Library Documentation https://matplotlib.org/













