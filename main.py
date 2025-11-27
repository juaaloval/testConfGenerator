import yaml
import argparse
from utils.config_loader import ConfigLoader
from models.llm_factory import LLMFactory
from parsers.oas_parser import OASParser
from parsers.testconf_parser import TestConfParser
from generators.test_value_generator import TestValueGenerator

def main():
    parser = argparse.ArgumentParser(description="RESTest Test Configuration Generator")
    parser.add_argument("--oas", required=True, help="Path to OAS specification file")
    parser.add_argument("--testconf", required=True, help="Path to initial TestConf file")
    parser.add_argument("--config", default="config.yaml", help="Path to configuration file")
    parser.add_argument("--output", default="extended_testconf.yaml", help="Output path for extended TestConf")
    
    args = parser.parse_args()
    
    # Load configuration
    config = ConfigLoader.load(args.config)
    print(f"Loaded configuration from {args.config}")
    
    # Initialize LLM
    print(f"Initializing LLM: {config['llm']['model_id']}...")
    try:
        llm = LLMFactory.create_llm(config['llm'])
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
        return

    # Parse inputs
    print("Parsing inputs...")
    try:
        oas_data = OASParser.parse(args.oas)
        testconf_data = TestConfParser.parse(args.testconf)
    except Exception as e:
        print(f"Failed to parse inputs: {e}")
        return
    
    # Generate values
    print("Generating test values...")
    generator = TestValueGenerator(llm)
    extended_conf = generator.generate(oas_data, testconf_data)
    
    # Save output
    print(f"Saving extended configuration to {args.output}...")
    TestConfParser.save(extended_conf, args.output)
    
    print("Done!")

if __name__ == "__main__":
    main()
