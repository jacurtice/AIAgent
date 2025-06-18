import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function, available_functions

def main():

    args = sys.argv[1:]
    if not args:
        print("Usage: python main.py 'Command prompt'")
        sys.exit(1)

    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")

    load_dotenv()

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    MAX_LOOPS = 20
    loop_count = 0
    function_called = True
    while loop_count < MAX_LOOPS and function_called:
        loop_count += 1

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls:
            print("No function calls detected.")
            print("Final response text:", response.text)
            function_called = False
        else:
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception(f"Function {function_call_part.name} returned None")
                elif verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
                
            messages.append(types.Content(role="tool", parts=function_responses))




if __name__ == "__main__":
    main()


