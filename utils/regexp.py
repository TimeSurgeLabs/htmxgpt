import re

def replace_code_blocks(text):
    # The regex pattern to find the code block
    # It uses capturing groups to capture the language and code content
    pattern = r"```([a-zA-Z0-9]+)\n(.*?)```"

    # The replacement function
    def repl(m):
        language = m.group(1)
        code_content = m.group(2)
        return f'<pre><code class="{language}">{code_content}</code></pre>'
    
    # Perform the replacement
    return re.sub(pattern, repl, text, flags=re.DOTALL)

def escape_lt_gt_inside_code_tags(text):
    # The regex pattern to find code tags
    pattern = r'<pre><code class="([a-zA-Z0-9]+)">([^<>]+)</code></pre>'

    # The replacement function
    def repl(m):
        language = m.group(1)
        code_content = m.group(2)
        # Escape '<' and '>' within the code content
        code_content = code_content.replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="language-{language}">{code_content}</code></pre>'

    # Perform the replacement
    return re.sub(pattern, repl, text)
