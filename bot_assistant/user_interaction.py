from abc import ABC, abstractmethod
from rich import print as rprint

 
class UserInterAbstract(ABC):
    @abstractmethod
    def user_input(inp_holder):
        pass
    
    @abstractmethod
    def user_output(output_info):
        pass


class ConsoleInteraction(UserInterAbstract):
    def user_input(inp_holder):
        user_inp = input(inp_holder)
        return user_inp
    
    def user_output(output_info, richprint=False):
        if richprint == True:
            rprint(output_info)
        else:
            print(output_info)