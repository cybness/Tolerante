import sys
import time
import psutil

def check_arguments():
    if len(sys.argv) == 1:
        print('Este programa necesita nombres de procesos como argumentos.')
        sys.exit(0)

def get_targets():
    targets = sys.argv[1:]
    return [t + '.exe' if not t.endswith('.exe') else t for t in targets]

def monitor(targets):
    procesos_vistos = set()

    while True:
        procesos_actuales = {proc.name().lower(): proc.pid for proc in psutil.process_iter(attrs=['pid', 'name'])}
        
        for target in targets:
            target_lower = target.lower()
            
            if target_lower in procesos_actuales:
                if target_lower not in procesos_vistos:
                    print(f"✔ La aplicación '{target}' está en ejecución con PID {procesos_actuales[target_lower]}.")
                    procesos_vistos.add(target_lower)
            else:
                if target_lower in procesos_vistos:
                    print(f"✖ La aplicación '{target}' se ha cerrado.")
                    procesos_vistos.remove(target_lower)

        time.sleep(2)

if __name__ == '__main__':
    check_arguments()
    targets = get_targets()
    monitor(targets)
