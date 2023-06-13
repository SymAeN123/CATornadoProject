from boto.s3.connection import S3Connection
from datetime import timedelta, datetime
import os

def _nearestDate(dates, pivot):
    return min(dates, key=lambda x: abs(x - pivot))

def _get_day(keys, datetimes, bucket_list):
    for i in range(len(bucket_list)):
        filename = str(bucket_list[i].key).split("/")[4]
        filename_split = (filename.split('.')[0]).split("_")
        dt_s = filename_split[0][4:] + "_" + filename_split[1]
        format = "%Y%m%d_%H%M%S"
        try:
            dt = datetime.strptime(dt_s, format)
        except ValueError:
            continue
        datetimes.append(dt)
        keys.append(bucket_list[i])

def _get_files(site, begin, end):
    num_days = end.day-begin.day+1
    conn = S3Connection(anon=True)
    bucket = conn.get_bucket('noaa-nexrad-level2')

    b_pref = begin.strftime('%Y/%m/%d/')+site
    b_list = list(bucket.list(prefix=b_pref))
    b_keys = []
    b_datetimes = []
    _get_day(b_keys, b_datetimes, b_list)

    if num_days >= 2:
        e_pref = end.strftime('%Y/%m/%d/')+site
        e_list = list(bucket.list(prefix=e_pref))
        e_keys = []
        e_datetimes = []
        _get_day(e_keys, e_datetimes, e_list)

    if num_days >= 3:
        num_middle_days = num_days - 2
        m_keys = []
        m_datetimes = []
        m_time = begin+timedelta(days=1)
        for i in range(num_middle_days):
            m_keys.append([])
            m_datetimes.append([])
            m_pref = (m_time+timedelta(days=i)).strftime('%Y/%m/%d/')+site
            m_list = list(bucket.list(prefix=m_pref))
            _get_day(m_keys[i], m_datetimes[i], m_list)

    keys = b_keys
    datetimes = b_datetimes
    if num_days >= 3:
        for day in m_keys:
            keys += day
        for day in m_datetimes:
            datetimes += day
    if num_days >= 2:
        keys += e_keys
        datetimes += e_datetimes

    return keys, datetimes


def download_radar_data(site: str, begin: datetime, end: datetime, abs_path: str = None):
    if not (abs_path is None):
        old_dir = __file__.removesuffix("downloader.py")
        os.chdir(abs_path)

    keys, datetimes = _get_files(site, begin, end)
    if len(keys) == 0:
        print(f"No data in site {site}.")
        return

    closest_b_datetime = _nearestDate(datetimes, begin)
    closest_e_datetime = _nearestDate(datetimes, end)
    b_index = datetimes.index(closest_b_datetime)
    e_index = datetimes.index(closest_e_datetime)

    for i in range(b_index, e_index+1):
        keys[i].get_contents_to_filename(str(keys[i].key).split("/")[4])

    if not (abs_path is None):
        os.chdir(old_dir)
    
    print(f"Finished downloading site {site}.")