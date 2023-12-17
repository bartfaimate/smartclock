
import datetime as dt
from typing import  Union


def subset(start_date, end_date):
    start_date = parse_time(start_date)
    end_date = parse_time(end_date)
    duration = max(1, (end_date - start_date).days)
    for i in range(duration):
        yield start_date + dt.timedelta(days=i)


def parse_time(time_expr: Union[str, dt.datetime]) -> dt.datetime:
    if not time_expr:
        raise RuntimeError("Time expression should be provided")
    if isinstance(time_expr, dt.datetime):
        return time_expr
    if isinstance(time_expr, dt.date):
        return dt.datetime(
            time_expr.year, time_expr.month, time_expr.day, 0, 0, 0
        )
    if not isinstance(time_expr, str):
        return time_expr

    formats = ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z")
    for fmt in formats:
        try:
            if fmt == "%Y-%m-%dT%H:%M:%S%z":
                dt_part, tz_info = time_expr.split("+")
                tz_info = tz_info.replace(":", "")
                time_expr = f"{dt_part}+{tz_info}"
            time_expr = dt.datetime.strptime(time_expr, fmt)
        except ValueError:
            continue
        else:
            return time_expr
    raise ValueError("Wrong date format", time_expr)


def get_tz_offset(date_time: dt.datetime):

    tz_info = date_time.tzinfo if date_time.tzinfo else date_time.astimezone().tzinfo

    delta = tz_info.utcoffset(date_time)

    delta = int(delta.seconds) + int(delta.days) * 24 * 3600
    delta_h = delta // 3600
    sign = "+" if delta_h >= 0 else "-"
    delta_m = delta % 3600 // 60
    return f"{sign}{str(abs(delta_h)).zfill(2)}:{str(delta_m).zfill(2)}"
