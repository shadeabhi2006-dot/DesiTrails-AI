from parser import parse_user_prompt


prompts = [

    "I want a peaceful nature trip under ₹1000",

    "I want an adventurous trekking trip with lots of outdoor activities",

    "I love history, temples and cultural places",

    "I want a quiet beach with very few tourists",

    "I want a lively and popular destination",

    "I want a nature trip around ₹1500 that is easy to reach"

]


for prompt in prompts:

    print("\n--------------------------------")

    print("PROMPT:")
    print(prompt)

    print("\nPREFERENCES:")

    result = parse_user_prompt(prompt)

    print(result)