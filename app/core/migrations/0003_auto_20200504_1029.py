# Generated by Django 3.0.5 on 2020-05-03 10:29
import os
import sys
import logging
import json
from django.db import migrations
from dateutil.parser import parse


logger = logging.getLogger(__name__)


def people_details_preprocessing(**people_details):
    people_dict = dict()
    people_dict['pid'] = people_details.get('_id')

    people_dict['index'] = people_details.get('index', -1)
    if people_dict['index'] < 0:
        logger.info("pid: {} without an index.\n".format(people_dict['pid']))
        logger.info(people_details)

    people_dict['guid'] = people_details.get('guid')
    has_died_str = people_details.get('has_died')
    people_dict['has_died'] = True if "True"==has_died_str else False

    try:
        people_dict['balance'] = float(
            people_details.get('balance').replace("$", "").replace(",", "")
        )
    except:
        people_dict['balance'] = 0

    people_dict['picture'] = people_details.get('picture')

    try:
        people_dict['age'] = int(people_details.get('age'))
    except:
        people_dict['age'] = None

    people_dict['eye_color'] = people_details.get('eyeColor')
    people_dict['name'] = people_details.get('name')
    people_dict['gender'] = people_details.get('gender', 'female')

    try:
        people_dict['company'] = int(people_details.get('company_id'))
    except:
        logger.info("People: {} without a company with him.\n".format(people_dict['index']))

    people_dict['email'] = people_details.get('email')
    people_dict['phone'] = people_details.get('phone')

    try:
        address_list = people_details.get('address').strip().split(',')
        address_list = [seg.strip() for seg in address_list]
        people_dict['street_name'] = address_list[0]
        people_dict['suburb'] = address_list[1]
        people_dict['state'] = address_list[2]
        people_dict['postcode'] = int(address_list[3])
    except:
        pass

    people_dict['about'] = people_details.get('about')

    try:
        people_dict['registered'] = parse(people_details.get('registered'))
    except:
        logger.info("Index: {} has no registered date \n".format(people_dict['index']))

    people_dict['greeting'] = people_details.get('greeting')

    return people_dict


def get_people_friends_list(**people_details):
    friends_list = []
    friends_data = people_details.get('friends')

    if friends_data:
        for friend in friends_data:
            friends_list.append(friend['index'])

    return friends_list


def load_food_tag_people_data(apps, schema_editor):
    Food = apps.get_model("core", "Food")
    Tag = apps.get_model("core", "Tag")
    People = apps.get_model("core", "People")
    Company = apps.get_model("core", "Company")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fullpath = os.path.join(os.path.dirname(base_dir), 'resources/people.json')

    friends = dict()

    with open(fullpath, encoding='utf-8') as pfile:
        peoples_str = pfile.read()
        peoples_str = peoples_str.replace("true", '"True"').replace("false", '"False"')
        peoples = json.loads(peoples_str)

        for people in peoples:
            foods_objs = []
            tags_objs = []

            favourite_foods = people['favouriteFood']
            for food in favourite_foods:
                item, _ = Food.objects.get_or_create(name=food)
                foods_objs.append(item)

            people_tags = people['tags']
            for tag in people_tags:
                item, _ = Tag.objects.get_or_create(name=tag)
                tags_objs.append(item)

            people_details = people_details_preprocessing(**people)
            people_company, _ = Company.objects.get_or_create(
                index=people_details.get('company')-1
            )
            people_details.update( {'company': people_company} )

            print("-----------------------------------------------------\n")
            print("Processing People instance of index: {}\n".format(people_details['index']))
            people_obj, _ = People.objects.get_or_create(**people_details)
            for food in foods_objs:
                people_obj.foods.add(food.id)
            for tag in tags_objs:
                people_obj.tags.add(tag.id)
            people_obj.save()

            friends[people_obj.id] = get_people_friends_list(**people)

    # Updating friends list for all people objects
    print("-----------------------------------------------------\n")
    print("Updating people's friends' list ...\n")
    for key, values_list in friends.items():
        individual = People.objects.get(id=key)
        print("Updating friends' list of People index: {}\n".format(individual.index))
        for value in values_list:
            try:
                new_friend = People.objects.get(index=value)
                individual.friends.add(new_friend.id)
            except:
                logger.info("People with index of {} doesn't exist.\n".format(value))
                print("People with index of {} doesn't exist.\n".format(value))

        individual.save()


def reverse_func(apps, schema_editor):
    """Logic for migration fallback"""
    Food = apps.get_model("core", "Food")
    Tag = apps.get_model("core", "Tag")
    People = apps.get_model("core", "People")
    Food.objects.all().delete()
    Tag.objects.all().delete()
    People.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200504_0909'),
    ]

    operations = [
        migrations.RunPython(load_food_tag_people_data, reverse_func)
    ] if 'test' not in sys.argv[1:] else []
