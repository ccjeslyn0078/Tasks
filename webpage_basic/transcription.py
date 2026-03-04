import httpx

API_KEY = "75ebd84e2b4120c5fb80e8d2416a2b49fcbcb01c"


async def transcribe_audio(file_path):

    url = "https://api.deepgram.com/v1/listen"

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "audio/mp3"
    }

    with open(file_path, "rb") as f:
        audio = f.read()

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, content=audio)

    result = response.json()

    return result["results"]["channels"][0]["alternatives"][0]["transcript"]
