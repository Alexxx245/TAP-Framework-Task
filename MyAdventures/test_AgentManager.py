import sys
import os
from unittest.mock import MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from AgentManager import AgentManager, SpecificAgent

"""Class to test the AgentManager functions"""
class TestAgentManager:

    def test_register_agents(self):
        manager = AgentManager()
           
        agent = MagicMock()
        manager.register(agent)
        assert agent in manager.agents

    # def test_start_specific_agent(self):
    #     manager = AgentManager()
       
    #     agent1 = MagicMock()
    #     manager.register(agent1)

    #     manager.start(0)
    #     agent1.start.assert_called_once()
    
    # def test_start_all_agents(self):
    #     manager = AgentManager()
       
    #     agent1 = MagicMock()
    #     agent2 = MagicMock()
    #     manager.register(agent1)
    #     manager.register(agent2)

    #     manager.start_all()
    #     agent1.start.assert_called_once()
    #     agent2.start.assert_called_once()

    def test_stop_specific_agent(self):
        manager = AgentManager()
       
        agent1 = MagicMock()
        manager.register(agent1)

        manager.stop(0)
        agent1.stop.assert_called_once()
        

    def test_stop_all_agents(self):
        manager = AgentManager()
       
        agent1 = MagicMock()
        agent2 = MagicMock()
        manager.register(agent1)
        manager.register(agent2)

        manager.stop_all()
        agent1.stop.assert_called_once()
        agent2.stop.assert_called_once()

    def test_kill_specific_agent(self):
        manager = AgentManager()
       
        agent1 = MagicMock()
        manager.register(agent1)

        manager.kill(0)
        agent1.stop.assert_called_once()
        assert agent1 not in manager.agents

    def test_kill_all_agents(self):
        manager = AgentManager()
        agent1 = MagicMock()
        agent2 = MagicMock()

        manager.register(agent1)
        manager.register(agent2)

        manager.kill_all()
        assert len(manager.agents) == 0
    
"""Class to test the SpecificAgent functions"""
class TestSpecificAgent:
     
    # def test_start_puts_currentActivity_on_true(self):
    #     with patch("AgentManager.Minecraft.Minecraft.create"):
    #         agent = SpecificAgent("Agent1")
    #         agent.run = MagicMock() 
    #         agent.start()
    #         assert agent.currentActivity is True

    def test_stop_puts_currentActivity_on_false(self):
        with patch("AgentManager.Minecraft.Minecraft.create"):
            agent = SpecificAgent("Agent1")
            agent.run = MagicMock() 
            agent.stop()
            assert agent.currentActivity is False

    def test_get_methods_returns_methods(self):
        with patch("AgentManager.Minecraft.Minecraft.create"):
            agent = SpecificAgent("Agent1")
            
            methods = agent.getMethods()

            assert "start" in methods
            assert "run" in methods
            assert "perform" in methods
            assert "stop" in methods
            assert "postToChat" in methods
            assert "getMethods" in methods
            
