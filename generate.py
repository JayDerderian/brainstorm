#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms ranging from pure "random"
    selections (see PRNG info), to more strict instructions. 

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
from random import randint
from midi import midiStuff as mid
from containers.melody import melody

#Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms ranging from pure "random"
    selections (see PRNG info), to more strict instructions.  
    '''

    # Constructor
    def __init__(self):


        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#


        # ----------Letters--------------#  

        '''Used to search against and return an integer representing an 
           Array index. The array will be used to generate a scale from
           whos total is the len(alphabet) - 1
           
           NOTE: Account for capitalization!'''


        self.alphabet = ['a', 'b','c','d', 'e', 'f', 'g',
                         'h','i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u',
                         'v', 'w', 'x', 'y,' 'z']

        #--------Notes and Scales--------#

        # Enharmonically spelled note names starting on A. Indicies: 0-16.
        # NOTE THE STARTING NOTE! 
        self.notes = ["A", "A#", "Bb", "B", 
                      "C", "C#", "Db", "D", 
                      "D#", "Eb", "E", "F", 
                      "F#", "Gb", "G", "G#",
                      "Ab"]

        # Major Scales
        '''
        NOTE:
            We won't need to create extra scales if we want to create 
            some kind of "mood" feature (happy/sad) since those "moods" 
            are usually elicited from chord progressions. If we want that, 
            then I'll just add a function to generate some minor chords based
            off the scale chosen from the dicitonary below.
        '''
        # Use indicies 1 - 12
        self.scales = {1: ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 
                       2: ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
                       3: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#' ],
                       4: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
                       5: ['E', 'F#', 'G#', 'A', 'B', 'C#', "D#"],
                       6: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
                       7: ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
                       8: ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                       9: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
                       10:['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                       11:['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
                       12:['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']}

     
        #-------------Rhythm--------------#

        '''
        NOTE:
            Durations in seconds (1 = quarter note (60bpm))
            Whole note to 32nd note
            
                [0] 4 = whole note                                                          
                [1] 3 = dotted half
                [2] 2 = half note           
                [3] 1.5 = dotted quarter    
                [4] 1 = quarter             
                [5] 0.75 = dotted eighth
                [6] 0.5 = eighth
                [7] 0.375 = dotted sixteenth
                [8] 0.25 = sixteenth 
                [9] 0.125 = thirty-second

        '''
        # Rhythms (0-9)
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 
                        0.375, 0.25, 0.125]

        # Fast rhythms (0-8)
        self.rhythmsFast = [0.375, 0.28125, 0.25, 0.1875, 0.125, 0.09375, 
                            0.0625, 0.046875, 0.03125]

        # Slow rhythms (0-7) - [n2 = n1 + (n1/2)]
        self.rhythmsSlow = [8.0, 12.0, 18.0, 27.0, 
                            40.5, 60.75, 91.125, 136.6875]
        
  
        #------------Tempo-------------#

        # Tempos (indices: 0-38)
        self.tempos = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0, #1-9 (0-8)
                       60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, #10-18 (9-17)
                       92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
                       126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, #28-36 (27-35)
                       184.0, 200.0, 208.0] #37-39 (36-38)


        #-----------Dynamics------------#
        
        '''
        NOTE: MIDI velocity/dynamics range: 0 - 127
        '''

        # Dynamics (0-26)
        self.dynamics = [20, 24, 28, 32, 36, 40, 44, 48, 52,
                         56, 60, 64, 68, 72, 76, 80, 84, 88,
                         92, 96, 100, 104, 108, 112, 116, 120, 124]

        # Soft dynamics (0-8)
        self.dynamicsSoft = [20, 24, 28, 32, 36, 40, 44, 48, 52]

        # Medium dynamics (0-8)
        self.dynamicsMed = [56, 60, 64, 68, 72, 76, 80, 84, 88]

        # Loud dynamics (0-8)
        self.dynamicsLoud = [92, 96, 100, 104, 108, 112, 116, 120, 124]



    #-----------------------------------------------------------------------------------------#
    #-----------------------------Conversion and Utility Functions----------------------------#
    #-----------------------------------------------------------------------------------------#

    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''Converts an array of floats to an array of ints'''
        if(data is None):
            return -1
        result = []
        for i in range(len(data)):
            result.append(int(data[i]))
        return result

    # Convert array of integers to be within the len-1 of another array. 
    def scaleTheScale(self, data, scale):
        '''
        This repeatedly subtracts the value of len(scale) - 1 from each integer in the 
        data array. This will keep the newly inputted array's values within the bounds 
        of the scale array. These values function as a collection of index numbers 
        to randomly chose from in order to pick note strings from the scale array.

        For example, if the given data array is [0, 55, 2, 71, 5] and the len
        of the scale array is 25, then the result should be [0, 5, 2, 21, 5]. 
        100 = 50 = 25 in this example.

        len(scale) - 1 acts as a way to do some modulo arithmatic whose base is
        a dynamically determined value. 
        '''
        if(data is None or len(data) == 0): 
            return -1
        for i in range(len(data)):
            while(data[i] > len(scale) - 1):
                data[i] -= len(scale) - 1
        return data

    # Maps letters to index numbers
    def mapLettersToNumbers(self, letters):
        '''
        Maps letters to index numbers, which
        will then be translated into notes (strings).

        NOTE: Need to account for capitalization!!
        '''
        if(letters is None): return -1
        numbers = []
        # Pick a letter
        for i in range(len(letters)):
            # Search alphabet
            for j in range(len(self.alphabet)):
                # If we get a match, store that index number
                '''NOTE: Find a way to account for capitalization! '''
                if(letters[i] == self.alphabet[j]):
                    numbers.append(i)
        if(numbers is None):
            return -1
        return numbers
    
    #Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        if(scale is None):
            return -1
        k = 5
        minorScale = []
        for i in range(len(scale)):
            minorScale.append(scale[k])
            k += 1
            if(k > len(scale) - 1):
                k = 0
        if(minorScale is None):
            return -1
        return minorScale


    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo between 40-208bpm.
        Returns a float upon success, 60.0 if fail.
        '''
        print("\nPicking tempo...")
        tempo = 0.0
        tempo = self.tempos[randint(0, len(self.tempo) - 1)]
        if (not tempo):
            return 60.0
        return tempo


    #-------------------------------------------------------------------------------#
    #-------------------------------------Pitch-------------------------------------#
    #-------------------------------------------------------------------------------#


    # Picks which key (scale) to use. 
    def pickKey(self):
        '''
        Picks which key (scale) to use. 
        Returns a list of pitch classes without specified octaves.

        For minor scales, feed the output of this into convertToMinor()
        '''
        scale = []
        scale = self.scales[randint(1, 12)]
        return scale

    # Converts a given integer to a pitch in a specified octave (ex C#6)
    def newNote(self, num, scale, octave):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6).
        Requires an integer, a given scale, and the required octave. 
        Returns a single string.
        '''
        if(num > len(scale) - 1):
            return -1
        if(octave < 1 or octave > 8):
            return -1
        newNote = scale[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote

   #Generate a series of notes based off an inputted array of integers
    def newNotes(self, data, isMinor):
        '''
        Generate a series of notes based on inputted data (an array of integers)
        This randomly picks the key and the starting octave! 

        NOTE:
            Long data sets will have the same note associated with different 
            values elsewhere in the array. 
            
            If we ascend through the available octaves we can pick a new 
            key/scale and cycle through the octaves again. This will allow for 
            some cool chromaticism to emerge rather "organiclly" while minimizing
            the amount of repeated notes associated with different elements in 
            the data array (unless we get the same scale chosen again, or there's
            a lot of common tones between the scales that are picked).  
        '''
        if(data is None):
            return -1

        notes = []

        # Pick starting octave (2 or 3)
        octave = randint(2, 3)
        octStart = octave

        # Pick key/scale
        scale = self.scales[randint(1, 12)]

        # Will this be a minor scale?
        if(isMinor == True):
            scale = self.convertToMinor(scale)

        #Display choices
        if(isMinor == True):
            print("\nGenerating", len(data), "notes starting in the key of", scale[0], "minor")
        else:
            print("\nGenerating", len(data), "notes starting in the key of", scale[0], "major")

        # Generate notes
        for i in range(len(data)):
            note = scale[data[i]]
            note = "".format(note, octave)
            notes.append(note)
            # If we've reached the end of the scale,
            # increment the octave (until octave 8)
            # Ideally trigger this condition every
            # 7 iterations. 
            if(i % 7 == 0):
                octave += 1
                # If we reach highest octave, reset
                # to original starting point and pick
                # a new scale to chose from
                if(octave > 8):
                    octave = octStart
                    scale = self.scales[randint(1, 12)]
                    if(isMinor == True):
                        scale = self.scaleTheScale(scale)
                        print("Key-change! Now using", scale[0], "minor")
                    else:
                        print("Key-change! Now using", scale[0], "major")
        return notes


    # Generate a series of notes based off an array of letters
    def newNotesFromLetters(self, name, minor):
        '''
        Generate a scale based on the letters from a name (or any random array of letters)
        '''
        if(name is None):
            return -1
        # Pick key, then generate 25 note scale (multiple octaves) from this root. 
        # Account for Whether this is a major or minor scale!

        # if(minor == True):

        # else:


    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#


    #Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        return rhythm

    #Pick a fast duration
    def newRhythmFast(self):
        '''
        Generate a single new fast rhythm
        '''
        rhythm = self.rhythmsFast[randint(0, len(self.rhythmsFast) - 1)]
        return rhythm
    
    #Pick a slow duration
    def newRhythmSlow(self):
        '''
        Generate a single new slow rhythm
        '''
        rhythm = self.rhythmsSlow[randint(0, len(self.rhythmsSlow) - 1)]
        return rhythm

    #Generate a list containing a rhythmic pattern
    def newRhythms(self, total):
        '''
        Generate lists of 2-20 rhythms to be used as a 
        melody/ostinato/riff/whatever. Uses infrequent repetition.
        '''
        rhythms = []
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            #Pick rhythm and add to list    
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            #Repeat this rhythm or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                #Limit reps to no more than 1/3 of the total no. of rhythms
                limit = math.floor(len(rhythms)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit) 
                for i in range(reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == total):
                        break
            else:
                if(rhythm not in rhythms):
                    rhythms.append(rhythm)

            print("Total:", len(rhythms))

        if(not rhythms):
            print("...Unable to generate pattern!")
            return -1
        return rhythms


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    #Generate a single dynamic (to be used such that a passage doesn't have consistenly
    #changing dynamics)
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        dynamic = self.dynamics[randint(0, len(self.dynamics) - 1)]
        return dynamic

    #Generate a soft dynamic
    def newDynamicSoft(self):
        '''
        Generates a single soft dynamic
        '''
        dynamic = self.dynamicsSoft[randint(0, len(self.dynamicsSoft) - 1)]
        return dynamic

    #Generate a medium dynamic
    def newDynamicMed(self):
        '''
        Generates a single medium dynamic
        '''
        dynamic = self.dynamicsMed[randint(0, len(self.dynamicsMed) - 1)]
        return dynamic

    #Generate a loud dynamic.
    def newDynamicLoud(self):
        '''
        Generates a single loud dynamic
        '''
        dynamic = self.dynamicsLoud[randint(0, len(self.dynamicsLoud) - 1)]
        return dynamic

    #Generate a list of dynamics. 
    def newDynamics(self, total):
        '''
        Generates a list of dynamics (MIDI velocites). Total supplied from elsewhere.
        Uses infrequent repetition. Returns -1 if unable to generate a list.
        '''
        dynamics = []
        print("\nGenerating", total, "semi-reapeating dynamics...")
        while(len(dynamics) < total):
            #Pick dynamic    
            dynamic = self.dynamics[randint(0, 9)]
            #Repeat this dynamic or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                #Limit reps to no more than 1/3 of the supplied total
                limit = math.floor(total/3)
                '''Note: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit) 
                for i in range(reps):
                    dynamics.append(dynamic)
                    if(len(dynamics) == total):
                        break
            else:
                if(dynamic not in dynamics):
                    dynamics.append(dynamic)
        if(not dynamics):
            print("...Unable to generate pattern!")
            return -1
        return dynamics



    #--------------------------------------------------------------------------------#
    #--------------------------------------Chords------------------------------------#
    #--------------------------------------------------------------------------------#


    #Generates a progression from the notes of a given scale
    def newChordsFromScale(self, scale):
        '''
        Generates a progression from the notes of a given scale.
        Returns -1 if recieving bad input, and -2 if generation was unsuccessfull
        
        NOTE: Chords will be derived from the given scale ONLY! Could possibly
              add more randomly inserted chromatic tones to give progressions more
              variance and color. 
        '''
        if(scale is None):
            return -1
        print("\nGenerating chords from a given scale...")
        print("Given scale:", scale)
        #How many chords?
        chords = []
        total = randint(3, 10)
        # total = randint(3, len(scale) - 1)
        print("\nGenerating", total, "chords...")
        #Pick notes
        while(len(chords) < total):
            chord = []
            #How many notes in this chord?
            totalNotes = randint(2, 7)
            while(len(chord) < totalNotes):
                # Pick note
                note = scale[randint(0, len(scale) - 1)]
                # Add if not already in list
                if(note not in chord):
                    chord.append(note)
                elif(note in chord and len(chord) > 2):
                    break
            chords.append(chord)
        if(not chords):
            print("...Unable to generate chords!")
            return -2
        print("\nTotal chords:", len(chords))
        print("Chords:", chords)
        return chords


    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    #Generate a melody. 
    def newMelody(self, data, isMinor):
        '''
        Picks a tempo, notes, rythms, and dynamics. Rhythms and dynamics are picked randomly (total
        for each is len(data), notes come from user. Should (ideally) handle either a character
        array for a person's name (or any random set of characters), or an array of integers
        of n length.

        Appends to pretty_midi object and returns new MIDI object and exports a MIDI file.

        Returns a newMelody() object.
        '''
        isLetters = False
        # Melody container object
        newMelody = melody()

        #------------------Process incoming data-----------------#
       
        print("\nProcessing incoming data...")

        '''
        Is this a character array, integer array, or array of floats?
        Need a boolean to remember whether we're using a character array
        or an integer array.

        If floats, convert to ints, then scale
        '''

        #-----------------------Generate!------------------------#
        
        print("\nGenerating melody...")

        # Pick tempo
        newMelody.tempo = self.newTempo()
        # Pick notes
        newMelody.notes = self.newNotes(data, isMinor)
        # Pick rhythms
        newMelody.rhythms = self.newRhythms(len(data) - 1)
        # Pick dynamics
        newMelody.dynamics = self.newDynamics(len(data) - 1)

        #-----------Check data and export to MIDI file------------#

        print("\nChecking results...")

        # Make sure all data was inputted
        if(newMelody.hasData() == False):
            print("ERROR: missing melody data!")
            return -1

        #Add data to MIDI object and write out file.
        if(mid.saveMelody(self, newMelody) == -1):
            print("ERROR: unable to export melody!")
            return -1

        #--------------------Display results----------------------#

        print("\nRESULTS:")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

        return newMelody