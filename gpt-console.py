# -*- coding: utf-8 -*-
import kbsChat
import apiManager
import json

# Main function that runs the chatbot
def main():
    init_promote = """
    我希望你担任投资理财助理，并想出创造性的方法来管理财务。在为客户制定财务计划时，您需要考虑预算、投资策略和风险管理，
    以帮助他们实现利润最大化。
    客户在向你提问时，通常将附加上实时金融指标数据以及一些股票基金等证券市场数据给你做参考，你将根据这些参考数据来回答用户提问。
    """

    message_log = [
        {"role": "system", "content": init_promote}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    # Start a loop that runs until the user types "quit"
    while True:
        if first_request:
            # If this is not the first request, get the user's input and add it to the conversation history
            user_input = input("You: ")

            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            api_calls_txt = kbsChat.generate_api_calls(user_input)
            formatted_api_calls_txt = apiManager.format_api_calls(api_calls_txt)
            print(f"AI assistant: {formatted_api_calls_txt}")

            response = kbsChat.chat_with_gpt(message_log, user_input, api_calls_txt)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

            print(f"AI assistant: {response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
