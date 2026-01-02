import platform

def detect_platform():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        arch = "amd64"
    elif "arm" in machine or "aarch64" in machine:
        arch = "arm64"
    else:
        arch = machine

    return system, arch

if __name__ == "__main__":
    print(detect_platform())
