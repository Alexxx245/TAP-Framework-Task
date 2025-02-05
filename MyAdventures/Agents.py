import AgentManager
from mcpi import block as Block
import random

""" Agent that relates the AgentManager with Minecraft Chat,
    allowing to register, list and kill agents directly using commands on the Minecraft chat """
class CommandLineAgent(AgentManager.SpecificAgent):

    def __init__(self, name, manager, list_agents):
        super().__init__(name,)
        self.manager = manager
        self.agent_list = list_agents

    def perform(self):
        chat = self.mc.events.pollChatPosts()
        for command in chat:
                w = command.message.split()
                if (w[0] == "#agent"):
                    match (w[1]):

                        case "register":

                            if (len(w) < 3 or len(w) > 4):
                                self.postToChat("ERROR! You have to indicate: #agent register -agent_type -agent_name")
                            elif (w[2] == "list" and len(w) == 3):
                                self.postToChat("List of possible agent classes:")
                                for agent in self.agent_list:
                                    self.postToChat("Agent: " + agent.__name__)
                            elif (w[2] != "list" and len(w) == 3):
                                self.postToChat("ERROR! You have to indicate a name for the agent")

                            elif any(agent.__class__.__name__ == w[2] for agent in self.manager.agents):
                                self.postToChat("ERROR! This type of agent is already registered")
                            
                            else:                               
                                for agent in self.agent_list:
                                    if (agent.__name__ == w[2]):
                                        new = agent(w[3])            #Create a new agent with the name given
                                        self.manager.register(new)   #Register the new agent created
                                        new.start()                  #Start the thread of the new agent

                                        self.postToChat("You have registered " + agent.__name__ + ": " + w[3])

                        case "list":
                            
                            #I applied functional programming to list the registered agents
                            self.postToChat("You have " + str(len(self.manager.agents)) + " agents:")
                            list(map(lambda agent: self.postToChat("Agent: " + agent.name + " [" + type(agent).__name__ + "]"), self.manager.agents))

                        case "kill":

                            if (len(w) < 3):
                                self.postToChat("ERROR! You have to indicate: #agent kill -agent_name")
                            elif (w[2] == self.name):
                                self.postToChat("ERROR! You can't kill the Manager Agent")
                            elif (w[2] == "all"):

                                #I applied functional programming to kill all agents except the Manager Agent using filter
                                #and then using sum to get the amunt of agents killed to post after on the Minecraft chat
                                agents_to_kill = list(filter(lambda agent: agent.name != self.name, self.manager.agents))

                                killed_count = 0
                                for agent in agents_to_kill:
                                    if agent:
                                        self.manager.kill(self.manager.agents.index(agent))
                                        killed_count += 1
                                self.postToChat("You have killed " + str(killed_count) + " agent(s)")
                            else:
                                agent = next((a for a in self.manager.agents if a.name == w[2]), None)
                                if agent:
                                    self.manager.kill(self.manager.agents.index(agent))
                                    self.postToChat("You have killed " + agent.name + " agent")
                                else:
                                    self.postToChat("Agent: " + w[2] + " not found")

                        case "methods":

                            if len(w) < 3:
                                self.postToChat("ERROR! You have to indicate: #agent methods -agent_name")
                            else:
                                agents = self.manager.agents.copy()
                                agent_found = False
                                for agent in agents:
                                    if agent.name == w[2]:
                                        methods = agent.getMethods()                               
                                        self.postToChat("Methods of " + agent.name + ": " + ",".join(methods))
                                        agent_found = True
                                        break
                                if not agent_found:
                                    self.postToChat("Agent: " + w[2] + " not found")

                        case "help":

                            self.postToChat("Manager commands: Use #agent before any command")
                            self.postToChat(" -> register -agent_type -agent_name: registers and activates a new agent from a set list")
                            self.postToChat(" -> register list: returns the list of possible agents")
                            self.postToChat(" -> list: returns the list of current activate agents registered")
                            self.postToChat(" -> kill: stops an active agent and remove it from the list")
                            self.postToChat(" -> kill all: stops and removes all active agents from the list")
                            self.postToChat(" -> methods -agent_name: returns the methods of the agent")

                        case _:                            
                            self.postToChat("Unknown command, use #agent help to see the available commands")


