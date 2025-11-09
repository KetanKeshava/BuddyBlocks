# Focus Flow

A productivity application built with Streamlit to help you manage your focus and workflow efficiently.

## Description

Focus Flow is a comprehensive productivity companion that helps users track their tasks, manage their time, and maintain focus throughout their workday. The application leverages Streamlit for an intuitive user interface and integrates with Snowflake for robust data management.

## Project Structure

```
focus-flow/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── utils/                          # Helper functions and utilities
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

## Technologies Used

- **Streamlit**: Web application framework
- **Snowflake**: Data storage and management
- **Pandas**: Data manipulation
- **pyttsx3**: Text-to-speech functionality

## License

This project is licensed under the MIT License.
