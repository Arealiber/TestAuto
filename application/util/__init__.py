from datetime import datetime
import pytz


def convert_timezone(time_in):
    """
    系统时间转换成utc时间本地时区时间
    :param time_in: datetime格式的utc时间
    :return: datetime时间的本地时区时间
    """
    if time_in:
        time_utc = time_in.replace(tzinfo=pytz.timezone('UTC'))
        time_local = time_utc.astimezone(pytz.timezone('Asia/Shanghai'))
        return time_local
    return time_in





