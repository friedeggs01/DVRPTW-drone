from .baseline import Node
import numpy as np


# Decision policy
# All the terminals are correspond to the current vehicle, for which decision is being made of which customer to visit next

# distance to the customer being considered (maybe change with time due to velocity at this time)

# customer demand (maybe not because we will solve stochastic demand problem)

# truck remaining capacity

# drone remaining capacity

# drone remaining battery

# waiting time of drone to meet truck again

# the amount of time till the customer can ready to served

# the amount of time till customer due date

# service value?
class DDR(Node):
    ...