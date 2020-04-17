###########################
# 6.00.2x Problem Set 1: Space Cows

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=100):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse = True) # COPY the diction as a sorted list of tuples
    trips = []                                      # a list to store all the trips taken

    while len(sorted_cows) != 0:                    # repeat until there are no cows left
        temp_limit = limit                          # reset the limit after each trip
        cargo = []                                  # a list of cow names taken on a given trip, reset after each trip

        for i in range(len(sorted_cows)):           # loop through all the cows in decending order to see which ones fit
            if sorted_cows[i][1] <= temp_limit:     # if the cow fits...
                cargo.append(sorted_cows[i][0])     # ...add the cow to the cargo
                temp_limit -= sorted_cows[i][1]     # ...reduce the weight limit
                if temp_limit < sorted_cows[-1][1]: # if the limits is less than the smallest cow...
                    break                           # ...then stop checking cows

        trips.append(cargo)                         # cargo is full, make a trip and return

        for cow in cargo:                           # for each cow in the cargo...
            new_list = [i for i in sorted_cows if i[0] != cow] # ...make a new list of cows that are not on the ship
            sorted_cows = new_list                  # replace sorted_cows with the new lsit
    return trips                                    # planet is empty, return the list of trips made

# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse = True)  # COPY the diction as a sorted list of tuples
    partition = get_partitions(sorted_cows)                                 # a generator of permutations
    valid_routes = []                                                       # a list of lists containing the cargo of each valid route

#############################################################################
############ generate all routes ############################################
############ check if each route is valid (based on weight limits) ##########
############ save the valid routes ##########################################
#############################################################################
    while True:                                                             # repeat until I decide to stop
        try:                                                                # try will generate routes until all permutations are evaluated, then it will skip to the exception
            route = partition.__next__()                                    # generate the next permutation of trips
            is_valid = True
            for trip in route:                                              # look at each trip taken
                trip_weight = 0                                             # reset weight to zero
                for cow in trip:                                            # for each cow on the trip
                    trip_weight += cow[1]                                   # add the cows weight to the total
                if trip_weight > limit:                                     # if the total weight exceeds the limit...
                    is_valid = False
                    break                                                   # ... the trip is not valid -> discard the whole permutation
            if is_valid:
                valid_routes.append(route)                                  # ... save the permutation to a list of possible answers
        except:                                                             # do this once all possible routes have been evaluated
            break                                                           # end the while loop
#############################################################################
############### find the permutation with the fewest trips ##################
#############################################################################
    shortest_route = 100000
    optimal_route = []                                                      # a list of trips taken for the optimal route

    for route in valid_routes:                                              # for each possible answer
        num_trips = len(route)                                              # the number of trips taken on this permutation
        if num_trips < shortest_route:                                      # if it has the fewest number of trips so far...
            shortest_route = num_trips                                      # set its length as the minimum length
            optimal_route = route                                           # copy the list of trips to a new list
#############################################################################
######## return the list of names for each trip on the optimal route ########
#############################################################################
    cargo = []                                                              # the list of list of cow names on each trip (ie. the return variable)
    for trip in optimal_route:                                              # for each trip in the optimal route
        names = [cow[0] for cow in trip]                                             # add the name of each cow to the cargo list
        cargo += [names]
    return cargo
#############################################################################
#############################################################################
#############################################################################
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")

    start = time.time()
    greedy_cow_transport(cows, limit)
    end = time.time()
    print('Greedy Algo took:', end - start, 'seconds')

    start = time.time()
    brute_force_cow_transport(cows, limit)
    end = time.time()
    print('Brute Force Algo took:', end - start, 'seconds')
    pass


"""
Here is some test data for you to see the results of your algorithms with.
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
#cows = {"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}


#### checking answers vs test cases ####
#Test1 = {'Polaris': 20, 'Horns': 50, 'MooMoo': 85, 'Clover': 5, 'Miss Bella': 15, 'Lotus': 10, 'Muscles': 65, 'Louis': 45, 'Milkshake': 75, 'Patches': 60}
#Limit1 = 100
#Test2 = {'Coco': 10, 'Willow': 35, 'Abby': 38, 'Dottie': 85, 'Lilly': 24, 'Patches': 12, 'Buttercup': 72, 'Betsy': 65, 'Rose': 50, 'Daisy': 50}
#Limit2 = 100
#Test3 = {'Luna': 41, 'Willow': 59, 'Starlight': 54, 'Abby': 28, 'Buttercup': 11, 'Betsy': 39, 'Coco': 59, 'Rose': 42}
#Limit3 = 120
#
#ans1 = greedy_cow_transport(Test1, Limit1)
#ans2 = greedy_cow_transport(Test2, Limit2)
#ans3 = greedy_cow_transport(Test3, Limit3)
#
print('\n QUESTION ONE - GREEDY FUNCTION')
print(greedy_cow_transport(cows, limit))

#print('\n Test 1:')
#for trip in ans1:
#    print(trip)
#print('\n Test 2:')
#for trip in ans2:
#    print(trip)
#print('\n Test 3:')
#for trip in ans3:
#    print(trip)

print('\n QUESTION TWO - BRUTE FORCE')
print(brute_force_cow_transport(cows, limit))


