# modules/psychology.py

TIPS = [
    "Запиши три вещи, за которые благодарна сегодня.",
    "Практикуй осознанное дыхание 5 минут.",
    "Улыбнись себе в зеркало — это улучшит настроение.",
]

async def get_tip(short=False):
    return TIPS[0] if short else f"💡 Психологический совет:\n\n{TIPS[0]}"
