# src/detector.py
import re
from typing import Dict, List, Tuple
import json

class EduHallucinationDetector:
    """Framework for detecting hallucinations in educational AI responses"""
    
    def __init__(self):
        self.detection_methods = {
            'calculation_check': self.check_calculation,
            'consistency_check': self.check_consistency,
            'confidence_analysis': self.analyze_confidence,
            'factual_verification': self.verify_facts
        }
    
    def detect_hallucination(self, question: str, ai_response: str, 
                           expected_answer: str = None, 
                           question_type: str = None) -> Dict:
        """Main detection method that combines multiple techniques"""
        
        results = {
            'question': question,
            'ai_response': ai_response,
            'expected_answer': expected_answer,
            'hallucination_detected': False,
            'confidence': 0.0,
            'detection_details': {}
        }
        
        # Run different detection methods based on question type
        if question_type == 'calculation':
            calc_result = self.check_calculation(question, ai_response, expected_answer)
            results['detection_details']['calculation'] = calc_result
            if calc_result['error_detected']:
                results['hallucination_detected'] = True
                results['confidence'] = calc_result['confidence']
        
        # Check for confidence markers
        confidence_result = self.analyze_confidence(ai_response)
        results['detection_details']['confidence'] = confidence_result
        
        # Check for factual accuracy if we have expected answer
        if expected_answer:
            fact_result = self.verify_facts(ai_response, expected_answer)
            results['detection_details']['factual'] = fact_result
            if fact_result['mismatch']:
                results['hallucination_detected'] = True
        
        return results
    
    def check_calculation(self, question: str, response: str, expected: str) -> Dict:
        """Check mathematical calculations for errors"""
        
        # Extract numbers from response
        numbers_in_response = re.findall(r'[\d,]+', response)
        numbers_in_response = [n.replace(',', '') for n in numbers_in_response]
        
        result = {
            'error_detected': False,
            'confidence': 0.0,
            'details': {}
        }
        
        if expected and str(expected) not in numbers_in_response:
            result['error_detected'] = True
            result['confidence'] = 0.9
            
            # Try to find the incorrect number
            for num in numbers_in_response:
                if len(num) >= len(str(expected)) - 2:  # Similar length
                    try:
                        diff = abs(int(num) - int(expected))
                        error_rate = diff / int(expected)
                        result['details'] = {
                            'found_number': num,
                            'expected': expected,
                            'difference': diff,
                            'error_rate': f"{error_rate*100:.2f}%"
                        }
                        break
                    except:
                        pass
        
        return result
    
    def analyze_confidence(self, response: str) -> Dict:
        """Analyze confidence markers in the response"""
        
        high_confidence_markers = [
            'definitely', 'certainly', 'exactly', 'precisely', 
            'without a doubt', 'absolutely'
        ]
        
        low_confidence_markers = [
            'approximately', 'about', 'roughly', 'around',
            'I think', 'perhaps', 'might be', 'possibly',
            'not yet been announced', 'as of now'
        ]
        
        result = {
            'confidence_level': 'neutral',
            'markers_found': []
        }
        
        response_lower = response.lower()
        
        for marker in high_confidence_markers:
            if marker in response_lower:
                result['confidence_level'] = 'high'
                result['markers_found'].append(marker)
        
        for marker in low_confidence_markers:
            if marker in response_lower:
                result['confidence_level'] = 'low'
                result['markers_found'].append(marker)
        
        return result
    
    def check_consistency(self, responses: List[str]) -> Dict:
        """Check consistency across multiple responses to same question"""
        # This would be used when we ask the same question multiple times
        pass
    
    def verify_facts(self, response: str, expected: str) -> Dict:
        """Basic factual verification"""
        
        result = {
            'mismatch': False,
            'similarity': 0.0
        }
        
        # Simple check - in real implementation, this would be more sophisticated
        if expected.lower() not in response.lower():
            result['mismatch'] = True
            
            # Calculate simple similarity
            expected_words = set(expected.lower().split())
            response_words = set(response.lower().split())
            
            if expected_words and response_words:
                overlap = len(expected_words & response_words)
                result['similarity'] = overlap / len(expected_words)
        
        return result
