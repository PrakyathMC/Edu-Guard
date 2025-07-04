# visualize_results.py
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def create_comprehensive_visualizations():
    """Create visualizations for the 65-question dataset results"""
    
    # Load the dataset test results
    with open('results/dataset_tests/run_20250704_092019/summary_statistics.json', 'r') as f:
        stats = json.load(f)
    
    # Load raw results for detailed analysis
    with open('results/dataset_tests/run_20250704_092019/raw_results.json', 'r') as f:
        raw_results = json.load(f)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Hallucination Rate by Subcategory (Top subplot)
    ax1 = plt.subplot(2, 2, 1)
    subcat_data = stats['by_subcategory']
    categories = list(subcat_data.keys())
    rates = [subcat_data[cat]['rate'] for cat in categories]
    
    # Sort by rate for better visualization
    sorted_data = sorted(zip(categories, rates), key=lambda x: x[1], reverse=True)
    categories, rates = zip(*sorted_data)
    
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(categories)))
    bars = ax1.bar(categories, rates, color=colors)
    ax1.set_xlabel('Question Subcategory')
    ax1.set_ylabel('Hallucination Rate (%)')
    ax1.set_title('Hallucination Rates by Question Type')
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    
    # Add percentage labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)
    
    # 2. Main Category Comparison (Top right)
    ax2 = plt.subplot(2, 2, 2)
    main_cat_data = stats['by_category']
    main_categories = list(main_cat_data.keys())
    main_rates = [main_cat_data[cat]['rate'] for cat in main_categories]
    main_totals = [main_cat_data[cat]['total'] for cat in main_categories]
    
    # Create pie chart
    colors2 = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    wedges, texts, autotexts = ax2.pie(main_totals, labels=main_categories, autopct='%1.1f%%',
                                        colors=colors2, startangle=90)
    ax2.set_title('Distribution of Questions by Main Category')
    
    # 3. Difficulty Analysis (Bottom left)
    ax3 = plt.subplot(2, 2, 3)
    diff_data = stats['by_difficulty']
    difficulties = ['easy', 'medium', 'hard']
    diff_rates = [diff_data.get(d, {'rate': 0})['rate'] for d in difficulties]
    diff_totals = [diff_data.get(d, {'total': 0})['total'] for d in difficulties]
    
    x = np.arange(len(difficulties))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, diff_rates, width, label='Hallucination Rate (%)', color='#e74c3c')
    bars2 = ax3.bar(x + width/2, diff_totals, width, label='Number of Questions', color='#3498db')
    
    ax3.set_xlabel('Difficulty Level')
    ax3.set_ylabel('Value')
    ax3.set_title('Hallucination Rate vs Question Count by Difficulty')
    ax3.set_xticks(x)
    ax3.set_xticklabels(difficulties)
    ax3.legend()
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    # 4. Overall Summary (Bottom right)
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    
    summary_text = f"""
    OVERALL SUMMARY
    
    Total Questions: {stats['overall']['total_questions']}
    Total Hallucinations: {stats['overall']['total_hallucinations']}
    Overall Rate: {stats['overall']['hallucination_rate']}%
    
    Highest Risk: {categories[0]} ({rates[0]}%)
    Lowest Risk: {categories[-1]} ({rates[-1]}%)
    
    Key Finding:
    Mathematical calculations show
    significantly higher hallucination
    rates than factual questions.
    """
    
    ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('results/comprehensive_hallucination_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved visualization to results/comprehensive_hallucination_analysis.png")
    
    # Create a second figure for hallucination examples
    fig2, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Find interesting hallucination examples
    examples = []
    for result in raw_results:
        if result['hallucination_detected'] and result['subcategory'] == 'arithmetic':
            examples.append(result)
            if len(examples) >= 3:
                break
    
    example_text = "EXAMPLE HALLUCINATIONS DETECTED\n" + "="*50 + "\n\n"
    for i, ex in enumerate(examples, 1):
        example_text += f"Example {i}:\n"
        example_text += f"Question: {ex['question']}\n"
        example_text += f"AI Answer: {ex['ai_answer'][:100]}...\n" if len(ex['ai_answer']) > 100 else f"AI Answer: {ex['ai_answer']}\n"
        example_text += f"Expected: {ex['expected_answer']}\n"
        example_text += f"Category: {ex['subcategory']}\n"
        example_text += "-"*40 + "\n\n"
    
    ax.text(0.05, 0.95, example_text, fontsize=10, verticalalignment='top',
            transform=ax.transAxes, fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
    
    plt.savefig('results/hallucination_examples.png', dpi=300, bbox_inches='tight')
    print("Saved examples to results/hallucination_examples.png")

if __name__ == "__main__":
    create_comprehensive_visualizations()