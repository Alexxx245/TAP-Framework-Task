import sys
import os
import pytest
from unittest.mock import MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from AgentManager import AgentManager
from Agents import *

@pytest.fixture
def mock_agent_manager():
    return AgentManager.AgentManager()


@pytest.fixture
def mock_mcpi():
    with patch("AgentManager.Minecraft.Minecraft.create") as mock_mc:
        yield mock_mc.return_value

class TestSpecificAgents:

    def test_command_line_agent_register_word(self, mock_agent_manager, mock_mcpi):
        
        # Simular mensaje de chat para registrar un agente
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent register TNTAgent tnt")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent])
        command_agent.perform()

        assert len(mock_agent_manager.agents) == 1
        assert mock_agent_manager.agents[0].name == "tnt"   #After writing in the Minecraft chat #agent register -agent_type -agent_name, 
                                                            #the agent should be registered with the same name and the lenght of the agents list will increment by 1                                                 

    def test_command_line_agent_list_word(self, mock_agent_manager, mock_mcpi):
        
        mock_agent_manager.register(TNTAgent("tnt"))
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent list")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent])
        command_agent.postToChat = MagicMock()
        command_agent.perform()

        command_agent.postToChat.assert_any_call("Agent: tnt [TNTAgent]")   #After writing in the Minecraft chat #agent list after registering an Agent, in the chat
                                                                            #should appear the name and the type of the agent registered

    def test_command_line_agent_kill_word(self, mock_agent_manager, mock_mcpi):
        
        mock_agent_manager.register(TNTAgent("tnt"))

        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent kill tnt")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent])
        command_agent.perform()

        assert len(mock_agent_manager.agents) == 0  #The lenght of the agents list after executing the kill command, should be decreased by 1 by every agent killed,
                                                    #but never will be 0 because you can't kill the Manager Agent

    def test_command_line_agent_kill_wordV2(self, mock_agent_manager, mock_mcpi):
        
        mock_agent_manager.register(TNTAgent("tnt"))
        mock_agent_manager.register(BuilderAgent("builder"))

        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent kill tnt")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent,BuilderAgent])
        command_agent.perform()

        assert len(mock_agent_manager.agents) == 1   #The lenght of the agents list after executing the kill command, should be decreased by 1 by every agent killed,                                                    

    def test_command_line_agent_kill_all_word(self, mock_agent_manager, mock_mcpi):
        
        mock_agent_manager.register(TNTAgent("tnt"))
        mock_agent_manager.register(BuilderAgent("builder"))
        mock_agent_manager.register(GardenerAgent("gardener"))
        mock_agent_manager.register(InsultAgent("insulter"))

        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent kill all")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent, BuilderAgent,GardenerAgent,InsultAgent])
        command_agent.perform()

        assert len(mock_agent_manager.agents) == 0   #The lenght of the agents list after executing the kill all command, 
                                                     #should kill all the registered agents
                                                     
    def test_command_line_agent_methods_word(self, mock_agent_manager, mock_mcpi):
        
        agent = TNTAgent("tnt")
        mock_agent_manager.register(agent)

        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="#agent methods tnt")
        ]

        command_agent = CommandLineAgent("Manager", mock_agent_manager, [TNTAgent])
        command_agent.postToChat = MagicMock()
        command_agent.perform()

        expected_methods = ",".join(agent.getMethods())
        command_agent.postToChat.assert_called_once_with("Methods of tnt: " + expected_methods)    #After executing the methods command indicating the agent,
                                                                                                   #should appear in the Minecraft chat the actual methods of the agent
                                                                                                   #In this case every agent has the same methods

    def test_tnt_agent_perform(self, mock_mcpi):
       
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="TNT")
        ]

        mock_mcpi.entity.getTilePos.return_value = MagicMock(x=0, y=0, z=0)

        tnt_agent = TNTAgent("TNTAgent")
        tnt_agent.mc = mock_mcpi

        tnt_agent.perform()

        mock_mcpi.setBlock.assert_any_call(0, 3, 0, Block.TNT)   #The perform function of TNTAgent should place x TNTs, being x the number that it's wanted 
                                                                 #and (is/are) placed 3 blocks above the current position of the player

    def test_insult_agent_perform(self, mock_mcpi):
        
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="Insult me")
        ]

        insult_agent = InsultAgent("Insulter")
        insult_agent.mc = mock_mcpi

        insult_agent.perform()

        mock_mcpi.postToChat.assert_called_once()
        args, _ = mock_mcpi.postToChat.call_args
        assert args[0] in InsultAgent.bad_words         #The perform function of InsultAgent should post a random message in the Minecraft chat
                                                        #from the list of bad words that has the agent

    def test_gardener_agent_perform_tree(self, mock_mcpi):
           
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="Plant tree")
        ]

        mock_mcpi.entity.getTilePos.return_value = MagicMock(x=20, y=20, z=20)

        gardener_agent = GardenerAgent("Gardener")
        gardener_agent.mc = mock_mcpi

        gardener_agent.perform()

        mock_mcpi.setBlock.assert_any_call(22, 20, 20, 17)  
        mock_mcpi.setBlock.assert_any_call(22, 23, 20, 18)     #The perform function indicating Plant tree of GardenerAgent should place a tree 2 blocks in front of the player 
                                                               #and leaves 3 blocks above the tree

    def test_gardener_agent_perform_flower(self, mock_mcpi):
           
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="Plant flower")
        ]

        mock_mcpi.entity.getTilePos.return_value = MagicMock(x=20, y=20, z=20)

        gardener_agent = GardenerAgent("Gardener")
        gardener_agent.mc = mock_mcpi

        gardener_agent.perform()

        mock_mcpi.setBlock.assert_any_call(22, 20, 20, 37)     #The perform function indicating Plant flower of GardenerAgent 
                                                               #should place a yellow flower 2 blocks in front of the player

    def test_builder_agent_perform(self, mock_mcpi):
       
        mock_mcpi.events.pollChatPosts.return_value = [
            MagicMock(message="Build house")
        ]

        
        mock_mcpi.entity.getTilePos.return_value = MagicMock(x=30, y=30, z=30)
        builder_agent = BuilderAgent("Builder")
        builder_agent.mc = mock_mcpi

        builder_agent.perform()

        mock_mcpi.setBlock.assert_any_call(30, 30, 30, 1)  
        mock_mcpi.setBlock.assert_any_call(32, 31, 30, 4) 
        mock_mcpi.setBlock.assert_any_call(31, 33, 32, 5)      #The perform function of BuilderAgent should build a house with 5x5 floor, 
                                                               #2 blocks high walls, a wooden roof and a wooden door of 2 blocks high

