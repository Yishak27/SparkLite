# SparkLite AI - Intelligent Sales Data Analysis Platform

SparkLite AI is a conversational data analysis tool that transforms how you interact with your sales data. Instead of writing complex queries or formulas, simply ask questions in plain English and get instant insights, visualizations, and summaries.

## What Makes SparkLite Special

This isn't just another data visualization tool. SparkLite AI remembers your conversations, learns from your corrections, and provides context-aware responses that get smarter over time. It's like having a data analyst who actually listens and improves with every interaction.

## Key Features

### Smart Conversation Memory
- Remembers your previous questions and corrections
- Builds context from your conversation history
- Learns your preferences and analysis patterns
- Provides more accurate responses based on past interactions

### Natural Language Processing
- Ask questions in plain English: "Show me sales trends by region"
- No need to learn SQL or complex formulas
- Understands business terminology and context
- Handles follow-up questions intelligently

### Automatic Visualizations
- Creates charts and graphs automatically based on your data
- Supports bar charts, line graphs, and pie charts
- Smart chart type selection based on data patterns
- Interactive visualizations using Plotly

### AI-Generated Summaries
- Provides narrative explanations of your data
- Highlights key insights and patterns
- Explains what the numbers actually mean
- Contextualizes findings within your business

### Flexible Data Support
- Upload CSV or JSON files up to 20MB
- Automatic data profiling and structure detection
- Handles various data formats and structures
- Real-time data validation and error handling

## Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for code generation)
- Groq API key (for AI responses)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sparklite-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the root directory:
```
OPEN_AI_KEY=your_openai_api_key_here
GROK_API_KEY=your_groq_api_key_here
```

4. Run the application:
```bash
streamlit run main.py
```

## How to Use

### 1. Upload Your Data
- Click "Browse files" and select your CSV or JSON file
- Maximum file size: 20MB
- Supported formats: CSV, JSON (flat or nested)

### 2. Explore Your Data
Once uploaded, you'll see:
- Total rows and columns
- First 5 rows preview
- Column information with data types
- Null value counts

### 3. Start Asking Questions
Try questions like:
- "What are the total sales by region?"
- "Show me the top 10 products by revenue"
- "Which sales person performed best last month?"
- "Create a chart showing sales trends over time"

### 4. Get Intelligent Responses
For each question, you'll receive:
- **Analysis Results**: Tables, numbers, or text answers
- **Visualizations**: Automatic charts when relevant
- **AI Summary**: Plain English explanation of findings
- **Generated Code**: View the Python code that created the analysis

## Example Use Cases

### Sales Performance Analysis
```
"Show me total sales by region"
"Which products have the highest profit margins?"
"Compare this quarter's performance to last quarter"
```

### Customer Insights
```
"Who are our top 5 customers by revenue?"
"What's the average order value by customer segment?"
"Show customer retention rates over time"
```

### Product Analysis
```
"Which products are selling best?"
"Show inventory turnover by product category"
"What's the seasonal trend for each product line?"
```

## Technical Architecture

### Core Components

**Natural Language Service** (`services/natural_language_service.py`)
- Handles conversation flow and context management
- Processes user queries and maintains chat history
- Manages memory and learning from corrections

**Code Generator** (`services/code_generator.py`)
- Converts natural language to Python/Pandas code
- Executes analysis code safely in isolated environment
- Formats results for display

**AI Generator** (`services/ai_generator.py`)
- Manages API connections to Groq/OpenAI
- Handles API key rotation for reliability
- Provides safe completion methods

**Visualization Engine** (`services/visualization.py`)
- Automatically detects appropriate chart types
- Creates interactive Plotly visualizations
- Supports bar, line, and pie charts

**AI Narration** (`services/ai_naration.py`)
- Generates human-readable summaries
- Explains data insights in business context
- Provides two-sentence explanations of findings

### Data Flow
1. User uploads data file (CSV/JSON)
2. System profiles data structure and columns
3. User asks question in natural language
4. AI converts question to Python/Pandas code
5. Code executes safely against the data
6. Results are formatted and visualized
7. AI generates narrative summary
8. Everything is displayed in an organized interface

## Configuration

### Streamlit Configuration
The app uses custom Streamlit configuration in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Environment Variables
- `OPEN_AI_KEY`: OpenAI API key for code generation
- `GROK_API_KEY`: Groq API key(s) for AI responses (comma-separated for multiple keys)

## Memory and Context Management

SparkLite AI maintains several types of memory:

### Conversation History
- Stores last 20 messages with timestamps
- Provides context for follow-up questions
- Enables reference to previous analyses

### Correction Learning
- Remembers when you correct or clarify responses
- Applies learned corrections to future similar questions
- Improves accuracy over time

### Analysis Patterns
- Tracks types of analyses you perform most
- Remembers successful code patterns
- Suggests relevant follow-up questions

## Troubleshooting

### Common Issues

**File Upload Problems**
- Ensure file is under 20MB
- Check that CSV has proper headers
- Verify JSON structure is valid

**API Key Issues**
- Verify API keys are correctly set in `.env`
- Check API key permissions and quotas
- Ensure no extra spaces in environment variables

**Analysis Errors**
- Try rephrasing your question more specifically
- Reference actual column names from your data
- Use the "Clear History" button to reset context

### Getting Help
- Check the generated code to understand what went wrong
- Use conversation history to see previous successful patterns
- Try simpler questions first, then build complexity

## Contributing

This project welcomes contributions! Areas where you can help:

- Adding new visualization types
- Improving natural language understanding
- Enhancing memory and context features
- Adding support for more data formats
- Optimizing performance for larger datasets

## Developer Information

**Created by**: Ermiyas Developer  
**Website**: https://ermiyas.dev  
**Contact**: inbox@ermiyas.dev  

SparkLite AI was built with a focus on making data analysis accessible to everyone, regardless of technical background. The goal is to democratize data insights through conversational AI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*SparkLite AI - Making data analysis as easy as having a conversation.*