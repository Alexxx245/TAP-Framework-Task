[![codecov](https://codecov.io/gh/Alexxx245/TAP-Framework-Task/graph/badge.svg?token=1WJWHS6F02)](https://codecov.io/gh/Alexxx245/TAP-Framework-Task)

## **DESCRIPTION OF THE PROJECT**

This project has the goal of implement a framework that executes code using Inversion Of Control on Minecraft.
My implementation of this task it is distributed on 4 important .py files.

- AgentManager.py is a file that contains 2 classes: AgentManager and SpecificAgent. 
  - AgentManager: Has a list of agents and methods to manage them and this class acts like the Minecraft Agent Framework.
  - SpecificAgent: Is the parent class of the agents that will be created, and contains methods to control them and one abstract method that every agent will implement on his way.
This class contains a method call getMethods() which uses reflective programming by using the introspection principle.

- Agents.py is a file that contains the classes of the agents that we want to create, in my case there's 5 classes (Agents). Each created Agent will implement on his way the perform method and uses the pollChatPosts() to read the chat:
  - **TNTAgent**: this agent implements the perform method by placing and exploding X number of TNTs being X the number of TNTs we want to spawn (if you don't specify a number, only 1 TNT will spawn above you)
He can do that because is used the `pollChatPosts()` method included on the mcpi module, and allows us to read the chat and executing the perform method when the phrase "TNT" is written.

  - **InsultAgent**: this agent basically posts on the Minecraft chat random bad words, that are predefinied on a list. He will insult you if you post on the chat `"Insult me"`.

  - **GardenerAgent**: this agent will plant a tree if you post on the chat "Plant tree" and he can build it by using 3 bocks of wood to build the trunk and above the last block it builds the leaves.
He can also plant a yellow flower by posting `"Plant flower"`

  - **BuilderAgent**: this agent will build you a non-functional house but at least the structure of it, he will do it by posting on the chat `"Build house"`. You can modify the ranges and the type of the materials as you want, be free to be creational.
  - **CommandLineAgent**: This is the main agent that relates the AgenManager with the Minecraft chat, allowing to register, list, kill agents directly using commands on the chat of the game. This class uses the methods of the AgentManager to manage the agents that will be registered. <br/>This Agent controlls the cycle of life of the other agents by using the Minecraft chat and write different commands:
> [!IMPORTANT]
> To use the different commands, always enter with #agent

1. register: you can do `register list` to know the available agents you can register or you can do `register -agent_type -agent_name`. Other type of message will return an error message.

2. list: you can know the actual agents that you have registered doing `list`

3. kill: you can do `kill -agent_name` to kill a specific agent, but the name could not be `"AgentManager"` or do `kill all` to kill all the agents that you have registered and also it show you how many agents did you kill. Otherwise it returns an error message.

4. methods: you can do `methods -agent_name` to know the methods of each agent (but in this case every agent has the same methods, it's only to add reflective programming). If you don't specify a name or an real name of a registered agent it returns an error message.

This agent uses functional programming on differents parts of his code because is a requirement of the task. Uses a lambda expression with a map to list the registered agents, uses a lambda expression with a filter to kill all agents except the own AgentManager, because he cannot die to keep the functionality of the program and also uses the Iterable sum method to count the number of agents that are killed.
> [!IMPORTANT]
> Is important to know that you cannot register various agents with the same type because I decided it this way, otherwise if you want to implement it, feel free.

## **HOW TO RUN IT**

> [!IMPORTANT]
> To prove the code you need to use the 1.12 version of Minecraft. You can use it installing TLauncher

- First execute on the terminal the StartServer.bat file (in case you are using Windows) if not check this repo to clone the correct OS version: https://github.com/orgs/AdventuresInMinecraft/repositories <br/>

- Run the Minecraft Server like this: <br/>
`cd AdventuresInMinecraft-PC` and then `.\StartServer.bat(sh/bat/command)` <br/>

- Then on Minecraft go to Multiplayer and add a server using localhost

- Once you are in game you need to execute the Agents.py file

- And now you can use the differents commands on the chat to prove this Agent framework, check #agent help to see the available commands

  
## **GUIDE OF CREATING AGENTS**

To create a new Agent, simply create a Class that inherits from SpecificAgent and implement the perform method which works like this: 
When you register an agent, it is added to the list of agents, and his thread will start, making him to be activated. And as long as the agent is still active (it is only desactivated if you kill him), his perform method will be executed.
So be creative on creating new Agents.

## **TESTING**<br/>

The other .py files are test of the functionality of the AgentManager and the specific Agents. This code has been tested using the pytest module and MagickMock.
