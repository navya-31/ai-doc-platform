# AI-Assisted Document Authoring Platform

A full-stack web application that enables users to generate, refine, and export professional business documents (Word .docx and PowerPoint .pptx) using AI-powered content generation.

## 🎯 Features

### Core Features
- **User Authentication**: Secure JWT-based registration and login
- **Project Management**: Create and manage multiple document projects
- **Document Types**: Support for both Word (.docx) and PowerPoint (.pptx)
- **AI Content Generation**: Section-by-section content generation using Google Gemini API
- **Interactive Refinement**: Edit and refine content with AI assistance
- **Feedback System**: Like/dislike and comment on generated content
- **Revision History**: Track all AI-powered edits and refinements
- **Document Export**: Export finished documents in native formats

### Bonus Features
- **AI-Suggested Outlines**: Generate document structure automatically from topic
- **Drag-and-Drop Reordering**: Organize sections/slides easily

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT with PyJWT
- **AI Integration**: Google Gemini API
- **Document Generation**: python-docx, python-pptx

### Frontend
- **HTML/CSS/JavaScript**: Vanilla JS with Bootstrap 5
- **API Communication**: Fetch API
- **State Management**: LocalStorage for auth tokens

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key (get from [Google AI Studio](https://aistudio.google.com/app/apikey))
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-doc-platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=your_api_key_here

# JWT Configuration (Optional - defaults provided)
JWT_SECRET=your_secret_key_here
JWT_EXPIRE_HOURS=24

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///data.db

# Server Port (Optional)
PORT=5000
```

**Important**: Get your Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Initialize Database
```bash
python app.py
# This will automatically create the database and tables on first run
```

## Running the Application

### Start the Backend Server
```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

### Access the Frontend

Open your web browser and navigate to:
```
http://127.0.0.1:5000/index.html
```

Or open the HTML files directly in your browser:
- `index.html` - Login/Registration
- `dashboard.html` - Project Dashboard
- `configure.html` - Project Configuration
- `editor.html` - Content Editor

## Usage Guide

### 1. User Registration & Login
1. Open `index.html`
2. Register a new account with email and password
3. Login with your credentials

### 2. Create a New Project
1. Click "Create New Project" on the dashboard
2. Select document type (Word or PowerPoint)
3. Enter your main topic
4. Click "AI-Suggest Outline" (optional) or manually add sections/slides
5. Click "Create Project & Continue"

### 3. Generate Content
1. In the editor, click "Generate Content (LLM)"
2. Wait for AI to generate content for each section/slide
3. Review the generated content

### 4. Refine Content
1. Click "AI Refine" on any section
2. Enter refinement instructions (e.g., "Make more formal", "Add bullet points")
3. Review the refined content
4. Use Like/Dislike buttons to provide feedback
5. Add comments for notes

### 5. View Revision History
1. Click "History" on any section
2. View all previous versions and refinement instructions
3. Track changes over time

### 6. Export Document
1. Click "Export .docx" or "Export .pptx"
2. Download the generated document
3. Open in Microsoft Word or PowerPoint

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Projects
- `GET /api/projects` - List all user projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects/suggest-outline` - AI-generate outline (Bonus)
- `POST /api/projects/{id}/generate` - Generate content for all sections
- `GET /api/projects/{id}/export?type=docx|pptx` - Export document

### Sections
- `POST /api/projects/{id}/sections` - Add new section
- `POST /api/sections/{id}/refine` - Refine section content
- `POST /api/sections/{id}/feedback` - Like/dislike/comment
- `GET /api/sections/{id}/history` - Get revision history

## Project Structure

```
ai-doc-platform/
│── backend/
│ ├── app.py
│ ├── auth.py
│ ├── llm.py
│ ├── models.py
│ ├── export_docx.py
│ ├── export_pptx.py
│ ├── db.py
│ ├── requirements.txt
│ └── data.db
│
└── frontend/
├── index.html
├── dashboard.html
├── editor.html
├── script.js
└── styles.css (optional)
```

## Environment Variables

| Variable    | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | - | Google Gemini API key |
| `JWT_SECRET` | ❌ No | `change_this_secret` | Secret key for JWT tokens |
| `JWT_EXPIRE_HOURS` | ❌ No | `24` | JWT token expiration time |
| `DATABASE_URL` | ❌ No | `sqlite:///data.db` | Database connection string |
| `PORT` | ❌ No | `5000` | Server port |

##Testing the API

### Test Gemini Connection
```bash
python test_gemini.py
```

### List Available Models
```bash
python list_models.py
```

## Troubleshooting

### Gemini API Not Working
1. Verify your API key in `.env`
2. Run `python test_gemini.py` to check connectivity
3. Ensure you have API access enabled in Google AI Studio
4. Check if billing is enabled (if required)

### Database Issues
```bash
# Delete and recreate database
rm data.db
python app.py
```

### CORS Errors
- Make sure Flask-CORS is installed
- Check that the frontend is accessing the correct API URL

### Export Not Working
- Verify `python-docx` and `python-pptx` are installed
- Check file permissions in the project directory

## Notes

- The application uses SQLite by default (suitable for development)
- For production, consider using PostgreSQL or MySQL
- JWT tokens expire after 24 hours by default
- All generated content is stored in the database
- Revision history is maintained for all AI refinements

## Demo Video

Create a 5-10 minute demo video showing:
1. User registration and login
2. Creating a Word document project
3. Creating a PowerPoint project
4. AI outline suggestion (bonus feature)
5. Content generation
6. Content refinement with AI
7. Using like/dislike and comments
8. Viewing revision history
9. Exporting documents

## License

This project is created as part of an assignment evaluation.

## Support

For issues or questions, please refer to the troubleshooting section or check the API documentation.

---

**Built with ❤️ using Flask, Gemini AI, and modern web technologies**