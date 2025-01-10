# Social Media Performance Analytics

## Overview
This project leverages the power of Langflow, DataStax Astra DB, and GPT to analyze and generate insights from mock social media engagement data. By simulating various post types like carousels, reels, and static images, the system fetches and processes engagement metrics to provide actionable insights.

This solution enables content creators and social media managers to gain data-driven insights through automated analysis of post performance across different content types.

## Project Structure
```
social-media-performance-analytics/
├── backend/                      # Fast API backend server
│   ├── main.py                  # Main server implementation
│   └── requirements.txt         # Backend dependencies
├── chat-app-ui/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── types/             # TypeScript type definitions
│   │   └── assets/            # Static assets
│   └── package.json           # Frontend dependencies
├── proof-of-concept/           # PoC implementation
│   ├── src/
│   │   ├── analytics/         # Analytics processing & prompt generation
│   │   ├── config/           # Astra DB Configuration management
│   │   ├── data/            # Mock data generation and handling
│   │   └── db/              # Astra DB operations
│   └── requirements.txt      # PoC dependencies
├── scripts/               # Utility scripts to run langflow project locally
└── social-media-performance-analytics-langflow-config.json
```

## Technical Components

### PoC Components
1. **Analytics Processor**
   - Handles social media metrics processing
   - Calculates engagement rates
   - Generates GPT prompt

2. **Astra DB Integration**
   - Manages database connections
   - Handles data persistence
   - Executes database queries

3. **Mock Data Generator**
   - Generates test data for:
     - Multiple post types (carousel, reel, static)
     - Engagement metrics
     - Time-distributed posts

### Frontend Components
- React-based chat interface
- TypeScript implementation
- Real-time analytics visualization

## Prerequisites
- Python version >=3.12
- Node.js version >=20
- Langflow installation
- DataStax Astra DB account
- Required Python packages (see `requirements.txt`)

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd chat-app-ui
npm install
npm run dev
```

### Database Configuration
1. Set up Astra DB credentials in `proof-of-concept/src/db_creds/`
2. Configure database connection in `proof-of-concept/src/config/astra_config.py`

## Usage

### Running the Application
1. Start the backend server:
```bash
python backend/main.py
```

2. Launch the frontend:
```bash
cd chat-app-ui
npm run dev
```

## Data Schema
```sql
CREATE TABLE social_media_analytics.posts (
    post_type text,
    posted_at timestamp,
    post_id text,
    likes int,
    shares int,
    comments int,
    PRIMARY KEY ((post_type), posted_at, post_id)
)
```

### Project Configuration
- Langflow configuration file: `social-media-performance-analytics-langflow-config.json`
- Environment variables: Create `.env` file based on `.env.example`

## Features
- Real-time analytics processing
- Multi-platform social media data analysis
- Custom analytics components
- Interactive chat interface
- Mock data generation for testing
- Scalable data storage with Astra DB
- GPT-powered insights generation

## Best Practices
- Regular testing and validation
- Consistent code formatting
- Documentation maintenance
- Database backup procedures
- Security best practices implementation