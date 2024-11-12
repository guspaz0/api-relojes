import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK
from src.schemas import Machine
from dotenv import dotenv_values
import psycopg2

configEnv = dotenv_values(".env")

config = {
    'host':configEnv["DB_HOST"],
    'database':configEnv["DB_NAME"],
    'user':configEnv["DB_USER"],
    'password':configEnv["DB_PASS"]
}

conn = psycopg2.connect(**config)
cur = conn.cursor()

def findMachine(machine):
    try:
        cur.execute('SELECT * FROM "Machines" '+ f"where sensorid = '{machine}';")
        data = cur.fetchone()
        if data:
            data = Machine(sensorid=data[0],serialnumber=data[1],sensorname=data[2],ip=data[3],ddns=data[4])
            return data
        else:
            raise IndexError('no existe el reloj')
    except Exception as e:
        return {'message': f"el reloj no existe {e}"}

def instanceZkpy(sensorid):
    machineData = findMachine(sensorid)
    zk = ZK(machineData.ip, port=int(configEnv["ZK_PORT"]), timeout=10, password=int(configEnv["ZK_PASS"]), force_udp=False, ommit_ping=True, verbose=False)
    return zk