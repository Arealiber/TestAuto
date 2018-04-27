from datetime import datetime
import pytz


def utc_to_shanghai_timezone(time_in):
    """
    utc时间转上海时区时间
    :param time_in: datetime格式的utc时间
    :return: datetime时间的本地时区时间
    """
    if time_in:
        time_utc = time_in.replace(tzinfo=pytz.timezone('UTC'))
        time_local = time_utc.astimezone(pytz.timezone('Asia/Shanghai'))
        return time_local
    return time_in


def shanghai_to_utc_timezone(time_in):
    """
    上海时区时间转utc时间
    :param time_in: datetime格式的utc时间
    :return: datetime时间的本地时区时间
    """
    if time_in:
        time_utc = time_in.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        time_local = time_utc.astimezone(pytz.timezone('UTC'))
        return time_local
    return time_in




