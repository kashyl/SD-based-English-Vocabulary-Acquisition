from prompt_generation.tag_categories import *
import random

def extract_value_if_enum(source):
    if isinstance(source, Enum):
        return source.value
    return source

def choose_from(*sources):
    """Chooses an item from each source provided."""
    choices = []
    for source in sources:
        source = extract_value_if_enum(source)  # Handle Enums
        if not source:  # If the source is empty, skip it
            continue
        if isinstance(source, list):
            choices.append(random.choice(source))
        else:
            choices.append(random_from_class(source))
    return choices

def choose_one(*weighted_sources):
    """Chooses based on given weights."""
    sources, weights = zip(*weighted_sources)
    sources = [extract_value_if_enum(source) for source in sources]  # Handle Enums
    return random.choices(sources, weights, k=1)[0]

def random_from_class(item):
    """Choose randomly among the attributes of a class or its instance."""
    # If it's not a class definition or an instance, simply return the item.
    if not isinstance(item, (Enum)):
        return item

    item = extract_value_if_enum(item)
    
    attributes = [attr for attr in dir(item) if not callable(getattr(item, attr)) and not attr.startswith("__")]

    if not attributes:
        raise ValueError(f"No attributes found for {item}")

    return random.choice(attributes)

def get_multiple_tags(elements, *probabilities):
    """
    Always returns one element from elements, and then additional elements based on probabilities.
    """
    elements = extract_value_if_enum(elements)  # Handle Enums
    
    # Always get one guaranteed object
    selected_elements = [random.choice(elements)]
    
    # Based on the probabilities, try to get additional elements
    for prob in probabilities:
        if random.random() < prob:
            element = random.choice(elements)
            
            # Ensure uniqueness, continue drawing until unique element is found
            while element in selected_elements:
                element = random.choice(elements)
                
            selected_elements.append(element)

    return selected_elements

def get_unique_samples(source, count):
    """Return a list with unique elements up to count."""
    source = extract_value_if_enum(source)  # Handle Enums
    
    if count <= len(source):
        return random.sample(source, count)
    else:
        unique_samples = random.sample(source, len(source))  # get all unique items first
        remaining_count = count - len(source)
        additional_samples = random.choices(source, k=remaining_count)  # allows duplicates
        return unique_samples + additional_samples

def get_single_tag(source, chance):
    """Return a single element from the source or None based on the provided chance."""
    source = extract_value_if_enum(source)
    if not source:
        return []
    
    return [random.choice(source)] if random.random() < chance else []


def choose_elements_based_on_probability(elements):
    """Return a list of elements chosen based on their probability."""
    chosen_elements = []
    
    for element, probability in extract_value_if_enum(elements):
        if random.random() < probability:
            chosen_elements.append(element)
            
    return chosen_elements

def generate_prompt_animals():    
    return (
        choose_elements_based_on_probability(Defaults.animal) + 
        get_multiple_tags(Animals.animal_names, 0.25, 0.1) +
        choose_from(
            choose_one(
                (Locations.natural_elements, 0.9), 
                (Locations.urban_elements, 0.1)
            )
        ) +
        get_single_tag(Nature.nature_phenomena_elements, 0.5)
    )

def generate_prompt_nature():
    return (
        choose_elements_based_on_probability(Defaults.nature) +
        get_multiple_tags(Locations.natural_elements, 0.75, 0.5, 0.25) +
        get_single_tag(Nature.plants_flowers, 0.75) +
        get_single_tag(Animals.animal_names, 0.5) +
        get_single_tag(Nature.nature_phenomena_elements, 0.5)
    )

def generate_prompt_sceneries():
    natural_elements_list = extract_value_if_enum(Locations.natural_elements)
    urban_elements_list = extract_value_if_enum(Locations.urban_elements)
    combined_elements = natural_elements_list + urban_elements_list
    return (
        choose_elements_based_on_probability(Defaults.sceneries) + 
        get_multiple_tags(combined_elements, 1.0, 0.75, 0.5) + 
        get_single_tag(ObjectsAndConcepts.misc_objects, 0.1) +
        get_single_tag(Nature.plants_flowers, 0.5)
    )

