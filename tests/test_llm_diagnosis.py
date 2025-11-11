"""
Unit tests for LLM Diagnosis Analyzer
"""
import pytest
from src.llm_diagnosis import LLMDiagnosisAnalyzer, get_llm_analyzer


class TestLLMDiagnosisAnalyzer:
    """Test suite for LLM Diagnosis Analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return LLMDiagnosisAnalyzer()
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer is not None
        assert analyzer.model_name == "gpt-4"
        assert analyzer.temperature == 0.7
    
    def test_generate_diagnosis_report_positive(self, analyzer):
        """Test diagnosis report generation for positive prediction"""
        features = {
            'feature_0': 65.0,  # Age
            'feature_1': 25.0,  # Tumor size
            'feature_2': 3.0,   # Cancer stage
            'feature_3': 0.8,   # Genetic risk
            'feature_4': 12.0,  # WBC
            'feature_5': 11.0,  # Hemoglobin
            'feature_6': 120.0, # Platelets
            'feature_7': 8.0,   # PSA
            'feature_8': 150.0, # Glucose
            'feature_9': 32.0   # BMI
        }
        
        feature_importance = {
            'feature_0': 0.15,
            'feature_1': 0.25,
            'feature_2': 0.20,
            'feature_3': 0.15,
            'feature_4': 0.10,
            'feature_5': 0.05,
            'feature_6': 0.05,
            'feature_7': 0.03,
            'feature_8': 0.02,
            'feature_9': 0.00
        }
        
        report = analyzer.generate_diagnosis_report(
            features=features,
            prediction=1,
            confidence=0.85,
            feature_importance=feature_importance
        )
        
        assert report is not None
        assert 'diagnosis_summary' in report
        assert 'risk_analysis' in report
        assert 'recommendations' in report
        assert 'feature_summary' in report
        assert 'next_steps' in report
    
    def test_generate_diagnosis_report_negative(self, analyzer):
        """Test diagnosis report generation for negative prediction"""
        features = {
            'feature_0': 35.0,
            'feature_1': 5.0,
            'feature_2': 1.0,
            'feature_3': 0.2,
            'feature_4': 7.0,
            'feature_5': 14.0,
            'feature_6': 200.0,
            'feature_7': 1.5,
            'feature_8': 100.0,
            'feature_9': 24.0
        }
        
        feature_importance = {
            'feature_0': 0.10,
            'feature_1': 0.15,
            'feature_2': 0.15,
            'feature_3': 0.12,
            'feature_4': 0.08,
            'feature_5': 0.08,
            'feature_6': 0.08,
            'feature_7': 0.12,
            'feature_8': 0.07,
            'feature_9': 0.00
        }
        
        report = analyzer.generate_diagnosis_report(
            features=features,
            prediction=0,
            confidence=0.78,
            feature_importance=feature_importance
        )
        
        assert report is not None
        assert 'recommendations' in report
        assert len(report['recommendations']) > 0
    
    def test_build_feature_summary(self, analyzer):
        """Test feature summary building"""
        features = {
            'feature_0': 50.0,
            'feature_1': 15.0,
        }
        
        feature_names = {
            'feature_0': 'Patient Age',
            'feature_1': 'Tumor Size (mm)'
        }
        
        summary = analyzer._build_feature_summary(features, feature_names)
        
        assert len(summary) == 2
        assert summary[0]['feature'] == 'Patient Age'
        assert summary[0]['value'] == 50.0
        assert 'interpretation' in summary[0]
    
    def test_interpret_confidence(self, analyzer):
        """Test confidence interpretation"""
        assert 'Very High' in analyzer._interpret_confidence(0.95)
        assert 'High' in analyzer._interpret_confidence(0.85)
        assert 'Good' in analyzer._interpret_confidence(0.75)
        assert 'Moderate' in analyzer._interpret_confidence(0.65)
        assert 'Low' in analyzer._interpret_confidence(0.45)
    
    def test_analyze_risk_factors(self, analyzer):
        """Test risk factor analysis"""
        features = {
            'feature_0': 70.0,  # High age
            'feature_1': 30.0,  # Large tumor
            'feature_2': 3.0,   # Advanced stage
            'feature_3': 0.9,   # High genetic risk
            'feature_4': 14.0,  # High WBC
        }
        
        feature_importance = {
            'feature_0': 0.20,
            'feature_1': 0.25,
            'feature_2': 0.20,
            'feature_3': 0.20,
            'feature_4': 0.15,
        }
        
        feature_names = {
            'feature_0': 'Patient Age',
            'feature_1': 'Tumor Size',
            'feature_2': 'Cancer Stage',
            'feature_3': 'Genetic Risk',
            'feature_4': 'WBC Count',
        }
        
        risk_analysis = analyzer._analyze_risk_factors(
            features=features,
            feature_names=feature_names,
            feature_importance=feature_importance
        )
        
        assert 'high_risk' in risk_analysis
        assert 'moderate_risk' in risk_analysis
        assert 'low_risk' in risk_analysis
        assert len(risk_analysis['high_risk']) > 0
    
    def test_generate_recommendations_high_risk(self, analyzer):
        """Test recommendation generation for high-risk cases"""
        recommendations = analyzer._generate_recommendations(
            prediction=1,
            confidence=0.9,
            features={'feature_0': 65.0},
            feature_names={'feature_0': 'Patient Age'}
        )
        
        assert len(recommendations) > 0
        assert any('oncologist' in rec.lower() for rec in recommendations)
    
    def test_generate_recommendations_low_risk(self, analyzer):
        """Test recommendation generation for low-risk cases"""
        recommendations = analyzer._generate_recommendations(
            prediction=0,
            confidence=0.85,
            features={'feature_0': 30.0},
            feature_names={'feature_0': 'Patient Age'}
        )
        
        assert len(recommendations) > 0
        assert any('routine' in rec.lower() for rec in recommendations)
    
    def test_suggest_next_steps_high_confidence(self, analyzer):
        """Test next steps suggestion for high confidence"""
        next_steps = analyzer._suggest_next_steps(
            prediction=1,
            confidence=0.95
        )
        
        assert len(next_steps) >= 5
        assert 'oncology' in str(next_steps).lower()
    
    def test_suggest_next_steps_low_confidence(self, analyzer):
        """Test next steps suggestion for low confidence"""
        next_steps = analyzer._suggest_next_steps(
            prediction=1,
            confidence=0.55
        )
        
        assert len(next_steps) >= 5
    
    def test_get_llm_analyzer_singleton(self):
        """Test singleton pattern for analyzer"""
        analyzer1 = get_llm_analyzer()
        analyzer2 = get_llm_analyzer()
        
        assert analyzer1 is analyzer2
    
    def test_assess_risk_level_high(self, analyzer):
        """Test high risk assessment"""
        # Test high age
        risk = analyzer._assess_risk_level('feature_0', 75.0)
        assert risk == 'high'
        
        # Test large tumor
        risk = analyzer._assess_risk_level('feature_1', 35.0)
        assert risk == 'high'
    
    def test_assess_risk_level_moderate(self, analyzer):
        """Test moderate risk assessment"""
        # Test moderate age
        risk = analyzer._assess_risk_level('feature_0', 60.0)
        assert risk == 'moderate'
        
        # Test moderate tumor
        risk = analyzer._assess_risk_level('feature_1', 25.0)
        assert risk == 'moderate'
    
    def test_assess_risk_level_low(self, analyzer):
        """Test low risk assessment"""
        # Test low age
        risk = analyzer._assess_risk_level('feature_0', 35.0)
        assert risk == 'low'
        
        # Test small tumor
        risk = analyzer._assess_risk_level('feature_1', 5.0)
        assert risk == 'low'
    
    def test_interpret_feature_value(self, analyzer):
        """Test individual feature value interpretation"""
        interpretation = analyzer._interpret_feature_value('feature_0', 65.0)
        assert 'age' in interpretation.lower()
        
        interpretation = analyzer._interpret_feature_value('feature_3', 0.8)
        assert 'high' in interpretation.lower() or 'risk' in interpretation.lower()
    
    def test_error_handling(self, analyzer):
        """Test error handling in diagnosis generation"""
        # Test with invalid data
        report = analyzer.generate_diagnosis_report(
            features=None,
            prediction=1,
            confidence=0.8,
            feature_importance={}
        )
        
        # Should return error report
        assert 'error' in report or 'diagnosis_summary' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
