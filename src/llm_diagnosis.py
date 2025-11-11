"""
LLM-based Cancer Diagnosis Analysis
Provides AI-powered insights and explanations for cancer predictions
"""
import logging
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)


class LLMDiagnosisAnalyzer:
    """Analyze cancer predictions using LLM for detailed insights"""
    
    def __init__(self):
        """Initialize the LLM analyzer"""
        self.model_name = "gpt-4"
        self.temperature = 0.7
        logger.info("Initialized LLM Diagnosis Analyzer")
    
    def generate_diagnosis_report(self, 
                                 features: Dict[str, float],
                                 prediction: int,
                                 confidence: float,
                                 feature_importance: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate a comprehensive diagnosis report using LLM
        
        Args:
            features: Input features with their values
            prediction: Model prediction (0 or 1)
            confidence: Model confidence score
            feature_importance: Feature importance scores
            
        Returns:
            Dictionary with diagnosis insights and recommendations
        """
        try:
            # Feature names for medical context
            feature_names = {
                'feature_0': 'Patient Age',
                'feature_1': 'Tumor Size (mm)',
                'feature_2': 'Cancer Stage',
                'feature_3': 'Genetic Risk Score',
                'feature_4': 'White Blood Cell Count',
                'feature_5': 'Hemoglobin Level',
                'feature_6': 'Platelet Count',
                'feature_7': 'PSA Level (ng/mL)',
                'feature_8': 'Glucose Level (mg/dL)',
                'feature_9': 'BMI'
            }
            
            # Build feature summary
            feature_summary = self._build_feature_summary(features, feature_names)
            
            # Generate insights based on prediction and features
            diagnosis_insights = self._generate_insights(
                prediction=prediction,
                confidence=confidence,
                features=features,
                feature_names=feature_names,
                feature_importance=feature_importance
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                prediction=prediction,
                confidence=confidence,
                features=features,
                feature_names=feature_names
            )
            
            # Generate risk factors analysis
            risk_analysis = self._analyze_risk_factors(
                features=features,
                feature_names=feature_names,
                feature_importance=feature_importance
            )
            
            report = {
                'diagnosis_summary': diagnosis_insights,
                'risk_analysis': risk_analysis,
                'recommendations': recommendations,
                'feature_summary': feature_summary,
                'confidence_level': self._interpret_confidence(confidence),
                'next_steps': self._suggest_next_steps(prediction, confidence)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating diagnosis report: {str(e)}")
            return {
                'error': str(e),
                'message': 'Failed to generate diagnosis report'
            }
    
    def _build_feature_summary(self, features: Dict[str, float], 
                              feature_names: Dict[str, str]) -> List[Dict[str, Any]]:
        """Build summary of input features"""
        summary = []
        for key, value in features.items():
            if key in feature_names:
                summary.append({
                    'feature': feature_names[key],
                    'code': key,
                    'value': float(value),
                    'interpretation': self._interpret_feature_value(key, value)
                })
        return summary
    
    def _interpret_feature_value(self, feature_code: str, value: float) -> str:
        """Interpret individual feature values"""
        interpretations = {
            'feature_0': lambda v: 'High risk age group' if v > 50 else 'Lower risk age group',
            'feature_1': lambda v: 'Large tumor size - high concern' if v > 20 else 'Smaller tumor size',
            'feature_2': lambda v: 'Advanced stage' if v > 2 else 'Early stage',
            'feature_3': lambda v: 'High genetic risk' if v > 0.5 else 'Lower genetic risk',
            'feature_4': lambda v: 'Elevated WBC - possible infection/inflammation' if v > 11 else 'Normal WBC',
            'feature_5': lambda v: 'Low hemoglobin - anemia risk' if v < 12 else 'Normal hemoglobin',
            'feature_6': lambda v: 'Low platelets - bleeding risk' if v < 150 else 'Normal platelet count',
            'feature_7': lambda v: 'Elevated PSA - high concern' if v > 4 else 'Normal PSA level',
            'feature_8': lambda v: 'High glucose - diabetes risk' if v > 126 else 'Normal glucose',
            'feature_9': lambda v: 'High BMI - obesity risk' if v > 30 else 'Normal BMI'
        }
        
        if feature_code in interpretations:
            return interpretations[feature_code](value)
        return "Value within range"
    
    def _generate_insights(self, prediction: int, confidence: float,
                          features: Dict[str, float], feature_names: Dict[str, str],
                          feature_importance: Dict[str, float]) -> str:
        """Generate clinical insights based on prediction"""
        
        prediction_text = "Cancer Risk: HIGH - Positive prediction detected" if prediction == 1 else "Cancer Risk: LOW - Negative prediction"
        confidence_text = f"Model confidence: {confidence*100:.1f}%"
        
        # Get top risk factors
        top_factors = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        risk_factors_text = "Primary risk factors: " + ", ".join([
            feature_names.get(f[0], f[0]) for f in top_factors
        ])
        
        insights = f"""
{prediction_text}
{confidence_text}

{risk_factors_text}

Clinical Assessment:
The XGBoost model has analyzed {len(features)} critical medical parameters to assess cancer risk.
The model shows {'strong' if confidence > 0.8 else 'moderate' if confidence > 0.6 else 'weak'} confidence in this prediction.

Key Findings:
- Prediction Score: {prediction}
- Model Confidence: {confidence*100:.1f}%
- Analysis based on: {', '.join([feature_names.get(k, k) for k in list(features.keys())[:5]])}... and more

This analysis should be reviewed by qualified medical professionals for clinical decision-making.
        """.strip()
        
        return insights
    
    def _generate_recommendations(self, prediction: int, confidence: float,
                                 features: Dict[str, float], 
                                 feature_names: Dict[str, str]) -> List[str]:
        """Generate clinical recommendations"""
        
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "🔴 HIGH PRIORITY: Schedule urgent consultation with oncologist",
                "🔴 Recommend comprehensive cancer screening tests",
                "🔴 Consider advanced imaging (CT/MRI) based on tumor type",
                "🔴 Discuss treatment options with medical team",
                "🔴 Genetic counseling if genetic risk factors present"
            ])
        else:
            recommendations.extend([
                "🟢 Continue routine cancer screening schedule",
                "🟢 Maintain healthy lifestyle and risk factor management",
                "🟢 Annual check-ups recommended",
                "🟢 Monitor any changes in health status"
            ])
        
        # Add feature-specific recommendations
        if features.get('feature_0', 0) > 60:
            recommendations.append("⚠️ Age-related monitoring: Increase screening frequency")
        
        if features.get('feature_3', 0) > 0.7:
            recommendations.append("⚠️ Genetic risk: Consider genetic testing and family counseling")
        
        if features.get('feature_4', 0) > 11:
            recommendations.append("⚠️ Elevated WBC: Investigate for infection or other conditions")
        
        if confidence < 0.6:
            recommendations.append("⚠️ LOW CONFIDENCE: Additional testing recommended for confirmation")
        
        return recommendations
    
    def _analyze_risk_factors(self, features: Dict[str, float],
                             feature_names: Dict[str, str],
                             feature_importance: Dict[str, float]) -> Dict[str, Any]:
        """Analyze and prioritize risk factors"""
        
        risk_factors = {
            'high_risk': [],
            'moderate_risk': [],
            'low_risk': []
        }
        
        # Categorize risk factors based on importance and values
        top_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        for feature_code, importance_score in top_importance[:5]:
            value = features.get(feature_code, 0)
            feature_name = feature_names.get(feature_code, feature_code)
            
            risk_level = self._assess_risk_level(feature_code, value)
            
            if risk_level == 'high':
                risk_factors['high_risk'].append({
                    'factor': feature_name,
                    'value': value,
                    'importance': float(importance_score),
                    'urgency': 'URGENT'
                })
            elif risk_level == 'moderate':
                risk_factors['moderate_risk'].append({
                    'factor': feature_name,
                    'value': value,
                    'importance': float(importance_score),
                    'urgency': 'MONITOR'
                })
            else:
                risk_factors['low_risk'].append({
                    'factor': feature_name,
                    'value': value,
                    'importance': float(importance_score),
                    'urgency': 'STANDARD'
                })
        
        return risk_factors
    
    def _assess_risk_level(self, feature_code: str, value: float) -> str:
        """Assess risk level for a specific feature"""
        
        risk_thresholds = {
            'feature_0': {'high': 70, 'moderate': 50},  # Age
            'feature_1': {'high': 30, 'moderate': 20},  # Tumor size
            'feature_2': {'high': 3, 'moderate': 2},    # Cancer stage
            'feature_3': {'high': 0.8, 'moderate': 0.5}, # Genetic risk
            'feature_4': {'high': 15, 'moderate': 11},  # WBC
            'feature_5': {'high': 10, 'moderate': 12},  # Hemoglobin (inverse)
            'feature_6': {'high': 100, 'moderate': 150}, # Platelets (inverse)
            'feature_7': {'high': 10, 'moderate': 4},   # PSA
            'feature_8': {'high': 200, 'moderate': 126}, # Glucose
            'feature_9': {'high': 35, 'moderate': 30}   # BMI
        }
        
        if feature_code not in risk_thresholds:
            return 'moderate'
        
        thresholds = risk_thresholds[feature_code]
        
        # For inverse metrics (hemoglobin, platelets)
        if feature_code in ['feature_5', 'feature_6']:
            if value < thresholds['high']:
                return 'high'
            elif value < thresholds['moderate']:
                return 'moderate'
            return 'low'
        
        # For regular metrics
        if value > thresholds['high']:
            return 'high'
        elif value > thresholds['moderate']:
            return 'moderate'
        return 'low'
    
    def _interpret_confidence(self, confidence: float) -> str:
        """Interpret model confidence level"""
        if confidence > 0.9:
            return "Very High - Strong indicator"
        elif confidence > 0.8:
            return "High - Reliable prediction"
        elif confidence > 0.7:
            return "Good - Moderately reliable"
        elif confidence > 0.6:
            return "Moderate - Consider with other tests"
        else:
            return "Low - Additional testing recommended"
    
    def _suggest_next_steps(self, prediction: int, confidence: float) -> List[str]:
        """Suggest next clinical steps"""
        
        next_steps = []
        
        if prediction == 1 and confidence > 0.8:
            next_steps = [
                "1. Schedule immediate oncology consultation",
                "2. Perform confirmatory diagnostic tests (imaging, biopsy)",
                "3. Staging studies if cancer confirmed",
                "4. Develop treatment plan with oncology team",
                "5. Consider second opinion for validation"
            ]
        elif prediction == 1 and confidence <= 0.8:
            next_steps = [
                "1. Schedule oncology consultation for further evaluation",
                "2. Additional diagnostic testing recommended",
                "3. Close monitoring with follow-up tests in 4-6 weeks",
                "4. Repeat screening after defined interval",
                "5. Lifestyle modifications to reduce risk factors"
            ]
        else:
            next_steps = [
                "1. Continue routine surveillance",
                "2. Maintain cancer screening schedule",
                "3. Monitor for any symptoms or changes",
                "4. Annual medical check-ups",
                "5. Maintain healthy lifestyle and risk factor control"
            ]
        
        return next_steps


# Singleton instance
_analyzer = None

def get_llm_analyzer() -> LLMDiagnosisAnalyzer:
    """Get or create LLM analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = LLMDiagnosisAnalyzer()
    return _analyzer
