# Finviz Scarper Consumer Project

- [Finviz Scarper Consumer Project](#finviz-scarper-consumer-project)
  - [The Screener Workflow](#the-screener-workflow)
  - [Installation](#installation)
    - [Locally](#locally)
    - [On AWS Lightsail](#on-aws-lightsail)
  - [Usage](#usage)
  - [n8n Workflows Configuration](#n8n-workflows-configuration)


## The Screener Workflow
* Keep track of scrapped data and avoid duplicates when writing to DB. If a change is introduced, get only the new data and append/modify the DB.
Also, get notified when new data is added.

* Schedules & Steps
  1. Before the beginning of the pre-market hours, clear the DB table.
  2. scrape at the beginning of the pre-market hours. --> Get notified (with the full list)
  3. scrape every 5 min starting from the pre-market hours until end of after-market hours.
    2.1 compare the ticker,
        ```plain
        if exists
            check news_title
            if news_title changes:
                update the whole row --> Get notified (with updated ticker)
        else:
            Append the new row --> Get notified (with appended ticker)
        ```


## Installation

### Locally
* Dependencies are docker, docker-compose (optional) and ngrok.


### On AWS Lightsail

* Create a machine with required dependencies installed. NOTE, create the ssh key pair beforehand.
```bash
aws lightsail create-instances \
    --instance-names screener \
    --bundle-id micro_3_0 \
    --region eu-west-1 \
    --availability-zone eu-west-1a \
    --blueprint-id ubuntu_22_04 \
    --key-pair-name lightsail_ir \
    --user-data '#!/bin/bash

set -x

apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release

sudo apt-get update
sudo apt-get -y install ca-certificates curl gnupg
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

sudo groupadd docker || true
sudo usermod -aG docker ubuntu
echo "Log out and log back in so that your group membership is re-evaluated."

sudo curl -SL "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Install ngrok and authentication for Linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok

# Get your authtoken from https://dashboard.ngrok.com/
# Run the following command to add your authtoken to the default ngrok.yml
NGROK_AUTHTOKEN=""
ngrok config add-authtoken ${NGROK_AUTHTOKEN}

# Set timezone to NY for simpler cron
sudo timedatectl set-timezone America/New_York
' \
--tags key=ENV,value=PROD key=PROJECT,value=SCREENER
```



## Usage

* After spinning up a VPS, pull images
```bash
docker pull nurhun/my-n8n-with-docker:v0.2
docker pull nurhun/my-pyfinviz:v0.4
```

* Create a persistent volume and network, if docker command will be used
```bash
docker volume create n8n_data
# Optional
docker network create my_n8n_network
```

* Run ngrok
```bash
ngrok http 5678

# Or better
nohup ngrok http 5678 > ngrok.log 2>&1 &
```

* scp the n8n docker-compose.yml to the VPS, or create a container with proper ENVs and volumes
```bash
docker run -d \
  --name n8n \
  -u $(id -u):$(getent group docker | cut -d: -f3) \
  --network my_n8n_network \
  -p 5678:5678 \
  -e WEBHOOK_URL=https://<ngrok_subdomain>.ngrok-free.dev \
  -e NEWS_DATE_TODAY=true \
  -v n8n_data:/home/node/.n8n \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /home/ubuntu:/app/workflows \
  --restart unless-stopped \
  nurhun/my-n8n-with-docker:v0.2
```

* Access n8n at `http://<the_ngrok_url>`

* Import the n8n workflows from the `n8n_workflows.json` file.

* Activate the workflow.


## n8n Workflows Configuration

* Since the US stock market has 3 trading sessions as follows
  - Pre-market trading session      4:00 AM - 9:30 AM
  - Regular market trading session  9:30 AM - 4:00 PM
  - After-hours trading session     4:00 PM - 8:00 PM

* So, we'll need to set a scheduler trigger with cron to start with the pre-market until the end of after-market hours.
  ```plain
  Cairo time
  */5 11-23 * * 1-5
  +
  */5 0-4 * * 1-5

  OR

  ET Time (New York time)
  */5 04-20 * * 1-5
  ```

* We'll need 2 parallel workflows,
  1. the first is to delete the previous day's DB file.
```bash
# Delete old DB file. Runs daily at 4 AM
docker rm pyfinviz2 pyfinviz > /dev/null 2>&1
docker run -p 4000:4000 -v pyfinviz_data:/app/db -e NEWS_DATE_TODAY="true" --name pyfinviz nurhun/my-pyfinviz:v0.4 rm db/screener_results.db
```

  1. The second is to run the screener every 5 min from 4 AM to 8 PM ET
```bash
# ET Time (New York time) */5 04-20 * * 1-5
docker rm pyfinviz2 pyfinviz > /dev/null 2>&1
docker run -p 4000:4000 -v pyfinviz_data:/app/db -e NEWS_DATE_TODAY="true" --name pyfinviz2 nurhun/my-pyfinviz:v0.4
```
