from ai.tokens import tkm

def split_file_by_tokens(content: str, token_limit: int) -> list[str]:
    '''Split a file into multiple parts, each within the token limit.'''
    current_part = ''
    current_token_count = 0
    parts = []
    for line in content.split('\n'):
        if current_token_count + len(tkm.encode(line)) > token_limit:
            parts.append(current_part)
            current_part = ''
            current_token_count = 0
        current_part += line + '\n'
        current_token_count += len(tkm.encode(line)) + 1
    if current_part != '':
        parts.append(current_part)
    return parts
