# Usage Examples

This document provides examples of how to use OctoCase for different scenarios.

## Command Line Examples

### Basic Usage
```bash
# Generate test cases with default login requirement
python test_case_generator.py

# Generate test cases for custom requirement
python test_case_generator.py -r "User can upload files up to 10MB in size"

# Generate CSV output
python test_case_generator.py -f csv -o my_test_cases

# Generate Excel output with custom requirement
python test_case_generator.py -f excel -r "User can search products by name and category" -o product_search_tests
```

### Using with OpenAI API
```bash
# Set environment variable
export OPENAI_API_KEY="your_actual_api_key_here"

# Or pass directly
python test_case_generator.py --openai-key "your_actual_api_key_here" -r "User authentication with 2FA"
```

### Using with Hugging Face
```bash
# Use Hugging Face provider (requires additional setup)
python test_case_generator.py -p huggingface -r "File download functionality"
```

## Jupyter Notebook Examples

### Quick Start
1. Open `test_case_generator.ipynb`
2. Run all cells with default configuration
3. Modify the requirement in the "Generate Test Cases" section
4. Re-run the generation and export cells

### Custom Requirements
```python
# Example requirements to test
requirements = [
    "User can log in with valid username and password. If incorrect, an error message appears.",
    "User can upload profile picture (JPEG, PNG) up to 5MB",
    "Shopping cart allows adding, removing, and updating item quantities",
    "Password reset via email verification link",
    "User can filter products by price range, category, and rating"
]
```

## Sample Output

### Generated Test Cases Structure
Each test case includes:
- **Test Case ID**: Unique identifier (TC_001, TC_002, etc.)
- **Requirement**: Specific functionality being tested
- **Step**: Detailed test execution steps
- **Expected Result**: What should happen when test is executed
- **Priority**: High/Medium/Low based on criticality

### Example Test Case
```
Test Case ID: TC_001
Requirement: Valid user login with correct credentials
Step: 1. Navigate to login page
      2. Enter valid username
      3. Enter valid password  
      4. Click login button
Expected Result: User is successfully logged in and redirected to dashboard
Priority: High
```

## Integration with Test Management Tools

### Excel/CSV Import
The generated files can be imported into:
- TestRail
- Zephyr
- qTest
- Azure DevOps Test Plans
- Jira Test Management

### Custom Field Mapping
You can modify the column names in the code to match your test management tool:
```python
# Customize column names
df.rename(columns={
    'test_case_id': 'Test ID',
    'requirement': 'Summary',
    'step': 'Test Steps',
    'expected_result': 'Expected Results',
    'priority': 'Priority'
}, inplace=True)
```

## Advanced Configuration

### Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGING_FACE_API_KEY=your_hf_api_key_here
```

### Custom Prompts
Modify the prompt in `test_case_generator.py` for domain-specific requirements:
```python
prompt = f"""
Generate test cases for {domain} application:
Requirement: {requirement}
Focus on: {specific_areas}
Include: {test_types}
"""
```

## Best Practices

1. **Clear Requirements**: Write detailed, unambiguous requirements
2. **Review Generated Cases**: Always review and refine AI-generated test cases
3. **Domain Context**: Add domain-specific context to prompts for better results
4. **Iterative Refinement**: Use generated cases as a starting point, not final output
5. **Security Testing**: Ensure security test cases are included for critical features

## Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure your API keys are correctly set
2. **Import Errors**: Install required dependencies with `pip install -r requirements.txt`
3. **Empty Output**: Check your requirement text is descriptive enough
4. **Format Issues**: Verify output file permissions and disk space

### Getting Help
- Check the GitHub issues for common problems
- Review the API documentation for OpenAI/Hugging Face
- Ensure your Python environment has all required packages