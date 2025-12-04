import argparse
import os

from testconf_agent.graph import get_testconf_agent_graph


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('oas_path',
                      help='Path to the input OAS file (e.g., oas.yaml)')
  parser.add_argument('output_directory',
                      help='Path to the output directory for the generated files')
  args = parser.parse_args()

  if not os.path.exists(args.oas_path):
      print(f"Error: Input file '{args.oas_path}' does not exist.")
      return

  graph = get_testconf_agent_graph()

  graph.invoke(
      {"oas_path": args.oas_path, "output_directory": args.output_directory},
      config={"max_concurrency": 1}
  )


if __name__ == '__main__':
    main()
