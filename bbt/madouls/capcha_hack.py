from openai import OpenAI


async def capcha_hack(image_url , type_code):

    print(image_url)
    
    client = OpenAI(
        api_key='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',
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="dots-studio/dots-3-note-preview:free",
        messages=[
            {"role": "user",
             'content':[
                {'type':'image_url','image_url':image_url},
                {'type':'text','text':f"give me just just the code => {type_code} )"}
            ]}
        ]
    )

    
    return((response.choices[0].message.content))