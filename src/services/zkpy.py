from datetime import datetime,timedelta, timezone
from src.schemas import Checkinout, resp_reloj, FormData, Machine, MachineInfo, zkSizes, zkUser, zkFinger
from dotenv import dotenv_values
from fastapi.exceptions import HTTPException
from src.services.utils import findMachine, instanceZkpy

configEnv = dotenv_values(".env")

def getFichadas(machine, f_desde, f_hasta):
    conn = None
    zk = instanceZkpy(machine)
    try:
        desde = datetime.date(datetime.strptime(f_desde,'%Y-%m-%d'))
        hasta = datetime.date(datetime.strptime(f_hasta,'%Y-%m-%d'))
        conn = zk.connect()
        conn.disable_device()
        attendance = conn.get_attendance()
        att_filtro = resp_reloj(results=[])
        for i in attendance:
            if datetime.date(i.timestamp) >= desde and datetime.date(i.timestamp) <= hasta:
                check = Checkinout(
                    badgenumber=format(i.user_id),
                    checktime=format(i.timestamp),
                    sensorid=machine,
                    verifycode=format(i.status),
                    checktype=format(i.punch))
                att_filtro.results.append(check)
        conn.enable_device()
        return att_filtro
    except Exception as e:
        print(e)
        return HTTPException('error durante la peticion al reloj '+machine+' desde '+f_desde.strftime('%Y-%m-%d')+' hasta '+f_hasta.strftime('%Y-%m-%d'))
    finally:
        if conn:
            conn.disconnect()
    conn=zk.connect()

def getInfo(machine, fields):
    conn = None
    zk = instanceZkpy(machine)
    try:
        conn = zk.connect()
        conn.disable_device()
        
        querys = fields.split(',')

        response = MachineInfo()
        if 'all' in querys:
            response = MachineInfo(
                firmware_version=conn.get_firmware_version(),
                serialnumber=conn.get_serialnumber(),
                platform=conn.get_platform(),
                device_name=conn.get_device_name(),
                face_version=conn.get_face_version(),
                fp_version=conn.get_fp_version(),
                extend_fmt=conn.get_extend_fmt(),
                user_extend_fmt=conn.get_user_extend_fmt(),
                face_fun_on=conn.get_face_fun_on(),
                compat_old_firmware=conn.get_compat_old_firmware(),
                network_params=conn.get_network_params(),
                mac=conn.get_mac(),
                pin_width=conn.get_pin_width(),
                time=conn.get_time())
        if 'usage' in querys:
            conn.read_sizes()
            response.usage_space = zkSizes(
                users=conn.users,
                fingers=conn.fingers,
                records=conn.records,
                users_cap=conn.users_cap,
                fingers_cap=conn.fingers_cap)
        if 'users' in querys:
            response.users = conn.get_users()

        conn.enable_device()
        return response
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()

    conn=zk.connect()

def setTime(machine, origen):
    conn = None
    zk = zk = instanceZkpy(machine)
    try:
        conn = zk.connect()
        conn.disable_device()
        if origen == 'local':
            newtime = datetime.now()-timedelta(hours=3)
            conn.set_time(newtime)
        response= MachineInfo()
        response.time = conn.get_time()
        conn.enable_device()
        return response
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()

    conn=zk.connect()

def copyTemplates(origen, destino, uids):
    conn = None
    conn2= None
    zk = instanceZkpy(origen)
    zk2 = instanceZkpy(destino)
    try:
        conn = zk.connect()
        conn2 = zk2.connect()
        conn.disable_device()
        conn2.disable_device()
        list_uids = [uids]
        if ',' in uids:
            list_uids = [int(i) for i in uids.split(',')]
        templates = conn.get_templates()
        users = conn.get_users()
        for x in list_uids:
            user = None
            fingers = []
            for i in range(0,len(users)):
                if int(users[i].uid) == int(x):
                    user = users[i]
                    conn2.set_user(
                        uid=user.uid, 
                        name=user.name,
                        privilege=user.privilege, 
                        password=user.password,
                        group_id=user.group_id, 
                        user_id=user.user_id, 
                        card=user.card)
                    break
            for f in range(0,len(templates)):
                if int(templates[f].uid) == x:
                    temp = templates[f]
                    fingers.append(temp)
            conn2.save_user_template(user, fingers)
        response = MachineInfo()
        response.users = conn2.get_users()
        conn2.enable_device()
        conn.enable_device()
        return response
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()
        if conn2:
            conn2.disconnect()
    conn2.disconnect()
    conn=zk.connect()