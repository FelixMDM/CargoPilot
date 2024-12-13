import pandas as pd

class Container:
    def __init__(self, pos=[0,0], weight=00000, name="UNUSED"):
        self.pos = pos
        self.weight = weight
        self.name = name

# getters
    def get_position(self):
        return self.pos

    def get_weight(self):
        return self.weight
    
    def get_name(self):
        return self.name
    
# printing the container in a nice stylized way
    def print_container(self):
        print(f"Name: {self.name}\nWeight: {self.weight}\nPosition: {self.pos}\n")

def read_manifest(input_file):
    grid = [[Container() for _ in range(12)] for _ in range(8)]

    df = pd.read_csv(input_file, header=None, sep=", ", engine='python')
    for i in range(96):
        row = df.iloc[i].tolist()

        numbers = []
        curr = ""
        for char in row[0]:
            if char.isdigit():
                curr += char
            elif curr:
                numbers.append(int(curr))
                curr = ""
        if curr:
            numbers.append(int(curr))

        x,y = numbers
        curr = ""
        for char in row[1]:
            if char.isdigit():
                curr += char

        weight = int(curr)
        container = Container([x,y], weight, row[2])
        grid[x-1][y-1] = container

    for row in range(8):
        for col in range(12):
            grid[row][col].print_container()

    return grid

def main():
    filename = "ShipCase1.txt"
    read_manifest(filename)

if __name__ == "__main__":
    main()