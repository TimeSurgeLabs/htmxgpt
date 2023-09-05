import re

def replace_code_blocks(text):
    # The regex pattern to find the code block
    # It uses capturing groups to capture the language and code content
    pattern = r"```([a-zA-Z0-9]+)\n(.*?)```"

    # The replacement function
    def repl(m):
        language = m.group(1)
        code_content = m.group(2).replace('\n', '<br/>')
        return f'<pre><code class="{language}">{code_content}</code></pre>'
    
    # Perform the replacement
    return re.sub(pattern, repl, text, flags=re.DOTALL)
