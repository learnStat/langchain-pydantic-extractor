
import argparse
from src.chain import build_chain
import datetime
import os
from dotenv import load_dotenv
load_dotenv(override=True )

test_input = [
    "We run our policy underwriting system on IBM z/OS. It's all COBOL, been running since the early 90s. Every night we kick off a batch job that pulls from DB2, runs through rating logic, and writes output files that downstream billing picks up in the morning. No real-time interface — everything is file-based handoffs.",
    "Our claims processing platform is PL/I on z/OS. It handles both online transactions during business hours through CICS and a nightly batch cycle for settlements. It calls out to three external systems — a fraud scoring service, a payment gateway, and an archival system. Been there about 25 years, heavily customized.",
    "We're running RPG on an IBM AS/400 — iSeries now technically. It's our core policy admin system. Agents interact with it in real time through green screen terminals. There's some integration with a third party print vendor but mostly self-contained. Management wants to modernize but nobody really knows what it all does anymore."
]


if __name__ == "__main__":
    chain, provider = build_chain()

    parser = argparse.ArgumentParser(description="Pydantic Output Parser using LangChain")
    parser.add_argument("--save", action="store_true", help="whether to save the output to a file instead of printing")
    args = parser.parse_args()

    if args.save:
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs/{provider}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_output.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"LLM Provider: {provider}\n\n")
            for idx, input_text in enumerate(test_input, start=1):
                f.write(f"\n ==== Input {idx} ====\n")
                result = chain.invoke({"system_description": input_text})
                f.write(str(result) + "\n")
        print(f"Output saved to {filename}")
    else:
        for idx, input_text in enumerate(test_input, start=1):
            print(f"\n ==== Input {idx} ====\n")
            result = chain.invoke({"system_description": input_text})
            print(result)

