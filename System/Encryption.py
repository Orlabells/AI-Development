import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

decoded = enc.decode([]) #Put Encrypted API HERE
