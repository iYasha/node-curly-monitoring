from dataclasses import dataclass
from dataclasses_json import dataclass_json
import psutil
import os
import json
from typing import List
import requests


@dataclass_json
@dataclass
class DiskUsage:
    total: float = 0.0
    used: float = 0.0
    free: float = 0.0


@dataclass_json
@dataclass
class RAM:
    total: float = 0.0
    used: float = 0.0
    free: float = 0.0


@dataclass_json
@dataclass
class UsageCPU:
    last_minute: float = 0.0
    last_five_minute: float = 0.0
    last_fifteen_minute: float = 0.0


@dataclass_json
@dataclass
class TempCPU:
    current: float = 0.0
    high: float = 0.0
    critical: float = 0.0


@dataclass_json
@dataclass
class CPU:
    count: int = 0
    percent_usage: UsageCPU = UsageCPU()
    sensors_temperatures: TempCPU = TempCPU()


@dataclass_json
@dataclass
class DockerState:
    status: str
    running: bool
    paused: bool
    restarting: bool
    dead: bool
    pid: int
    exit_code: int
    error: str
    started_at: str
    finished_at: str


@dataclass_json
@dataclass
class Docker:
    state: DockerState
    name: str
    restart_count: int
    ports: list


@dataclass_json
@dataclass
class ServerStats:
    cpu: CPU
    ram: RAM
    disk: DiskUsage
    docker: List[Docker]


def to_gb(number: int) -> float:
    return round(number / (2 ** 30), 2)


def get_disk() -> DiskUsage:
    if hasattr(psutil, "disk_usage"):
        disk = psutil.disk_usage('/')
        return DiskUsage(
            total=to_gb(disk.total),
            used=to_gb(disk.used),
            free=to_gb(disk.free),
        )
    return DiskUsage()


def get_ram() -> RAM:
    if hasattr(psutil, "virtual_memory"):
        mem = psutil.virtual_memory()
        return RAM(
            total=to_gb(mem.total),
            used=to_gb(mem.used),
            free=to_gb(mem.active)
        )
    return RAM()


def get_cpu() -> CPU:
    if hasattr(psutil, "cpu_count") and hasattr(psutil, "getloadavg"):
        cpu_usage = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    else:
        cpu_usage = [0.0, 0.0, 0.0]
    if hasattr(psutil, "sensors_temperatures"):
        current = []
        high = []
        critical = []
        for temp in psutil.sensors_temperatures()['coretemp']:
            current.append(temp.current)
            high.append(temp.high)
            critical.append(temp.critical)
        temp = TempCPU(
            current=sum(current) / len(current),
            high=sum(high) / len(high),
            critical=sum(critical) / len(critical),
        )
    else:
        temp = TempCPU()
    if hasattr(psutil, "cpu_count"):
        return CPU(
            count=psutil.cpu_count(),
            percent_usage=UsageCPU(
                last_minute=cpu_usage[0],
                last_five_minute=cpu_usage[1],
                last_fifteen_minute=cpu_usage[2]
            ),
            sensors_temperatures=temp
        )
    return CPU()


def get_docker() -> List[Docker]:
    docker_data = os.popen("docker inspect --format '{{json .}}' $(docker ps -qa)").read()
    container_data = [json.loads(x) for x in docker_data.split('\n') if x]
    docker_info = [
        Docker(
            state=DockerState(
                status=x['State']['Status'],
                running=x['State']['Running'],
                paused=x['State']['Paused'],
                restarting=x['State']['Restarting'],
                dead=x['State']['Dead'],
                pid=x['State']['Pid'],
                exit_code=x['State']['ExitCode'],
                error=x['State']['Error'],
                started_at=x['State']['StartedAt'],
                finished_at=x['State']['FinishedAt'],
            ),
            name=x['Name'].replace('/', ''),
            restart_count=x['RestartCount'],
            ports=x['NetworkSettings']['Ports'].keys()
        )
        for x in container_data]
    return docker_info


if __name__ == '__main__':
    stats = ServerStats(cpu=get_cpu(),
                        disk=get_disk(),
                        ram=get_ram(),
                        docker=get_docker()
                        )
    requests.post(url=f'{os.getenv("MASTER_SERVER")}/server/stats', json=stats.to_json())
