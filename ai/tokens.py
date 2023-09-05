import tiktoken

tkm = tiktoken.get_encoding("cl100k_base")

def precise_tokens_from_messages(messages, model):
    
    if "gpt-3.5" in model:
        tokens_per_message = 4
        tokens_per_name = -1
    else:
        tokens_per_message = 3
        tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        num_tokens += len(tkm.encode(message['content']))
        num_tokens += len(tkm.encode(message['role']))
        if message.get('name', '') != '':
            num_tokens += tokens_per_name

    num_tokens += 3
    return num_tokens

def token_count_single_message(message, model):

    if "gpt-3.5" in model:
        tokens_per_message = 4
        tokens_per_name = -1
    else:
        tokens_per_message = 3
        tokens_per_name = 1

    num_tokens = 0
    num_tokens += tokens_per_message
    num_tokens += len(tkm.encode(message['content']))
    num_tokens += len(tkm.encode(message['role']))
    if message.get('name', '') != '':
        num_tokens += tokens_per_name

    num_tokens += 3  # Adding the 3 additional tokens similar to the original function

    return num_tokens
