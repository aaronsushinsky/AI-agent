import os
import argparse
from dotenv import load_dotenv
from google import genai
from prompts import *
from call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError

from google.genai import types
client = genai.Client(api_key=api_key)

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    candidate_history = []
    for i in range(20):
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt
            )
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata != None:
            if args.verbose == True:
                print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
                print("Response tokens: ", response.usage_metadata.candidates_token_count)
                print("User prompt: ", args.user_prompt)

            func_result_list =[]
            verbose = args.verbose    
            if response.function_calls is not None:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=verbose)
                    
                    if not function_call_result.parts:
                        raise Exception("Parts list is empty")
                    if function_call_result.parts[0].function_response is None:
                        raise Exception ("Function response is None")
                    if function_call_result.parts[0].function_response.response is None:
                        raise Exception ("No function result present")
                    func_result_list.append(function_call_result.parts[0])
                    
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=func_result_list))
            else:
                print(response.text)
                return

        else:
            raise RuntimeError
    print("Something went wrong: agent hit max iterations without a final response.")
    sys.exit(1)
if __name__ == "__main__":
    main()
