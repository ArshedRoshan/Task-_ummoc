votes = {'A': 0, 'B': 0, 'C': 0}

def vote(name):
    global votes
    if name in votes:
        votes[name] += 1
        return True
    else:
        return False

def count_votes():
    sorted_votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
    return sorted_votes



vote('A')
vote('B')
vote('A')

print(count_votes())