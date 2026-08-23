import subprocess

# list
# 215 list follows
# aliens.general 19 1 y
# aliens.proof 38 20 y
# aliens.random 51 39 y
GROUPS = {
    "aliens.general": [1, 19],
    "aliens.proof": [20, 38],
    "aliens.random": [39, 51]
}

for group in GROUPS:
    for i in range(GROUPS[group][0], GROUPS[group][1]):
        subprocess.run(f"echo 'group {group}\r\narticle {i}\r\nquit' | nc localhost 119 >> log.txt", shell=True)