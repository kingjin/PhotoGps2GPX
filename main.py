import exifread  # pip install exifread
import os


def read(picPath):
    f = open(picPath, 'rb')
    contents = exifread.process_file(f)
    ong = 0
    lat = 0
    GPSAltitude = 0
    for key in contents:
        # print("key", key, contents[key])

        if key == "GPS GPSLongitude":
            # print("经度 =", contents[key].printable, contents['GPS GPSLatitudeRef'])
            lon = contents[key].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            long = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600

        elif key == "GPS GPSLatitude":
            # print("纬度 =", contents[key], contents['GPS GPSLongitudeRef'])

            lat = contents[key].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
        elif key == "GPS GPSAltitude":
            GPSAltitude = float(contents[key].printable.replace("1000", "").replace("/", "")) / 1000
            # print("GPSAltitude 高度", GPSAltitude)

    return float(lat), float(long), float(GPSAltitude)


if __name__ == '__main__':

    # 图片所在的目录
    basePath = r"C:\Users\xxxx\Desktop\20220404"

    listName = os.listdir(basePath)

    strGps = ""
    inxx = 0  # 记录图片张数
    TmpGps = '''<wpt lat="%s" lon="%s"><name>%s</name><geoidheight>%s</geoidheight></wpt>'''
    for name in listName:
        picPath = os.path.join(basePath, name)

        # 判断是否为文件
        if not os.path.isfile(picPath):
            continue

        LotLone = read(picPath)
        if len(LotLone) == 3:
            inxx = inxx + 1
            strGps = strGps + "\n" + TmpGps % (LotLone[0], LotLone[1], inxx, LotLone[2])

    strGps = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="MyGeoPosition.com" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"> ''' + strGps + '''</gpx>'''

    print(strGps)
    # 保存到文件
    with open('test.gpx', "w+", encoding="utf-8") as saveFile:
        saveFile.write(strGps)


