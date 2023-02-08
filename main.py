import time
from driver import SearchEngine
se = SearchEngine(0)

while True:
    se.load_site("https://deprem.io/yardim-istek-enkaz")
    time.sleep(5)
    if se.isAvailable() == 0:
        print("We go")
        se.send_food()
        time.sleep(30)
    else:
        print("Waiting next rount")
        time.sleep(60)
