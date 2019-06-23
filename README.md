# Promoter.io NPS Downloader

A Python script for downloading NPS data using the [NPS API](https://developers.promoter.io/reference) to local files, integrated with [Mara](https://github.com/mara). 

## Resulting data
It creates one data set as CSV with the following structure:

1. **Campaign Performance** consists of measures such as score, score_type, campaign, and contact attributes. The script creates one file per day in a specified time range:
                            
   data/2015/03/31/nps/nps_v1.csv

   Each line contains one NPS user feedback with the score and other information:

        id             | 12312
        score          | 9
        score_type     | promoter
        created        | 2016-09-30T10:09:17.339051Z
        attributes     | {"customerid" : 34223, "orderid": 11111}
        sent_date      | 2016-09-30T02:48:25.435403Z
        campaign_id    | 123123
        campaign_name  | BE_Dutch_Search
        comments       | I'm happy with the service provided   


## Getting Started

### Prerequisites

To use the NPS Downloader you have to create an API token to access the Promoter.io API.

### Installation

 The NPS Downloader requires:

    Python (>= 3.5)
    requests (>=2.19.1)
    click (>=6.0)

The easiest way to install nps-downloader is using pip

    pip install git+git@github.com:jrolland82/nps-downloader.git --process-dependency-links

In case you want to install it in a virtual environment:

    $ git clone git@github.com:jrolland82/nps-downloader.git nps_downloader
    $ cd nps_downloader
    $ python3 -m venv .venv
    $ .venv/bin/pip install . --process-dependency-links


## Usage

To run the NPS Performance Downloader call `download-nps-data` with its config parameters:  

    $ download-nps-data \
    --access_token "Token blabla344235dfd34"
    --data_dir /tmp/nps
    --first_date '2016-08-21'
