import requests

states = []
with open("weatherstates.txt") as f:
    for line in f:
        states.append(line.strip())
print(states)

# for state part print(states.split("/")) then split on -, just in case. Then Title.
weather = requests.get(states[0])
print(weather.content)
