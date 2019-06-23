from datetime import datetime, timedelta
import csv
import os
import requests
from pathlib import Path
import errno
import logging

from nps_downloader import config

PROMOTER_API_BASE_URL = 'https://app.promoter.io/api/v2/feedback/'
FILE_OUTPUT_VERSION = 'v1'


def download_data():
    headers = {
        'Authorization': config.access_token(),
        'Content-Type': 'application/json'
    }
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890()¿?!%&áéíóúàèìòùäëïöü')

    start_date = datetime.strptime(config.first_date(), "%Y-%m-%d").date()
    today = datetime.utcnow().date()

    for day in [today - timedelta(x) for x in range((today - start_date).days + 1)]:
        relative_path = Path('{year}/{month}/{day}/nps/nps_{version}.csv'.format(year=str(day.year),
                                                                                 month=str(day.month).zfill(2),
                                                                                 day=str(day.day).zfill(2),
                                                                                 version=FILE_OUTPUT_VERSION))
        ensure_data_directory(relative_path)
        current_path = Path(config.data_dir()) / relative_path

        # It does not download from the API if the file already exists, except for today
        if os.path.isfile(current_path) and day != today:
            logging.info('Skipping {path}, it already exists'.format(path=str(current_path)))
        else:
            logging.info('Generating {path} ...'.format(path=str(current_path)))
            next_day_limit = day + timedelta(days=1)

            url = '{base_url}?posted_date_0={day}&posted_date_1={next_day_limit}'.format(base_url=PROMOTER_API_BASE_URL,
                                                                                         next_day_limit=next_day_limit,
                                                                                         day=day)
            tmp_list_result = []

            while url:
                json_decoded = requests.get(url, headers=headers).json()
                url = json_decoded['next'] if 'next' in json_decoded else None
                result_list = json_decoded['results'] if 'results' in json_decoded else []

                for result in result_list:
                    comment = str(result['comment'])
                    tmp_list_result.append([result['id'], result['score'], result['score_type'], result['created'],
                                            result['contact']['attributes'], result['survey']['sent_date'],
                                            result['campaign']['id'], result['campaign']['name'],
                                            ''.join(filter(whitelist.__contains__, comment))])

            if len(tmp_list_result) > 0:
                logging.info('{records} records to insert into {path} ...'.format(records=str(len(tmp_list_result)),
                                                                                  path=str(current_path)))
                nps = open(current_path, 'w')
                with nps:
                    writer = csv.writer(nps)
                    writer.writerows(tmp_list_result)


def ensure_data_directory(relative_path: Path = None) -> Path:
    """Checks if a directory in the data dir path exists. Creates it if necessary

    Args:
        relative_path: A Path object pointing to a file relative to the data directory

    Returns:
        The absolute path Path object

    """
    if relative_path is None:
        return Path(config.data_dir())
    try:
        path = Path(config.data_dir(), relative_path)
        # if path points to a file, create parent directory instead
        if path.suffix:
            if not path.parent.exists():
                path.parent.mkdir(exist_ok=True, parents=True)
        else:
            if not path.exists():
                path.mkdir(exist_ok=True, parents=True)
        return path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
