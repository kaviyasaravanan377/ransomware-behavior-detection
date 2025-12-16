import math

def calculate_entropy(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if not data:
            return 0

        freq = {}
        for b in data:
            freq[b] = freq.get(b, 0) + 1

        entropy = 0
        for count in freq.values():
            p = count / len(data)
            entropy -= p * math.log2(p)

        return entropy
    except:
        return 0
