# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics

import random
import pylab
random.seed(0)

'''
Begin helper code
'''
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() > self.clearProb:
            return False
        else:
            return True

    def __str__(self):
        return 'I am a Simple Virus '

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException()
        else:
            return SimpleVirus(self.maxBirthProb, self.clearProb)


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.maxPop = maxPop
        self.viruses = viruses

    def __str__():
        return 'I am a patient'

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max possible population of viruses within this patient.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # create a copy of the list of viruses
        copy_viruses = self.viruses[:]

        # determine if each virus survives or not
        for virus in copy_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)

        # update the population density
        popDensity = len(self.viruses) / self.maxPop

        # determine if each virus reproduces or not
        copy_viruses = self.viruses[:]
        if popDensity < 1:
            for virus in copy_viruses:
                try:
                    self.viruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    pass

        return len(self.viruses)

#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # a dictionary for the virus populate for each time step
    # the step number is the key
    # the values are lists of viral populations from multiple simulations
    trial_results = {}

    # a list of all the viruses
    viruses = []

    # create the number of viruses defined in the function call
    for virus in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))

    # create a single patient
    sickMan = Patient(viruses, maxPop)

    # one trial of the simulation to build the list
    for step in range(300):
        trial_results[step] = [sickMan.update()]

    # subsequent trials are added to the list
    for trial in range(numTrials - 1):

        # a list of all the viruses
        viruses = []

        # create the number of viruses defined in the function call
        for virus in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))

        # create a new patient for each trial
        sickMan = Patient(viruses, maxPop)

        # simulate 300 time steps and record the progression of the virus after each step
        for step in range(300):
            trial_results[step].append(sickMan.update())

    # average the trial results
    averages = []
    for k, v in trial_results.items():
        averages.append(sum(v)/len(trial_results[k]))

    pylab.plot(averages, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def __str__(self):
        return 'I am a Resistant Virus.'

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # if 'drug' is not in the resistances dictionary then add it as false
        # then return the value of 'drug'
        if not drug in self.resistances:
            self.resistances[drug] = False
        return self.resistances[drug]

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # store all immunities into a list
        immune_list = []
        for k, v in self.resistances.items():
            if v:
                immune_list.append(k)

        # create the immunity dictionary for the child
        child_resistances = {}

        # store immunities PLUS MUTATIONS in the child's dictionary
        for k, v in self.resistances.items():
            if random.random() > (1 - self.mutProb):
                child_resistances[k] = 1 - v
            else:
                child_resistances[k] = v


        # check if the virus is immune to all drugs in the list
        if all(drug in immune_list for drug in activeDrugs):

            # stochastically determine whether this virus reproduces
            if random.random() > self.maxBirthProb * (1 - popDensity):
                raise NoChildException()
            else:
                return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)



class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.prescription = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if not newDrug in self.prescription:
            self.prescription.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescription


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # the number of viruses that are resistant to all drugs
        count = 0

        # for each virus in the list provided
        for virus in self.viruses:
            # store its immunities into a list
            immune_list = []
            for k, v in virus.getResistances().items():
                if v:
                    immune_list.append(k)
            # check if the virus is immune to all drugs in the list
            if all(drug in immune_list for drug in drugResist):
                count += 1

        return count


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # a copy of the list of viruses
        copy_viruses = self.viruses[:]

        # determine if each virus survives or not
        for virus in copy_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)

        # update the population density
        popDensity = len(self.viruses) / self.maxPop

        # determine if each virus reproduces or not
        copy_viruses = self.viruses[:]

        if popDensity < 1:
            # virus can only reproduce if it is immune to all drugs administered
            for virus in copy_viruses:
                # store all immunities into a list
                immune_list = []
                for k, v in virus.getResistances().items():
                    if v:
                        immune_list.append(k)
                # check if the virus is immune to all drugs administered
                if all(drug in immune_list for drug in self.prescription):
                    try:
                        self.viruses.append(virus.reproduce(popDensity, self.prescription))
                    except NoChildException:
                        pass
        return len(self.viruses)

#
# PROBLEM 4
#

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """
    steps = 150
    # store the results of each trial as a list
    # append all trial lists together to make a list of lists for each dataset
    virus_pop = []
    resistant_pop = []

    # run numTrials trials
    for trial in range(numTrials):

        # create a new list of numViruses x ResistantVirus instances
        viruses = []
        for i in range(numViruses):
            virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(virus)

        # create a new instance of a treated patient
        Treated_Patient = TreatedPatient(viruses, maxPop)

        # create empty lists to store the results for this one trial
        virus_pop_trial = []
        resistant_pop_trial = []

        # run 150 timesteps
        for step in range(steps):

            # store values in list
            virus_pop_trial.append(Treated_Patient.update())
            resistant_pop_trial.append(Treated_Patient.getResistPop(['guttagonol']))

        # prescribe drug to the patient
        Treated_Patient.addPrescription('guttagonol')

        # run another 150 updates
        for step in range(steps):

            # store values in list
            virus_pop_trial.append(Treated_Patient.update())
            resistant_pop_trial.append(Treated_Patient.getResistPop(['guttagonol']))

        # add the trial results to the master lists
        virus_pop.append(virus_pop_trial)
        resistant_pop.append(resistant_pop_trial)

    # compute averages
    avg_virus_pop = []
    avg_resistant_pop = []

    for step in range(steps * 2):
        total1 = 0
        total2 = 0
        for trial in range(numTrials):
            total1 += virus_pop[trial][step]
            total2 += resistant_pop[trial][step]
        avg_virus_pop.append( total1 / numTrials )
        avg_resistant_pop.append( total2 / numTrials)

    # chart the data
    pylab.plot(avg_virus_pop, label = "Average Virus Population")
    pylab.plot(avg_resistant_pop, label = "Average Guttagonol Resistant Population")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()

