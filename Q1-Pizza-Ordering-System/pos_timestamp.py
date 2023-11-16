import time
import datetime as dt
from pos_constants import TIMEFMT, DATEFMT, DATE_WITH_TIMEFMT


def main() -> None:
    currentTime = time.time()
    strTime = dt.datetime.fromtimestamp(currentTime).strftime(TIMEFMT)
    strDate = dt.datetime.fromtimestamp(currentTime).strftime(DATEFMT)
    print(strTime, strDate)
    # int(time.mktime(time.strptime(strTime, TIMEFMT)))


    # iso = dt.datetime.now().isoformat()
    # print(iso)
if __name__ == "__main__":
    main()
