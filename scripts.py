from datacenter.models import Schoolkid, Lesson, Commendation, Mark, Chastisement
import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


COMMENDATIONS = [
    'Молодец!', 
    'Отлично!', 
    'Хорошо!', 
    'Гораздо лучше, чем я ожидал!', 
    'Ты меня приятно удивил!', 
    'Великолепно!', 'Прекрасно!', 
    'Ты меня очень обрадовал!', 
    'Именно этого я давно ждал от тебя!', 
    'Сказано здорово – просто и ясно!', 
    'Ты, как всегда, точен!', 
    'Очень хороший ответ!', 
    'Талантливо!', 
    'Ты сегодня прыгнул выше головы!', 
    'Я поражен!', 'Уже существенно лучше!', 
    'Потрясающе!', 'Замечательно!', 
    'Прекрасное начало!', 
    'Так держать!', 
    'Ты на верном пути!', 
    'Здорово!', 
    'Это как раз то, что нужно!', 
    'Я тобой горжусь!', 
    'С каждым разом у тебя получается всё лучше!', 
    'Мы с тобой не зря поработали!', 
    'Я вижу, как ты стараешься!', 
    'Ты растешь над собой!', 
    'Ты многое сделал, я это вижу!', 
    'Теперь у тебя точно все получится!'
]


def get_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('Ученик не найден')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников. Уточните ФИО')    


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points = 5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, subject_title):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        lesson = (
            Lesson.objects.filter(
                year_of_study=schoolkid.year_of_study,
                group_letter=schoolkid.group_letter,
                subject__title=subject_title,
            )
            .order_by("-date")
            .first()
        )
        if lesson:
            Commendation.objects.create(
                text=random.choice(COMMENDATIONS),
                created=lesson.date,
                schoolkid=schoolkid,
                subject=lesson.subject,
                teacher=lesson.teacher,
            )
        else:
            print('Предмет не найден')
