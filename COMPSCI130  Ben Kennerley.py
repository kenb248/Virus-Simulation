### COMPSCI 130, Semester 012019
### Project Two - Virus
import turtle
import random
import math
#used to infect 
class Virus:
    def __init__(self, colour, duration):
        self.colour = colour
        self.duration = duration
        
"""This class is responsible for moving and holding the location of each individual person
as well as implementing cures and infections to each individual person"""
class Person:
    def __init__(self, world_size):
        self.world_size = world_size
        self.radius = 7
        turtle.colormode(255)
        """Following lines set random starting location and destination"""
        start_x_cord = random.randint(-(self.world_size[0] / 2)+7, (self.world_size[0] / 2)-7)
        start_y_cord = random.randint(-(self.world_size[1] / 2)+7, (self.world_size[1] / 2)-7)
        self.location = (start_x_cord, start_y_cord)
        self._get_random_location()
        
    """random locations are used to assign a destination for the person
    Coordinates are gotten in terms of world size so that if world size changes the person will still be in bounds of world"""
    def _get_random_location(self):
        x_cord = random.randint(-(self.world_size[0] / 2)+7, (self.world_size[0] / 2)-7)
        y_cord = random.randint(-(self.world_size[1] / 2)+7, (self.world_size[1] / 2)-7)
        self.destination = (x_cord, y_cord)
 
    """used to initially draw the person at the start of the simulation"""
    def draw(self):
        turtle.penup()
        turtle.goto(self.location)
        turtle.dot((self.radius * 2))

    """returns true if the distance between self and other is less than the diameter"""
    def collides(self, other):
        distance = math.sqrt(((self.location[0] - other[0])**2) + ((self.location[1] - other[1])**2)) #gives the distance between the current person and the current infected person
        if distance <= (self.radius*2):
            return True
        else:
            return False
        pass

    """given a list of infected people, returns True if the current non infected person is touching
    someone who is infected.""" 
    def collision_list(self, list_of_others):
        for i in list_of_others: #list_of_others is a list containing the positon of all infected people
            is_touching = self.collides(i)
            if is_touching == True:
                return True
            elif is_touching ==False:
                pass
        pass

    """infect a person with the virus"""
    def infect(self, virus):
        self.duration = virus.duration
        self.hours_sick = 0 #keeps track of how long a person has been infected
        pass

    """returns true if person is one radius within destination"""
    def reached_destination(self):
        if turtle.distance(self.destination) <= self.radius:
            self.reached_point = True
        else:
            self.reached_point = False
        pass

    """increase hours of sickness, check if duration of virus is reached.  If the
    duration is reached then the person is cured."""
    def progress_illness(self):
        if self.hours_sick == self.duration:
            return True
        else:
            self.hours_sick += 1
            return False   

    """Updates the person each hour.
     - moves each person by calling the move method
     - if the destination is reached then set a new destination"""
    def update(self):
        self.move()
        self.reached_destination()
        if self.reached_point == True: #sets new destination when current one reached
            self._get_random_location()
        
    """moves person towards the destination"""
    def move(self):
        turtle.penup()
        turtle.goto(self.location)
        turtle.seth(turtle.towards(self.destination))
        turtle.forward((self.radius / 2)) 
        turtle.dot((self.radius * 2))
        self.location = turtle.position()
        pass

