import datetime
import psutil
import requests
import json
import os


def createData():
    """
    送信するデータの生成を行います。
    """
    mem = psutil.virtual_memory()
    memUsed = mem.used / 1024 / 1024
    memAvailable = mem.available / 1024 / 1024
    memTotal = mem.total / 1024 / 1024
    memPercent = mem.percent

    cpuPercent = psutil.cpu_percent(interval=10)

    disk = psutil.disk_usage(path='/')
    diskPercent = disk.percent
    diskUsed = disk.used / 1024 / 1024 / 1024
    diskFree = disk.free / 1024 / 1024 / 1024
    diskTotal = disk.total / 1024 / 1024 / 1024

    print(f"cpu: percent: {cpuPercent}")
    print(
        f"mem: used: {memUsed}, available: {memAvailable}, total: {memTotal}, percent: {memPercent}")
    print(
        f"Disk: used: {diskUsed}, free: {diskFree}, total: {diskTotal}, percent: {diskPercent}")

    nowDateTime = datetime.datetime.utcnow()

    data = {
        "cpu": cpuPercent,
        "memUsed": memUsed,
        "memAvailable": memAvailable,
        "diskUsed": diskUsed,
        "diskFree": diskFree,
        "created_at": nowDateTime.isoformat(timespec='seconds') + "Z"
    }

    return data


def send(data, config):
    """
    データの送信を行います。
    Args:
        data : 送信するデータを指定します。
        config : 設定情報を指定します。
    """
    url = config["endpoint"]

    params = {
        "post_key": config["postKey"],
        "collection_id": config["collectionID"]
    }

    sendData = json.dumps(data)
    print(sendData)

    response = requests.post(
        url,
        headers={'content-type': 'application/json'},
        params=params,
        data=sendData,
        verify=False,
    )

    print(response)


def main():
    """
    メイン関数です。
    """
    currentDir = os.path.dirname(__file__)
    jsonFile = open(f"{currentDir}/config.json", "r")

    config = json.load(jsonFile)

    data = createData()
    send(data, config)


main()