def generate_prompt_clothes():
    source_to_probability = [
        (Clothing.dresses_and_skirts, 0.5),
        (Clothing.inners, 1),
        (Clothing.outers, 1),
        (Clothing.bottoms, 1),
        (Clothing.footwear, 0.8),
        (Clothing.headwear, 0.75),
        (Clothing.sleeves, 0.5),
        (Clothing.accessories, 1),
        (Clothing.special_costumes_and_decorative_elements, 0.25),
        (Clothing.fabrics_and_patterns, 0.25)
    ]

    choices = [get_single_tag(source, chance) for source, chance in source_to_probability]
    return choose_from(*choices)

def generate_prompt_objects():
    return get_multiple_tags(ObjectsAndConcepts.misc_objects, 0.75, 0.5, 0.25)

def generate_prompt_actions():
    always_chosen = [extract_value_if_enum(Actions.basic_actions), extract_value_if_enum(Actions.poses)]
    source_to_probability = [
        (Actions.hands_and_arms, 0.75),
        (Actions.legs_and_feet, 0.75),
        (Actions.head, 0.5),
        (Actions.interactions_with_others, 0.5),
        (Actions.interactions_with_objects_and_environment, 0.5),
        (Actions.angles, 0.25)
    ]
    choices = always_chosen + [get_single_tag(source, chance) for source, chance in source_to_probability]
    return choose_from(*choices)

def generate_prompt_people():
    basic_actions_list = extract_value_if_enum(Actions.basic_actions)
    poses_list = extract_value_if_enum(Actions.poses)

    always_chosen = [
        get_single_tag(People.basic, 1.0),  # 100% chance to get one
        get_single_tag(People.occupations_and_roles, 1.0),
        get_single_tag(Hair.style, 1.0),
        get_single_tag(Hair.length, 1.0),
        get_single_tag(Hair.color, 1.0),
        get_single_tag(random.choice(list(Expressions)).value, 1.0),
        choose_one((Locations.indoors, 0.25), (Locations.urban_elements, 0.75))
    ]

    source_to_probability = [
        (Hair.accessories, 0.5),
        (Hair.other, 0.25),
        (Eyes.color, 0.75),
        (Eyes.eyewear_related, 0.1),
        (basic_actions_list + poses_list, 0.25),
        (Clothing.inners, 0.25),
        (Clothing.outers, 0.25),
        (Clothing.bottoms, 0.25),
        (Clothing.footwear, 0.5),
        (Clothing.headwear, 0.25),
        (Clothing.accessories, 0.1)
    ]

    choices = always_chosen + [get_single_tag(source, chance) for source, chance in source_to_probability]

    return choose_from(*choices)

def generate_prompt_fantasy():
    return (
        get_single_tag(choose_one((People.basic, 0.25), (Animals.animal_names, 0.75)), 1.0) +
        get_single_tag(Eyes.eye_features_conditions, 0.1) +
        get_single_tag(Eyes.pupils_sclera, 0.25) +
        get_multiple_tags(Animals.animal_features, 0.5, 0.25, 0.1) +
        get_multiple_tags(People.fantasy_and_mythical, 0.5, 0.25, 0.1)
    )

def generate_prompt_hairstyles():
    return choose_elements_based_on_probability(Defaults.hairstyles) + choose_from(
        Hair.style,
        Hair.length,
        Hair.color,
        get_single_tag(Hair.accessories, 0.75)
    )

def generate_prompt_expressions():
    return choose_elements_based_on_probability(Defaults.expressions) + choose_from(
        People.basic,
        random.choice(list(Expressions)).value
    )

PROMPT_CATEGORIES_FUNCTIONS = {
    "Animals": generate_prompt_animals,
    "Nature": generate_prompt_nature,
    "Sceneries": generate_prompt_sceneries,
    "Clothes": generate_prompt_clothes,
    "Objects": generate_prompt_objects,
    "Actions": generate_prompt_actions,
    "People": generate_prompt_people,
    "Fantasy": generate_prompt_fantasy,
    "Hair Styles": generate_prompt_hairstyles,
    "Expressions": generate_prompt_expressions,
}

def generate_prompt(prompt_category):
    if prompt_category not in PROMPT_CATEGORIES_FUNCTIONS:
        raise ValueError("Invalid prompt category")

    return PROMPT_CATEGORIES_FUNCTIONS[prompt_category]()