"""This class is responsible for everything as a whole in the simulation ie. manages every person but doesn't
have the specific details of each person, also manages implementing infections and cures"""
class World:
    def __init__(self, width, height, n):
        """variables relating to people in the simulation"""
        self.people = [] #list holding all the people in the simulation
        self.person_count = 1 #used to differintiate between people in the simulation
        self.list_of_infected = [] #list which will contain all infected people
        self.number_of_people = n   #is the number of people in the simulation
        self.add_person()
        self.position_of_infected = []
        """Msc variables relating to setup"""
        self.base = turtle.Pen() #making the frame with a seperate turtle so that it only gets drawn once to save time
        self.base.hideturtle()  
        turtle.clear()#so that when simulation resets, people from previous simulation are cleared correctly
        self.size = (width, height)
        self.hours = 0
 
        
    """Adds the number of people in the simulation to a list, note currently just a string representing a person
    not and instance of the person class yet"""
    def add_person(self):
        for i in range(self.number_of_people):
            person = "p" + str(self.person_count) #this way each person unique
            self.people.append(person)
            self.person_count += 1

    """Choose a random person to infect and infect with a Virus"""
    def infect_person(self):
        person_to_infect = random.choice(self.people)
        if person_to_infect not in self.list_of_infected: #ensures someone who is already infected isn't infected again
            self.list_of_infected.append(person_to_infect)
            self.people.remove(person_to_infect)
        else:
            self.infect_person() 
        self.virus_colour = (255,0,0)
        self.virus = Virus(self.virus_colour, 50)#the second input value of the class Virus is the virus duration
        self.list_of_infected[self.list_of_infected.index(person_to_infect)].infect(self.virus)
        
    """Remove all infections from all people"""
    def cure_all(self):
        for i in self.list_of_infected:
            self.people.append(i)
        self.list_of_infected.clear()


    #def update_infections_slow(self):
        #not needed as this is covered in the simulate method
        #pass
        
    #Part D make the collision detection faster
    #def update_infections_fast(self):
        #pass
                    
    """Simulate an hour in the simulation
    #- increase hours passed.
    #- update all peoples location
    #- update all infection transmissions
    #- progress's illness"""
    def simulate(self):
        turtle.clear()
        self.position_of_infected.clear()
        self.hours += 1
        for i in self.list_of_infected: #updates all infected people
            turtle.pencolor(self.virus_colour)
            not_ill = i.progress_illness()#progresses the illness
            if not_ill == True: #cures person if duration of illness has been reached
                self.list_of_infected.remove(i)
                self.people.append(i)
            elif not_ill == False:
                i.update()
                self.position_of_infected.append(i.location)
            
        for i in self.people:#updates all healthy people
            turtle.pencolor(0,0,0)
            i.update()
            """following code is for collision detection"""
            got_infected = i.collision_list(self.position_of_infected)
            if got_infected == True:
                self.people.remove(i)
                self.list_of_infected.append(i)
                i.infect(self.virus)
        turtle.update()

    """Draws the world:
        - draw the box that frames the world
        - write the number of hours and number of people infected at the top of the frame"""
    def draw(self):
        self.base.penup()
        #In terms of self.size so that if the size of the world changed the frame would scale with it
        if self.hours == 0:#only drawn at start of simulation doesn't need to be drawn each hour/tick
            self.base.goto(-(self.size[0] / 2), (self.size[1] / 2))
            self.base.pendown()
            self.base.goto((self.size[0] / 2), (self.size[1] / 2)) 
            self.base.goto((self.size[0] / 2), -(self.size[1] / 2))
            self.base.goto(-(self.size[0] / 2), -(self.size[1] / 2))
            self.base.goto(-(self.size[0] / 2), (self.size[1] / 2))
            for i in range(len(self.people)):
                self.people[i] = Person(self.size) #for each person in the list of people creates an instance of the class for them
                self.people[i].draw()#

        """Following code for updating hours and infected count in simulation"""
        turtle.goto(-(self.size[0] / 2), (self.size[1] / 2))
        turtle.write("Hours " + str(self.hours))
        turtle.goto(-20, self.size[1]/2)
        turtle.write("Infected " + str(len(self.list_of_infected))) #since all infected people in a list the length of the list is the count of infected    
        turtle.update()

    
#---------------------------------------------------------
#Should not need to alter any of the code below this line
#---------------------------------------------------------
class GraphicalWorld:
    """ Handles the user interface for the simulation

    space - starts and stops the simulation
    'z' - resets the application to the initial state
    'x' - infects a random person
    'c' - cures all the people
    """
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.TITLE = 'COMPSCI 130 Project One'
        self.MARGIN = 50 #gap around each side
        self.PEOPLE = 50 #number of people in the simulation
        self.framework = AnimationFramework(self.WIDTH, self.HEIGHT, self.TITLE)
        
        self.framework.add_key_action(self.setup, 'z') 
        self.framework.add_key_action(self.infect, 'x')
        self.framework.add_key_action(self.cure, 'c')
        self.framework.add_key_action(self.toggle_simulation, ' ') 
        self.framework.add_tick_action(self.next_turn)
        
        self.world = None

    def setup(self):
        """ Reset the simulation to the initial state """
        print('resetting the world')        
        self.framework.stop_simulation()
        self.world = World(self.WIDTH - self.MARGIN * 2, self.HEIGHT - self.MARGIN * 2, self.PEOPLE)
        self.world.draw()
        
    def infect(self):
        """ Infect a person, and update the drawing """
        print('infecting a person')
        self.world.infect_person()
        #self.world.draw()#this isn't included so that if the simulation is paused and this function is executed the count of infected won't
        #overlap with the existing count and it means the changes take place in the next tick of the simulation

    def cure(self):
        """ Remove infections from all the people """
        print('cured all people')
        self.world.cure_all()
        #self.world.draw() #this isnt inclued so that if the simulation is paused and this function is executed the count of infected won't
        #overlap with the existing count and it means the changes take place in the next tick of the simulation

    def toggle_simulation(self):
        """ Starts and stops the simulation """
        if self.framework.simulation_is_running():
            self.framework.stop_simulation()
        else:
            self.framework.start_simulation()           

    def next_turn(self):
        """ Perform the tasks needed for the next animation cycle """
        self.world.simulate()
        self.world.draw()
        
## This is the animation framework
## Do not edit this framework
class AnimationFramework:
    """This framework is used to provide support for animation of
       interactive applications using the turtle library.  There is
       no need to edit any of the code in this framework.
    """
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 1 #smallest delay is 1 millisecond      
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.tracer(0, 0) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        turtle.setundobuffer(None)
        turtle.hideturtle() #prevent turtle appearance
        self.__animation_loop()

    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def simulation_is_running(self):
        return self.simulation_running
    
    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func):
        self.tick = func

    def __animation_loop(self):
        try:
            if self.simulation_running:
                self.tick()
            turtle.ontimer(self.__animation_loop, self.delay)
        except turtle.Terminator:
            pass


gw = GraphicalWorld()
gw.setup()
turtle.mainloop() #Need this at the end to ensure events handled properly
