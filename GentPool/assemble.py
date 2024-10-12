import argparse
import os

import dotenv
from gentopia import chat
from gentopia.assembler.agent_assembler import AgentAssembler
from gentopia.output import enable_log
from gentopia.tools.google_search import GoogleSearch
from gentopia.tools.pdf_reader import PDFReader


def main():
    enable_log(log_level='info')
    dotenv.load_dotenv(".env")

    parser = argparse.ArgumentParser(description='Assemble an agent with given name.')
    parser.add_argument('name', type=str, help='Name of the agent to assemble.')
    parser.add_argument('--print_agent', action='store_true', help='Print the agent if specified.')

    args = parser.parse_args()
    agent_name = args.name
    print_agent = args.print_agent

    # check if agent_name is under directory ./gentpool/pool/
    if not os.path.exists(f'./gentpool/pool/{agent_name}'):
        raise ValueError(f'Agent {agent_name} does not exist. Check ./gentpool/pool/ for available agents.')

    agent_config_path = f'./gentpool/pool/{agent_name}/agent.yaml'

    assembler = AgentAssembler(file=agent_config_path)

    # # assembler.manager = LocalLLMManager()
    # print(f">>> Assembling agent {agent_name}...")
    agent = assembler.get_agent()

    if agent.name != agent_name:
        raise ValueError(f"Agent name mismatch. Expected {agent_name}, got {agent.name}.")

    chat(agent, verbose=print_agent)

def process_input(agent):
    print("Agent is ready. Type your query:")
    while True:
        user_input = input("User: ").strip()

        if "search" in user_input.lower():
            result = GoogleSearch()._run(user_input)
            print("Google Search Results:\n", result)

        elif "read pdf" in user_input.lower():
            filepath = user_input.split("read pdf", 1)[1].strip()
            result = PDFReader()._run(filepath)
            print("PDF Content:\n", result)

        elif user_input.lower() in ["quit", "exit"]:
            print("Exiting...")
            break
        else:
            chat(agent, verbose=print)

if __name__ == '__main__':
    main()
