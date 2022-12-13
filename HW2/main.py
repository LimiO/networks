import subprocess
import validators
import sys


class Application:
    def __init__(self, host):
        self.min = 0 # 0 потому что выбираю с самого начала и меньше просто нет
        self.max = self.min + 1
        self.host = host

    def process(self):
        # тут мы находим какой потенциально может быть max
        self.find_max()
        return self.binsearch_mtu()

    def binsearch_mtu(self):
        l = self.min
        r = self.max
        # бинпоиск по mtu
        while r != l and r != l + 1:
            m = (l + r) // 2
            if self.is_mtu_can_set(m):
                l = m
            else:
                r = m
        if self.is_mtu_can_set(r):
            return r
        return l

    def find_max(self):
        # для чего это? Для того чтобы мы вообще поняли какой максимум mtu может быть. 
        max_ = self.max
        while True:
            if not self.is_mtu_can_set(max_):
                break
            max_ *= 2
        self.max = max_

    def is_mtu_can_set(self, mtu):
        # Собственно сам виновник торжества. Проверка ровно вот такая. 
        process = subprocess.Popen(['ping', self.host, '-M', 'do', '-s', str(mtu), '-c', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if process.wait() == 0:
            return True
        return False

def validate_icmp():
    process = subprocess.Popen(["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.wait() == 0:
        return
    print("Errors with ICMP")
    exit(1)

def check_alive(host):
    process = subprocess.Popen(['ping' , host, "-c", '1'])
    if process.wait() != 0:
        raise Exception("Bad host")


if len(sys.argv) < 2:
    print("No host")
    exit(1)
host = sys.argv[1]
if not validators.domain(host):
    print("Given not valid host")
    exit(1)
check_alive(host)
validate_icmp()

app = Application(sys.argv[1])
print(app.process() + 28)
