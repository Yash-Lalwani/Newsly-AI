# Newsly.AI - News Aggregator

A clean, modular Streamlit news aggregator application with sentiment analysis and AI-powered insights.

## Project Structure

```
News-Aggregator/
├── app.py              # Main application entry point
├── components.py       # UI components and layout functions
├── news_utils.py       # News fetching and processing utilities
├── visualizations.py   # Data visualization and charts
├── chat_bot.py         # AI chat assistant functionality
├── style.css          # Custom CSS styling
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Module Organization

### `app.py`
- Main application entry point
- Coordinates all modules and renders the complete interface
- Handles user input and orchestrates data flow

### `components.py`
- UI components and layout functions
- Header, hero section, navigation tabs
- Article cards and search sections
- CSS loading functionality

### `news_utils.py`
- News fetching and processing utilities
- RSS URL construction
- Sentiment analysis
- Time formatting and source icon extraction
- Chat query parsing

### `visualizations.py`
- Data visualization components
- Word cloud generation
- Keyword frequency charts
- Sentiment distribution charts
- Insights section rendering

### `chat_bot.py`
- AI chat assistant functionality
- Chat interface rendering
- Message handling and history
- News search integration

### `style.css`
- Complete CSS styling separated from Python code
- Dark theme implementation
- Responsive design
- Component-specific styling

## Features

- **Multi-keyword Search**: Search for news using up to 3 keywords
- **Sentiment Analysis**: AI-powered sentiment analysis of headlines
- **Interactive Visualizations**: Word clouds, keyword frequency, and sentiment distribution charts
- **Chat Assistant**: AI chatbot for natural language news queries
- **Advanced Filtering**: Sort and filter articles by date, sentiment, and relevance
- **Responsive Design**: Clean, modern UI that works on all devices

## Installation and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser to the displayed URL (typically `http://localhost:8501`)

## Development

The codebase is now modular and easy to maintain:

- Add new UI components in `components.py`
- Extend news processing functionality in `news_utils.py`
- Create new visualizations in `visualizations.py`
- Enhance the chat bot in `chat_bot.py`
- Modify styling in `style.css`

Each module has clear responsibilities and can be developed independently while maintaining the overall application functionality.