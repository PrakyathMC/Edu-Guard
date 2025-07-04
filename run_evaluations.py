# run_evaluation.py
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from src.detector import EduHallucinationDetector
import time

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_evaluation_dataset():
    """Create a dataset with known hallucinations and correct answers"""
    
    dataset = [
        # Known hallucinations (based on our tests)
        {
            "question": "What is 3847 × 2916?",
            "correct_answer": "11217852",
            "expected_hallucination": True,
            "category": "complex_math"
        },
        
        # Should be correct
        {
            "question": "What is 2 + 2?",
            "correct_answer": "4",
            "expected_hallucination": False,
            "category": "simple_math"
        },
        
        # Edge cases
        {
            "question": "What year did World War II end?",
            "correct_answer": "1945",
            "expected_hallucination": False,
            "category": "historical_fact"
        },
        
        # Ambiguous
        {
            "question": "What is the exact value of pi?",
            "correct_answer": "3.14159265358979323846...",
            "expected_hallucination": False,  # AI should say it's infinite
            "category": "mathematical_constant"
        }
    ]
    
    return dataset

def evaluate_framework():
    """Test our detection framework"""
    
    dataset = create_evaluation_dataset()
    detector = EduHallucinationDetector()
    
    results = []
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    
    print("Evaluating Hallucination Detection Framework")
    print("=" * 60)
    
    for item in dataset:
        # Get AI response
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=f"{item['question']} Please answer concisely."
            )
            
            ai_answer = response.output_text.strip()
            
            # Detect hallucination
            detection = detector.detect_hallucination(
                question=item['question'],
                ai_response=ai_answer,
                expected_answer=item['correct_answer'],
                question_type=item['category']
            )
            
            # Compare with expected
            detected = detection['hallucination_detected']
            expected = item['expected_hallucination']
            
            if detected and expected:
                true_positives += 1
                result = "TRUE POSITIVE ✓"
            elif not detected and not expected:
                true_negatives += 1
                result = "TRUE NEGATIVE ✓"
            elif detected and not expected:
                false_positives += 1
                result = "FALSE POSITIVE ✗"
            else:
                false_negatives += 1
                result = "FALSE NEGATIVE ✗"
            
            print(f"\nQ: {item['question']}")
            print(f"AI Answer: {ai_answer}")
            print(f"Expected Hallucination: {expected}")
            print(f"Detected Hallucination: {detected}")
            print(f"Result: {result}")
            print("-" * 40)
            
            results.append({
                "question": item['question'],
                "ai_answer": ai_answer,
                "detection": detection,
                "expected": expected,
                "result": result
            })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Calculate metrics
    total = len(dataset)
    accuracy = (true_positives + true_negatives) / total * 100
    
    if (true_positives + false_positives) > 0:
        precision = true_positives / (true_positives + false_positives) * 100
    else:
        precision = 0
        
    if (true_positives + false_negatives) > 0:
        recall = true_positives / (true_positives + false_negatives) * 100
    else:
        recall = 0
    
    print("\n" + "=" * 60)
    print("EVALUATION METRICS")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"True Negatives: {true_negatives}")
    print(f"False Negatives: {false_negatives}")
    print(f"\nAccuracy: {accuracy:.1f}%")
    print(f"Precision: {precision:.1f}%")
    print(f"Recall: {recall:.1f}%")
    
    # Save results
    with open("results/framework_evaluation.json", "w") as f:
        json.dump({
            "results": results,
            "metrics": {
                "true_positives": true_positives,
                "false_positives": false_positives,
                "true_negatives": true_negatives,
                "false_negatives": false_negatives,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall
            }
        }, f, indent=2)
    
    print("\nResults saved to results/framework_evaluation.json")

if __name__ == "__main__":
    evaluate_framework()