import json
import sys
import urllib.request

def fetch_activity(username): #ucitava sa gita
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:#otvara konekcij
            data = json.loads(response.read().decode()) #ucitava i dekodira json
            return data #vraca listu podataka
    except Exception as e:
        print(f"Greska u hvatanju aktivnosti za usera '{username}': {e}")
        return [] #ako dodje do greske ili nepostojecih podataka vraca se prazna lista

def parse_event(event):
    type = event.get("type")
    repo = event.get("repo", {}).get("name", "Nepoznat repo")

    if type == "PushEvent":#koliko ima pushovanih eventa na dat repo
        commits = len(event.get("payload", {}).get("commits", []))
        return f"Izbaceno {commits} commit(s) na {repo}"
    elif type == "IssuesEvent":#koliko ima "zapocetih problema" na repo
        action = event.get("payload", {}).get("action", "nepoznata akcija")
        return f"{action.capitalize()} problem u repozitorijumu - {repo}"
    elif type == "WatchEvent": #koliko ima obelezenih projekata
        return f"Zvezdica na {repo}"
    elif type == "ForkEvent": #koliko ima kopiranih projekata
        return f"Forkovan {repo}"
    else:
        return f"{type} na {repo}"

# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kako se koristi: python __main__.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    events = fetch_activity(username)
    for event in events:
        print(parse_event(event))
