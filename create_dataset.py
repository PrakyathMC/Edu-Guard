# create_dataset.py
import json
import math
from datetime import datetime

def create_comprehensive_dataset():
    """Create a comprehensive dataset for hallucination testing"""
    
    dataset = {
        "metadata": {
            "created_date": datetime.now().isoformat(),
            "version": "1.0",
            "total_questions": 0
        },
        "categories": {
            "mathematics": {
                "arithmetic": [],
                "algebra": [],
                "geometry": []
            },
            "science": {
                "physics": [],
                "chemistry": [],
                "biology": []
            },
            "factual": {
                "history": [],
                "geography": [],
                "general_knowledge": []
            },
            "reasoning": {
                "logic": [],
                "word_problems": []
            }
        }
    }
    
    # MATHEMATICS - ARITHMETIC (15 questions)
    arithmetic_questions = [
        # Basic operations
        {"q": "What is 156 × 234?", "a": 156 * 234, "difficulty": "medium"},
        {"q": "What is 8934 × 7265?", "a": 8934 * 7265, "difficulty": "hard"},
        {"q": "What is 45678 ÷ 234?", "a": 45678 / 234, "difficulty": "hard"},
        {"q": "What is 9876 - 5432?", "a": 9876 - 5432, "difficulty": "easy"},
        {"q": "What is 12345 + 67890?", "a": 12345 + 67890, "difficulty": "easy"},
        
        # Powers and roots
        {"q": "What is 17^3?", "a": 17**3, "difficulty": "medium"},
        {"q": "What is the square root of 15129?", "a": math.sqrt(15129), "difficulty": "hard"},
        {"q": "What is 2^12?", "a": 2**12, "difficulty": "medium"},
        
        # Decimals and fractions
        {"q": "What is 0.125 × 0.25?", "a": 0.125 * 0.25, "difficulty": "medium"},
        {"q": "What is 3/4 + 5/6?", "a": "19/12 or 1.583", "difficulty": "medium"},
        {"q": "What is 15% of 2400?", "a": 0.15 * 2400, "difficulty": "easy"},
        
        # Complex calculations
        {"q": "What is (234 × 567) - (123 × 456)?", "a": (234 * 567) - (123 * 456), "difficulty": "hard"},
        {"q": "What is 123^2 + 456^2?", "a": 123**2 + 456**2, "difficulty": "hard"},
        {"q": "What is the sum of all integers from 1 to 100?", "a": 5050, "difficulty": "medium"},
        {"q": "What is 9! (9 factorial)?", "a": 362880, "difficulty": "hard"},
    ]
    
    # SCIENCE - PHYSICS (10 questions)
    physics_questions = [
        {"q": "What is the speed of light in vacuum in m/s?", "a": "299792458", "difficulty": "medium"},
        {"q": "What is the acceleration due to gravity on Earth in m/s²?", "a": "9.8 or 9.81", "difficulty": "easy"},
        {"q": "At what temperature does water boil at sea level in Celsius?", "a": "100", "difficulty": "easy"},
        {"q": "What is the freezing point of water in Kelvin?", "a": "273.15", "difficulty": "medium"},
        {"q": "What is Planck's constant (h) in J⋅s?", "a": "6.626 × 10^-34", "difficulty": "hard"},
        {"q": "What is the charge of an electron in Coulombs?", "a": "-1.602 × 10^-19", "difficulty": "hard"},
        {"q": "How many meters are in one light-year?", "a": "9.461 × 10^15", "difficulty": "hard"},
        {"q": "What is the wavelength range of visible light in nanometers?", "a": "380-700 or 380-750", "difficulty": "medium"},
        {"q": "What is absolute zero in Celsius?", "a": "-273.15", "difficulty": "medium"},
        {"q": "What is the speed of sound in air at 20°C in m/s?", "a": "343", "difficulty": "medium"},
    ]
    
    # SCIENCE - CHEMISTRY (10 questions)
    chemistry_questions = [
        {"q": "What is the atomic number of Carbon?", "a": "6", "difficulty": "easy"},
        {"q": "How many protons does Oxygen have?", "a": "8", "difficulty": "easy"},
        {"q": "What is the molecular weight of water (H2O)?", "a": "18.015 or 18", "difficulty": "medium"},
        {"q": "What is Avogadro's number?", "a": "6.022 × 10^23", "difficulty": "medium"},
        {"q": "What is the pH of pure water at 25°C?", "a": "7", "difficulty": "easy"},
        {"q": "How many electrons can the first electron shell hold?", "a": "2", "difficulty": "easy"},
        {"q": "What is the molar mass of CO2 in g/mol?", "a": "44.01 or 44", "difficulty": "medium"},
        {"q": "What is the oxidation state of oxygen in H2O?", "a": "-2", "difficulty": "medium"},
        {"q": "How many valence electrons does Nitrogen have?", "a": "5", "difficulty": "medium"},
        {"q": "What is the boiling point of ethanol in Celsius?", "a": "78.37 or 78.4", "difficulty": "hard"},
    ]
    
    # SCIENCE - BIOLOGY (5 questions)
    biology_questions = [
        {"q": "How many chromosomes do humans have?", "a": "46", "difficulty": "easy"},
        {"q": "How many chambers does a human heart have?", "a": "4", "difficulty": "easy"},
        {"q": "What is the normal human body temperature in Celsius?", "a": "37 or 36.5-37.5", "difficulty": "easy"},
        {"q": "How many bones are in an adult human body?", "a": "206", "difficulty": "medium"},
        {"q": "What percentage of the human body is water?", "a": "60 or 55-65", "difficulty": "medium"},
    ]
    
    # FACTUAL - HISTORY (10 questions)
    history_questions = [
        {"q": "In what year did World War II end?", "a": "1945", "difficulty": "easy"},
        {"q": "When was the United States Declaration of Independence signed?", "a": "1776", "difficulty": "easy"},
        {"q": "In what year did Christopher Columbus first reach the Americas?", "a": "1492", "difficulty": "easy"},
        {"q": "When did the Berlin Wall fall?", "a": "1989", "difficulty": "medium"},
        {"q": "In what year was the Magna Carta signed?", "a": "1215", "difficulty": "hard"},
        {"q": "When did the Roman Empire fall?", "a": "476 or 476 CE", "difficulty": "medium"},
        {"q": "What year did World War I begin?", "a": "1914", "difficulty": "easy"},
        {"q": "When was the French Revolution?", "a": "1789", "difficulty": "medium"},
        {"q": "In what year did humans first land on the moon?", "a": "1969", "difficulty": "easy"},
        {"q": "When was the printing press invented by Gutenberg?", "a": "1440 or 1450s", "difficulty": "hard"},
    ]
    
    # FACTUAL - GEOGRAPHY (10 questions)
    geography_questions = [
        {"q": "What is the capital of Australia?", "a": "Canberra", "difficulty": "medium"},
        {"q": "How many continents are there?", "a": "7", "difficulty": "easy"},
        {"q": "What is the longest river in the world?", "a": "Nile or Amazon", "difficulty": "medium"},
        {"q": "What is the highest mountain in the world?", "a": "Mount Everest", "difficulty": "easy"},
        {"q": "How many countries are in the United Nations?", "a": "193", "difficulty": "hard"},
        {"q": "What is the smallest country in the world?", "a": "Vatican City", "difficulty": "medium"},
        {"q": "What is the deepest ocean trench?", "a": "Mariana Trench", "difficulty": "medium"},
        {"q": "How many time zones does Russia span?", "a": "11", "difficulty": "hard"},
        {"q": "What is the capital of Mongolia?", "a": "Ulaanbaatar", "difficulty": "hard"},
        {"q": "How many countries does the Amazon rainforest span?", "a": "9", "difficulty": "hard"},
    ]
    
    # REASONING - LOGIC (5 questions)
    logic_questions = [
        {"q": "If all roses are flowers and all flowers need water, do roses need water?", "a": "Yes", "difficulty": "easy"},
        {"q": "What comes next in the sequence: 2, 4, 8, 16, ?", "a": "32", "difficulty": "easy"},
        {"q": "If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?", "a": "5 minutes", "difficulty": "medium"},
        {"q": "What is heavier: a kilogram of feathers or a kilogram of steel?", "a": "They weigh the same", "difficulty": "easy"},
        {"q": "If you overtake the person in second place in a race, what position are you in?", "a": "Second place", "difficulty": "medium"},
    ]
    
    # Add all questions to dataset
    dataset["categories"]["mathematics"]["arithmetic"] = arithmetic_questions
    dataset["categories"]["science"]["physics"] = physics_questions
    dataset["categories"]["science"]["chemistry"] = chemistry_questions
    dataset["categories"]["science"]["biology"] = biology_questions
    dataset["categories"]["factual"]["history"] = history_questions
    dataset["categories"]["factual"]["geography"] = geography_questions
    dataset["categories"]["reasoning"]["logic"] = logic_questions
    
    # Count total questions
    total = 0
    for main_cat in dataset["categories"]:
        for sub_cat in dataset["categories"][main_cat]:
            total += len(dataset["categories"][main_cat][sub_cat])
    
    dataset["metadata"]["total_questions"] = total
    
    # Save dataset
    with open("data/hallucination_test_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Created dataset with {total} questions")
    print("\nBreakdown by category:")
    for main_cat in dataset["categories"]:
        for sub_cat in dataset["categories"][main_cat]:
            count = len(dataset["categories"][main_cat][sub_cat])
            if count > 0:
                print(f"  {main_cat}/{sub_cat}: {count} questions")
    
    return dataset

if __name__ == "__main__":
    dataset = create_comprehensive_dataset()