""" Agent that spawns TNT(s) above the player when a certain message is posted to chat """
class TNTAgent(AgentManager.SpecificAgent):
    
    def perform(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            words = message.message.split()

            if words[0] == "TNT":
                # to control the number of TNT(s) that will spawn, if the user doesn't put a number, only 1 TNT will be spawned
                num_tnt = int(words[1]) if len(words) > 1 and words[1].isdigit() and int(words[1]) > 0 else 1
                
                self.postToChat("Placing" + str(num_tnt) + " TNT above you!!")
                pos = self.mc.entity.getTilePos(message.entityId)

                for i in range(num_tnt):

                    self.mc.setBlock(pos.x, pos.y + 3 + i, pos.z, Block.TNT)
                    # to activate Redstone in the last TNT
                    self.mc.setBlock(pos.x, pos.y + 3 + num_tnt, pos.z, 152)
                    #to clean the block above the Redstone
                    self.mc.setBlock(pos.x, pos.y + 3 + num_tnt, pos.z, Block.AIR)


""" Agent that insults players when certain messages are post to chat """
class InsultAgent(AgentManager.SpecificAgent):

    bad_words = ["You smell bad!", "You're a noob!", "You're a loser!", "You sucks!"]
    def perform(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            if (message.message == "Insult me"):
                self.mc.postToChat(random.choice(self.bad_words))


""" Agent that plants trees and flowers when certain messages are post to chat """
class GardenerAgent(AgentManager.SpecificAgent):
    
    def perform(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            pos = self.mc.entity.getTilePos(message.entityId)

            if (message.message == "Plant tree"):

           # to build the trunk of the tree
                for i in range(3):
                    self.mc.setBlock(pos.x+2,pos.y + i, pos.z, 17) #id 17 is for the wood block

            # to build the leaves of the tree
                for dx in range(-2, 3):
                    for dz in range(-2, 3):
                        if abs(dx) + abs(dz) < 3:
                            self.mc.setBlock(pos.x+2 + dx, pos.y + 3, pos.z + dz, 18) #id 18 is for the leaves block

            #to plant a yellow flower
            elif (message.message == "Plant flower"):
                self.mc.setBlock(pos.x + 2, pos.y, pos.z, 37) #id 37 is for the yellow flower


""" Agent that builds a house when a certain message is post to chat """
class  BuilderAgent(AgentManager.SpecificAgent):

    def perform(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            pos = self.mc.entity.getTilePos(message.entityId)

            if (message.message == "Build house"):

                # Build walls
                for i in range(5):
                    for j in range(5):
                        self.mc.setBlock(pos.x + i, pos.y, pos.z + j, 1)  # Stone floor
                        self.mc.setBlock(pos.x + i, pos.y + 1, pos.z + j, 4)  # Cobblestone walls
                        self.mc.setBlock(pos.x + i, pos.y + 2, pos.z + j, 4)

                # Build roof
                for i in range(5):
                    for j in range(5):
                        self.mc.setBlock(pos.x + i, pos.y + 3, pos.z + j, 5)  # Wooden roof

                        # Add Wooden door
                        self.mc.setBlock(pos.x + 2, pos.y, pos.z, 5)
                        self.mc.setBlock(pos.x + 2, pos.y + 1, pos.z, 5)
                        
if __name__ == "__main__":
    manager = AgentManager.AgentManager()
    manager.register(CommandLineAgent("AgentManager", manager, [TNTAgent, InsultAgent, GardenerAgent, BuilderAgent]))   #register the AgentManager and the list of the possible agents
                                                                                                                        #that we want register on Minecraft
    manager.start_all()   #start a thread for every agent we register