import json
from django.conf import settings


def generate_ai_guidance(conversation):
    """Uses OpenAI if configured, otherwise returns deterministic guidance."""
    if settings.OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            'You are a trauma-informed assistant guiding women in filing safety complaints. '
                            'Ask one clear, empathetic question at a time and extract structured data fields.'
                        ),
                    },
                    {'role': 'user', 'content': json.dumps(conversation)},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    latest = conversation[-1]['content'] if conversation else ''
    if 'location' not in latest.lower():
        return 'Please share where the incident happened (city/area and exact place if possible).'
    if 'time' not in latest.lower():
        return 'When did this incident happen? You can provide approximate date and time.'
    return 'Please describe what happened in your own words and mention any witnesses or evidence.'
