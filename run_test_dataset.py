# run_dataset_test.py
import json
import os
from datetime import datetime
import time
from openai import OpenAI
from dotenv import load_dotenv
from src.detector import EduHallucinationDetector
import pandas as pd

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class DatasetTester:
    def __init__(self):
        self.detector = EduHallucinationDetector()
        self.results_dir = "results/dataset_tests"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Initialize results storage
        self.all_results = []
        self.summary_stats = {}
        
    def load_dataset(self):
        """Load the test dataset"""
        with open("data/hallucination_test_dataset.json", "r") as f:
            return json.load(f)
    
    def test_single_question(self, question_data, category, subcategory):
        """Test a single question and return results"""
        question = question_data["q"]
        expected_answer = str(question_data["a"])
        difficulty = question_data.get("difficulty", "medium")
        
        try:
            # Get AI response
            response = client.responses.create(
                model="gpt-4.1",
                input=f"{question} Please provide a direct, numerical answer where applicable."
            )
            
            ai_answer = response.output_text.strip()
            
            # Detect hallucination
            detection = self.detector.detect_hallucination(
                question=question,
                ai_response=ai_answer,
                expected_answer=expected_answer,
                question_type=subcategory
            )
            
            # Create result record
            result = {
                "category": category,
                "subcategory": subcategory,
                "difficulty": difficulty,
                "question": question,
                "expected_answer": expected_answer,
                "ai_answer": ai_answer,
                "hallucination_detected": detection['hallucination_detected'],
                "detection_confidence": detection['confidence'],
                "detection_details": detection['detection_details']
            }
            
            return result
            
        except Exception as e:
            return {
                "category": category,
                "subcategory": subcategory,
                "difficulty": difficulty,
                "question": question,
                "expected_answer": expected_answer,
                "ai_answer": f"ERROR: {str(e)}",
                "hallucination_detected": None,
                "error": True
            }
    
    def run_tests(self):
        """Run all tests in the dataset"""
        dataset = self.load_dataset()
        total_questions = dataset["metadata"]["total_questions"]
        
        print(f"Starting test run: {self.timestamp}")
        print(f"Total questions to test: {total_questions}")
        print("="*70)
        
        question_count = 0
        
        # Test each category
        for main_category, subcategories in dataset["categories"].items():
            for subcategory, questions in subcategories.items():
                if not questions:
                    continue
                    
                print(f"\nTesting {main_category}/{subcategory} ({len(questions)} questions)")
                print("-"*50)
                
                for i, question_data in enumerate(questions):
                    question_count += 1
                    
                    # Progress indicator
                    print(f"[{question_count}/{total_questions}] Testing: {question_data['q'][:50]}...")
                    
                    # Test the question
                    result = self.test_single_question(question_data, main_category, subcategory)
                    self.all_results.append(result)
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                    # Save intermediate results every 10 questions
                    if question_count % 10 == 0:
                        self.save_intermediate_results()
        
        print("\n" + "="*70)
        print("Test run completed!")
        self.analyze_results()
        self.save_final_results()
    
    def save_intermediate_results(self):
        """Save results periodically during testing"""
        temp_file = os.path.join(self.results_dir, f"temp_{self.timestamp}.json")
        with open(temp_file, "w") as f:
            json.dump(self.all_results, f, indent=2)
    
    def analyze_results(self):
        """Analyze test results and generate summary statistics"""
        df = pd.DataFrame(self.all_results)
        
        # Overall statistics
        total_tested = len(df)
        total_hallucinations = df['hallucination_detected'].sum()
        overall_rate = (total_hallucinations / total_tested * 100) if total_tested > 0 else 0
        
        self.summary_stats['overall'] = {
            'total_questions': total_tested,
            'total_hallucinations': int(total_hallucinations),
            'hallucination_rate': round(overall_rate, 2)
        }
        
        # By category
        self.summary_stats['by_category'] = {}
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            cat_hallucinations = cat_df['hallucination_detected'].sum()
            cat_rate = (cat_hallucinations / len(cat_df) * 100) if len(cat_df) > 0 else 0
            
            self.summary_stats['by_category'][category] = {
                'total': len(cat_df),
                'hallucinations': int(cat_hallucinations),
                'rate': round(cat_rate, 2)
            }
        
        # By subcategory
        self.summary_stats['by_subcategory'] = {}
        for subcategory in df['subcategory'].unique():
            sub_df = df[df['subcategory'] == subcategory]
            sub_hallucinations = sub_df['hallucination_detected'].sum()
            sub_rate = (sub_hallucinations / len(sub_df) * 100) if len(sub_df) > 0 else 0
            
            self.summary_stats['by_subcategory'][subcategory] = {
                'total': len(sub_df),
                'hallucinations': int(sub_hallucinations),
                'rate': round(sub_rate, 2)
            }
        
        # By difficulty
        self.summary_stats['by_difficulty'] = {}
        for difficulty in df['difficulty'].unique():
            diff_df = df[df['difficulty'] == difficulty]
            diff_hallucinations = diff_df['hallucination_detected'].sum()
            diff_rate = (diff_hallucinations / len(diff_df) * 100) if len(diff_df) > 0 else 0
            
            self.summary_stats['by_difficulty'][difficulty] = {
                'total': len(diff_df),
                'hallucinations': int(diff_hallucinations),
                'rate': round(diff_rate, 2)
            }
    
    def save_final_results(self):
        """Save all results and analysis"""
        # Create output directory for this run
        run_dir = os.path.join(self.results_dir, f"run_{self.timestamp}")
        os.makedirs(run_dir, exist_ok=True)
        
        # 1. Save raw results
        raw_file = os.path.join(run_dir, "raw_results.json")
        with open(raw_file, "w") as f:
            json.dump(self.all_results, f, indent=2)
        
        # 2. Save summary statistics
        summary_file = os.path.join(run_dir, "summary_statistics.json")
        with open(summary_file, "w") as f:
            json.dump(self.summary_stats, f, indent=2)
        
        # 3. Save as CSV for easy analysis
        csv_file = os.path.join(run_dir, "results.csv")
        df = pd.DataFrame(self.all_results)
        df.to_csv(csv_file, index=False)
        
        # 4. Generate summary report
        report_file = os.path.join(run_dir, "summary_report.txt")
        with open(report_file, "w") as f:
            f.write(f"HALLUCINATION DETECTION TEST REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("OVERALL STATISTICS\n")
            f.write("-"*30 + "\n")
            f.write(f"Total Questions: {self.summary_stats['overall']['total_questions']}\n")
            f.write(f"Total Hallucinations: {self.summary_stats['overall']['total_hallucinations']}\n")
            f.write(f"Overall Hallucination Rate: {self.summary_stats['overall']['hallucination_rate']}%\n\n")
            
            f.write("BY CATEGORY\n")
            f.write("-"*30 + "\n")
            for cat, stats in self.summary_stats['by_category'].items():
                f.write(f"{cat:15} | Total: {stats['total']:3} | Hallucinations: {stats['hallucinations']:3} | Rate: {stats['rate']:6.2f}%\n")
            
            f.write("\nBY SUBCATEGORY\n")
            f.write("-"*30 + "\n")
            for subcat, stats in self.summary_stats['by_subcategory'].items():
                f.write(f"{subcat:15} | Total: {stats['total']:3} | Hallucinations: {stats['hallucinations']:3} | Rate: {stats['rate']:6.2f}%\n")
            
            f.write("\nBY DIFFICULTY\n")
            f.write("-"*30 + "\n")
            for diff, stats in self.summary_stats['by_difficulty'].items():
                f.write(f"{diff:10} | Total: {stats['total']:3} | Hallucinations: {stats['hallucinations']:3} | Rate: {stats['rate']:6.2f}%\n")
        
        # Print summary
        print("\nRESULTS SAVED:")
        print(f"  Directory: {run_dir}")
        print(f"  - Raw results: raw_results.json")
        print(f"  - Summary stats: summary_statistics.json")
        print(f"  - CSV file: results.csv")
        print(f"  - Summary report: summary_report.txt")
        
        # Display key findings
        print("\nKEY FINDINGS:")
        print(f"  Overall hallucination rate: {self.summary_stats['overall']['hallucination_rate']}%")
        
        # Find highest and lowest hallucination categories
        cat_stats = self.summary_stats['by_subcategory']
        sorted_cats = sorted(cat_stats.items(), key=lambda x: x[1]['rate'], reverse=True)
        
        print(f"\n  Highest hallucination rate: {sorted_cats[0][0]} ({sorted_cats[0][1]['rate']}%)")
        print(f"  Lowest hallucination rate: {sorted_cats[-1][0]} ({sorted_cats[-1][1]['rate']}%)")
        
        # Clean up temp files
        temp_files = [f for f in os.listdir(self.results_dir) if f.startswith(f"temp_{self.timestamp}")]
        for temp_file in temp_files:
            os.remove(os.path.join(self.results_dir, temp_file))

def main():
    """Main function to run the dataset test"""
    print("EduGuard Dataset Testing Framework")
    print("="*70)
    
    # Check if dataset exists
    if not os.path.exists("data/hallucination_test_dataset.json"):
        print("ERROR: Dataset not found. Please run create_dataset.py first.")
        return
    
    # Confirm before starting
    print("\nThis will test 70 questions and may take 5-10 minutes.")
    response = input("Do you want to continue? (y/n): ")
    
    if response.lower() != 'y':
        print("Test cancelled.")
        return
    
    # Run tests
    tester = DatasetTester()
    tester.run_tests()

if __name__ == "__main__":
    main()