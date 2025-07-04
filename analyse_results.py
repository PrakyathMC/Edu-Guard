# analyze_results.py
import json
import glob
from src.detector import EduHallucinationDetector

def analyze_test_results():
    """Analyze the results from our hallucination tests"""
    
    # Find the most recent results file
    result_files = glob.glob("results/hallucination_test_*.json")
    if not result_files:
        print("No result files found!")
        return
    
    latest_file = sorted(result_files)[-1]
    print(f"Analyzing: {latest_file}\n")
    
    with open(latest_file, 'r') as f:
        results = json.load(f)
    
    # Initialize detector
    detector = EduHallucinationDetector()
    
    # Analyze each result
    hallucination_count = 0
    detailed_results = []
    
    for result in results:
        detection = detector.detect_hallucination(
            question=result['question'],
            ai_response=result['ai_answer'],
            expected_answer=str(result['expected_answer']),
            question_type=result['type']
        )
        
        if detection['hallucination_detected']:
            hallucination_count += 1
            
        detailed_results.append({
            **result,
            'detection': detection
        })
        
        print(f"\nQuestion: {result['question']}")
        print(f"Category: {result['category']}")
        print(f"Hallucination Detected: {detection['hallucination_detected']}")
        if detection['hallucination_detected']:
            print(f"Detection Details: {detection['detection_details']}")
        print("-" * 60)
    
    # Summary statistics
    print(f"\n\nSUMMARY")
    print(f"Total Questions: {len(results)}")
    print(f"Hallucinations Detected: {hallucination_count}")
    print(f"Detection Rate: {hallucination_count/len(results)*100:.1f}%")
    
    # Save detailed analysis
    with open("results/analysis_detailed.json", 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    return detailed_results

if __name__ == "__main__":
    analyze_test_results()
