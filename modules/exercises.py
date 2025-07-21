# modules/exercises.py

MORNING_EXERCISES = [
    "5 минут легкой зарядки для пробуждения тела.",
    "Наклоны головы и вращение плечами.",
    "Дыхательные упражнения – глубокий вдох-выдох."
]

EVENING_EXERCISES = [
    "Растяжка спины и ног перед сном.",
    "Медленное дыхание и расслабление мышц.",
    "Легкие упражнения на шею и плечи."
]

async def get_morning_exercise():
    return MORNING_EXERCISES[0]

async def get_evening_exercise():
    return EVENING_EXERCISES[0]
