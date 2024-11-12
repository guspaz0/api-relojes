from src.schemas import  MachineInfo, zkSizes, zkUser, zkFinger, zkUserTemplate, enrollUserZk, zkCreateUser
from fastapi.exceptions import HTTPException
import codecs
from src.services.utils import findMachine, instanceZkpy

def createUser(body: zkCreateUser):
    conn = None
    zk = instanceZkpy(body.machine)
    try:
        conn = zk.connect()

        conn.disable_device()

        conn.set_user(
            uid=body.uid,
            name=body.name,
            privilege=body.privilege,
            password=body.password,
            group_id=body.group_id,
            user_id=body.user_id,
            card=body.card
        )
        machineInfo = MachineInfo()
        machineInfo.users = conn.get_users()
        conn.enable_device()
        return machineInfo
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()
    conn=zk.connect()

def enrollUser(body: enrollUserZk):
    conn = None
    zk = instanceZkpy(body.machine)
    try:
        conn = zk.connect()
        conn.disable_device()
        zk.enroll_user(body.uid,body.temp_id,body.user_id)
        conn.enable_device()
        return fingerUser(body.machine, body.uid)
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()
    conn=zk.connect()

def fingerUser(machine,uid):
    conn = None
    zk = instanceZkpy(machine)
    try:
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        ##response= zkUser()
        response = []
        for i in range(0,10):
            template = conn.get_user_template(uid=int(uid), temp_id=i)
            if template:
                if template.size != 0:
                    response.append(zkFinger(
                        uid=template.uid,
                        fid=template.fid,
                        size=template.size,
                        valid=template.valid,
                        template=codecs.encode(template.template,'hex').decode('ascii')
                    ))
        conn.enable_device()
        return response
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()
    conn=zk.connect()

def deleteUser(machine, uid, legajo):
    conn = None
    zk = zk = instanceZkpy(machine)
    try:
        conn = zk.connect()
        conn.disable_device()

        response= zkUser(uid=int(uid))
        conn.get_users()
        conn.delete_user(uid=int(uid))

        conn.enable_device()
        return response
    except Exception as e:
        return HTTPException('Error no manejado en get info machine '+str(e))
    finally:
        if conn:
            conn.disconnect()
    conn=zk.connect()