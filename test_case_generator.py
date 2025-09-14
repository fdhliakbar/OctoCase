#!/usr/bin/env python3
"""
OctoCase - AI-Powered Test Case Generator
Command-line version of the test case generator
"""

import pandas as pd
import json
import os
import re
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

# For environment variables
from dotenv import load_dotenv
load_dotenv()


class TestCaseGenerator:
    def __init__(self, use_openai=True, openai_key=None, hf_key=None):
        self.use_openai = use_openai
        self.openai_key = openai_key
        self.hf_key = hf_key
        
        if use_openai:
            self._setup_openai()
        else:
            self._setup_huggingface()
    
    def _setup_openai(self):
        """Setup OpenAI client"""
        try:
            import openai
            if self.openai_key and self.openai_key != 'your_openai_api_key_here':
                self.client = openai.OpenAI(api_key=self.openai_key)
                print("✅ OpenAI client initialized successfully")
            else:
                print("⚠️ OpenAI API key not provided. Using fallback generation.")
                self.client = None
        except ImportError:
            print("❌ OpenAI library not installed. Run: pip install openai")
            print("Using fallback generation...")
            self.client = None
    
    def _setup_huggingface(self):
        """Setup Hugging Face pipeline"""
        try:
            from transformers import pipeline
            # Using a smaller, efficient model for text generation
            self.pipeline = pipeline(
                "text-generation", 
                model="microsoft/DialoGPT-medium",
                max_length=512
            )
            print("✅ Hugging Face pipeline initialized successfully")
        except ImportError:
            print("❌ Transformers library not installed. Run: pip install transformers torch")
            print("Using fallback generation...")
            self.pipeline = None
    
    def generate_test_cases_openai(self, requirement: str) -> List[Dict]:
        """Generate test cases using OpenAI"""
        if not self.client:
            return self._generate_fallback_test_cases(requirement)
        
        prompt = f"""
Generate comprehensive test cases for the following requirement:

Requirement: {requirement}

Please generate test cases in JSON format with the following structure:
[
  {{
    "test_case_id": "TC_001",
    "requirement": "Specific requirement being tested",
    "step": "Detailed test steps",
    "expected_result": "Expected outcome",
    "priority": "High/Medium/Low"
  }}
]

Include positive test cases, negative test cases, edge cases, and boundary conditions.
Generate at least 8-10 comprehensive test cases.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a QA expert specializing in creating comprehensive test cases. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Extract JSON from the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                test_cases = json.loads(json_match.group())
                return test_cases
            else:
                print("⚠️ Could not parse JSON from OpenAI response. Using fallback.")
                return self._generate_fallback_test_cases(requirement)
                
        except Exception as e:
            print(f"❌ Error with OpenAI API: {e}")
            return self._generate_fallback_test_cases(requirement)
    
    def generate_test_cases_huggingface(self, requirement: str) -> List[Dict]:
        """Generate test cases using Hugging Face (with fallback logic)"""
        if not self.pipeline:
            return self._generate_fallback_test_cases(requirement)
        
        # For this demo, we'll use the fallback method as HF free models 
        # are not as effective for structured JSON generation
        print("ℹ️ Using rule-based generation (HF models work better with API access)")
        return self._generate_fallback_test_cases(requirement)
    
    def _generate_fallback_test_cases(self, requirement: str) -> List[Dict]:
        """Generate test cases using rule-based approach when AI is not available"""
        
        # Parse requirement to understand the functionality
        is_login = 'login' in requirement.lower() or 'log in' in requirement.lower()
        has_username = 'username' in requirement.lower()
        has_password = 'password' in requirement.lower()
        has_error = 'error' in requirement.lower()
        
        test_cases = []
        
        if is_login:
            # Generate login-specific test cases
            base_cases = [
                {
                    "test_case_id": "TC_001",
                    "requirement": "Valid user login with correct credentials",
                    "step": "1. Navigate to login page\n2. Enter valid username\n3. Enter valid password\n4. Click login button",
                    "expected_result": "User is successfully logged in and redirected to dashboard",
                    "priority": "High"
                },
                {
                    "test_case_id": "TC_002",
                    "requirement": "Invalid login with incorrect username",
                    "step": "1. Navigate to login page\n2. Enter invalid username\n3. Enter valid password\n4. Click login button",
                    "expected_result": "Error message displayed: 'Invalid username or password'",
                    "priority": "High"
                },
                {
                    "test_case_id": "TC_003",
                    "requirement": "Invalid login with incorrect password",
                    "step": "1. Navigate to login page\n2. Enter valid username\n3. Enter invalid password\n4. Click login button",
                    "expected_result": "Error message displayed: 'Invalid username or password'",
                    "priority": "High"
                },
                {
                    "test_case_id": "TC_004",
                    "requirement": "Login with empty username field",
                    "step": "1. Navigate to login page\n2. Leave username field empty\n3. Enter valid password\n4. Click login button",
                    "expected_result": "Error message displayed: 'Username is required'",
                    "priority": "Medium"
                },
                {
                    "test_case_id": "TC_005",
                    "requirement": "Login with empty password field",
                    "step": "1. Navigate to login page\n2. Enter valid username\n3. Leave password field empty\n4. Click login button",
                    "expected_result": "Error message displayed: 'Password is required'",
                    "priority": "Medium"
                },
                {
                    "test_case_id": "TC_006",
                    "requirement": "Login with both fields empty",
                    "step": "1. Navigate to login page\n2. Leave both username and password fields empty\n3. Click login button",
                    "expected_result": "Error messages displayed for both required fields",
                    "priority": "Medium"
                },
                {
                    "test_case_id": "TC_007",
                    "requirement": "Login with special characters in username",
                    "step": "1. Navigate to login page\n2. Enter username with special characters (!@#$%)\n3. Enter valid password\n4. Click login button",
                    "expected_result": "System handles special characters appropriately or shows validation error",
                    "priority": "Low"
                },
                {
                    "test_case_id": "TC_008",
                    "requirement": "Login with SQL injection attempt",
                    "step": "1. Navigate to login page\n2. Enter SQL injection string in username (e.g., ' OR '1'='1)\n3. Enter any password\n4. Click login button",
                    "expected_result": "Login fails securely, no SQL injection vulnerability",
                    "priority": "High"
                },
                {
                    "test_case_id": "TC_009",
                    "requirement": "Login with maximum length username",
                    "step": "1. Navigate to login page\n2. Enter username at maximum allowed length\n3. Enter valid password\n4. Click login button",
                    "expected_result": "System accepts or rejects based on validation rules",
                    "priority": "Low"
                },
                {
                    "test_case_id": "TC_010",
                    "requirement": "Case sensitivity test for username",
                    "step": "1. Navigate to login page\n2. Enter valid username in different case (upper/lower)\n3. Enter valid password\n4. Click login button",
                    "expected_result": "Login success/failure based on system case sensitivity rules",
                    "priority": "Medium"
                }
            ]
            test_cases.extend(base_cases)
        else:
            # Generic test cases for other requirements
            test_cases = [
                {
                    "test_case_id": "TC_001",
                    "requirement": f"Positive test case for: {requirement}",
                    "step": "1. Perform the required action with valid inputs\n2. Verify the functionality works as expected",
                    "expected_result": "The functionality works as specified in the requirement",
                    "priority": "High"
                },
                {
                    "test_case_id": "TC_002",
                    "requirement": f"Negative test case for: {requirement}",
                    "step": "1. Perform the required action with invalid inputs\n2. Verify error handling",
                    "expected_result": "Appropriate error message is displayed",
                    "priority": "High"
                }
            ]
        
        return test_cases
    
    def generate_test_cases(self, requirement: str) -> List[Dict]:
        """Main method to generate test cases"""
        print(f"Generating test cases for: {requirement}")
        
        if self.use_openai:
            return self.generate_test_cases_openai(requirement)
        else:
            return self.generate_test_cases_huggingface(requirement)


def export_test_cases(test_cases_df, filename, format_type='excel'):
    """
    Export test cases to Excel or CSV format
    """
    try:
        if format_type.lower() == 'excel':
            filename_with_ext = f"{filename}.xlsx"
            
            # Create Excel writer with formatting
            with pd.ExcelWriter(filename_with_ext, engine='openpyxl') as writer:
                test_cases_df.to_excel(writer, sheet_name='Test Cases', index=False)
                
                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Test Cases']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
            print(f"✅ Test cases exported to {filename_with_ext}")
            
        elif format_type.lower() == 'csv':
            filename_with_ext = f"{filename}.csv"
            test_cases_df.to_csv(filename_with_ext, index=False)
            print(f"✅ Test cases exported to {filename_with_ext}")
            
        else:
            print("❌ Unsupported format. Use 'excel' or 'csv'")
            return None
            
        return filename_with_ext
        
    except Exception as e:
        print(f"❌ Error exporting test cases: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='OctoCase - AI-Powered Test Case Generator')
    parser.add_argument('--requirement', '-r', type=str, 
                       default="The user can log in with a valid username and password. If incorrect, an error message appears.",
                       help='Requirement text to generate test cases for')
    parser.add_argument('--format', '-f', choices=['excel', 'csv'], default='excel',
                       help='Output format (excel or csv)')
    parser.add_argument('--output', '-o', type=str, 
                       default=f'test_cases_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                       help='Output filename (without extension)')
    parser.add_argument('--provider', '-p', choices=['openai', 'huggingface'], default='openai',
                       help='AI provider to use')
    parser.add_argument('--openai-key', type=str, help='OpenAI API key')
    parser.add_argument('--hf-key', type=str, help='Hugging Face API key')
    
    args = parser.parse_args()
    
    # Configuration
    use_openai = args.provider == 'openai'
    openai_key = args.openai_key or os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    hf_key = args.hf_key or os.getenv('HUGGING_FACE_API_KEY', 'your_hugging_face_api_key_here')
    
    print("🚀 OctoCase - AI-Powered Test Case Generator")
    print("=" * 50)
    print(f"Provider: {'OpenAI' if use_openai else 'Hugging Face'}")
    print(f"Output format: {args.format}")
    print(f"Output filename: {args.output}")
    print()
    
    # Initialize generator
    generator = TestCaseGenerator(
        use_openai=use_openai,
        openai_key=openai_key,
        hf_key=hf_key
    )
    
    # Generate test cases
    test_cases = generator.generate_test_cases(args.requirement)
    
    if not test_cases:
        print("❌ No test cases generated. Please check your configuration.")
        return
    
    print(f"\n✅ Generated {len(test_cases)} test cases successfully!")
    
    # Create DataFrame
    df = pd.DataFrame(test_cases)
    
    # Show summary
    print(f"\n📊 Test Case Summary:")
    print(f"Total test cases: {len(df)}")
    priority_counts = df['priority'].value_counts()
    print("Priority distribution:")
    for priority, count in priority_counts.items():
        print(f"  {priority}: {count} test cases")
    
    # Export
    exported_file = export_test_cases(df, args.output, args.format)
    
    if exported_file:
        print(f"\n📄 File created: {exported_file}")
        print("🎉 Test case generation completed successfully!")
    else:
        print("❌ Failed to export test cases.")


if __name__ == "__main__":
    main()