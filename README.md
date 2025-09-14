# OctoCase - AI-Powered Test Case Generator

An automated test case generation system that uses AI/LLM technology to generate comprehensive test cases for software functionality, specifically designed for login systems.

## Features

- **AI-Powered Generation**: Uses OpenAI GPT models or Hugging Face transformers to generate test cases
- **Structured Output**: Exports test cases to Excel/CSV with standardized columns
- **Comprehensive Coverage**: Generates systematic test cases covering various scenarios
- **Time-Saving**: Automates manual test case writing for QA engineers
- **Easy Integration**: Jupyter Notebook interface for interactive use

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fdhliakbar/OctoCase.git
cd OctoCase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

1. Open the Jupyter Notebook:
```bash
jupyter notebook test_case_generator.ipynb
```

2. Configure your API keys in the notebook or .env file

3. Define your requirements (example provided for login functionality)

4. Run the cells to generate test cases

5. Export results to Excel/CSV format

## Test Case Output Format

The generated test cases include the following columns:
- **Test Case ID**: Unique identifier for each test case
- **Requirement**: The specific requirement being tested
- **Step**: Detailed steps to execute the test
- **Expected Result**: Expected outcome of the test
- **Priority**: Test priority level (Low/Medium/High)

## Example

For a login requirement: "The user can log in with a valid username and password. If incorrect, an error message appears."

The system generates comprehensive test cases covering:
- Valid login scenarios
- Invalid username/password combinations
- Error message validation
- Edge cases and boundary conditions

## License

This project is licensed under the MIT License - see the LICENSE file for details.