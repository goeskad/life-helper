import time
import financialAssistant
import gptAPIs


async def chat_with_gpt(message_log, user_input, output_queue):
    user_input = await financialAssistant.prepare_user_input(user_input, output_queue)
    message_log.append({"role": "user", "content": user_input})

    # Send the conversation history to the chatbot and get its response
    start_time = time.time()
    response = gptAPIs.invoke_gpt(message_log, use_stream=True)

    chunk_time = time.time() - start_time
    print("GPT call cost: " + str(chunk_time))
    await output_queue.put(response)
