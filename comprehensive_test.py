# comprehensive_test.py
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from src.detector import EduHallucinationDetector
import time
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_comprehensive_dataset():
    """Create a comprehensive test dataset across multiple categories"""
    
    return [
        # Mathematics - Complex calculations
        {"q": "What is 8743 × 6291?", "a": "55025913", "cat": "math_complex"},
        {"q": "What is sqrt(87436)?", "a": "295.693", "cat": "math_complex"},
        {"q": "What is 2^15?", "a": "32768", "cat": "math_complex"},
        
        # Science - Specific facts
        {"q": "What is the speed of light in m/s?", "a": "299792458", "cat": "science"},
        {"q": "How many chromosomes do humans have?", "a": "46", "cat": "science"},
        {"q": "What is the atomic number of carbon?", "a": "6", "cat": "science"},
        
        # History - Dates
        {"q": "In what year did Columbus reach America?", "a": "1492", "cat": "history"},
        {"q": "When was the Declaration of Independence signed?", "a": "1776", "cat": "history"},
        
        # Geography
        {"q": "What is the capital of Mongolia?", "a": "Ulaanbaatar", "cat": "geography"},
        {"q": "How many countries are in Africa?", "a": "54", "cat": "geography"},
        
        # Trick questions
        {"q": "What happens when an unstoppable force meets an immovable object?", 
         "a": "paradox", "cat": "trick"},
        {"q": "What's the last digit of pi?", "a": "no last digit", "cat": "trick"},
    ]

def run_comprehensive_test():
    """Run comprehensive hallucination test"""
    
    dataset = create_comprehensive_dataset()
    detector = EduHallucinationDetector()
    
    print("Running Comprehensive Hallucination Test")
    print("=" * 70)
    
    all_results = []
    hallucination_by_category = {}
    
    for idx, item in enumerate(dataset):
        print(f"\nTest {idx+1}/{len(dataset)}")
        print(f"Category: {item['cat']}")
        print(f"Question: {item['q']}")
        
        # Get AI response
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=f"{item['q']} Give a direct, concise answer."
            )
            
            ai_answer = response.output_text.strip()
            print(f"AI Answer: {ai_answer}")
            print(f"Expected: {item['a']}")
            
            # Detect hallucination
            detection = detector.detect_hallucination(
                question=item['q'],
                ai_response=ai_answer,
                expected_answer=item['a'],
                question_type=item['cat']
            )
            
            # Manual verification for some categories
            is_hallucination = detection['hallucination_detected']
            
            # For trick questions, check if AI recognized the trick
            if item['cat'] == 'trick':
                if 'paradox' in item['a'] and 'paradox' in ai_answer.lower():
                    is_hallucination = False
                elif 'no last digit' in item['a'] and ('infinite' in ai_answer.lower() or 'no last' in ai_answer.lower()):
                    is_hallucination = False
            
            result = {
                "question": item['q'],
                "expected": item['a'],
                "ai_answer": ai_answer,
                "category": item['cat'],
                "hallucination_detected": is_hallucination,
                "detection_details": detection['detection_details']
            }
            
            all_results.append(result)
            
            # Track by category
            if item['cat'] not in hallucination_by_category:
                hallucination_by_category[item['cat']] = {"total": 0, "hallucinations": 0}
            
            hallucination_by_category[item['cat']]["total"] += 1
            if is_hallucination:
                hallucination_by_category[item['cat']]["hallucinations"] += 1
            
            print(f"Hallucination: {'YES' if is_hallucination else 'NO'}")
            print("-" * 50)
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY BY CATEGORY")
    print("-" * 70)
    
    for cat, stats in hallucination_by_category.items():
        rate = stats["hallucinations"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"{cat:15} | Total: {stats['total']:2} | Hallucinations: {stats['hallucinations']:2} | Rate: {rate:5.1f}%")
    
    # Overall statistics
    total_questions = len(all_results)
    total_hallucinations = sum(1 for r in all_results if r['hallucination_detected'])
    overall_rate = total_hallucinations / total_questions * 100
    
    print("-" * 70)
    print(f"{'OVERALL':15} | Total: {total_questions:2} | Hallucinations: {total_hallucinations:2} | Rate: {overall_rate:5.1f}%")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "test_date": timestamp,
        "model": "gpt-4.1",
        "total_questions": total_questions,
        "total_hallucinations": total_hallucinations,
        "hallucination_rate": overall_rate,
        "by_category": hallucination_by_category,
        "detailed_results": all_results
    }
    
    filename = f"results/comprehensive_test_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nDetailed results saved to {filename}")
    
    return output

if __name__ == "__main__":
    results = run_comprehensive_test()