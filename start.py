from drop import Drop
import random
# Display a welcome message



# Generate a random map of droplets.


drop1 = Drop(1,2,1)
print(drop1)

# Initialize gridmap
# size of the gridmap = 5
length = 5
gridmap = [[0 for i in range(length)] for j in range(length)]
# Random gridmap generation(TODO)
# difficulty = input("Choose your difficulty level from 1(easiest) to 5(hardest): ")

gridmap[0][2] = random.randint(0,9)
gridmapdefault = [[random.randint(0,9) for i in range(length)] for j in range(length)]

for row in gridmapdefault:
    for elem in row:
        print(elem, end=' ')
    print()

