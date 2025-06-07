# 📄 PDF Search App with FAISS and MySQL

A powerful Flask web application that enables intelligent semantic search within PDF documents using AI embeddings and vector similarity search.

## 🎯 What This App Does

This application allows you to:
- **Upload PDF files** through a web interface
- **Extract and process text** from PDF documents
- **Convert text into AI embeddings** using state-of-the-art language models
- **Store embeddings** in a FAISS vector database for lightning-fast search
- **Perform semantic search** - find relevant content even when exact keywords don't match
- **Track usage** with MySQL database logging
- **Get instant results** with relevant passages highlighted

## ✨ Key Features

- 📤 **Easy PDF Upload**: Drag-and-drop or click to upload PDF files
- 🧠 **AI-Powered Search**: Uses Sentence Transformers for semantic understanding
- ⚡ **Lightning Fast**: FAISS vector search returns results in milliseconds
- 📊 **Usage Analytics**: MySQL database tracks all uploads and searches
- 🎨 **Clean Interface**: Modern, responsive web design
- 🔍 **Smart Results**: Returns most relevant text passages with similarity scores

## 🏗️ Project Architecture

```
pdf_faiss_app/
├── app.py                 # Main Flask application
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── style.css         # Web interface styling
├── templates/
│   └── index.html        # Web interface template
├── faiss_index/
│   └── faiss_handler.py  # FAISS vector operations
├── pdf_processor/
│   └── extract.py        # PDF text extraction
└── database/
    └── db.py             # MySQL database operations
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Flask (Python) | Web framework and API |
| **AI/ML** | Sentence Transformers | Text embedding generation |
| **Vector DB** | FAISS | Fast similarity search |
| **Database** | MySQL | Metadata and query logging |
| **Frontend** | HTML/CSS/JavaScript | User interface |
| **PDF Processing** | PyPDF2 | Text extraction from PDFs |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher** ([Download Python](https://www.python.org/downloads/))
- **MySQL Server** ([Download MySQL](https://dev.mysql.com/downloads/mysql/))
- **pip** (Python package installer - comes with Python)
- **Git** (optional, for cloning)

## 🚀 Installation & Setup

### Step 1: Get the Code

**Option A: Clone from Git**
```bash
git clone https://github.com/yourusername/pdf-faiss-app.git
cd pdf-faiss-app
```

**Option B: Download ZIP**
- Download the project files
- Extract to a folder named `pdf-faiss-app`
- Navigate to the folder

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- Flask (web framework)
- mysql-connector-python (MySQL database connection)
- sentence-transformers (AI embeddings)
- faiss-cpu (vector search)
- PyPDF2 (PDF processing)
- python-dotenv (environment variables)

### Step 4: Set Up MySQL Database

#### 4.1 Start MySQL Server
- **Windows**: Start MySQL from Services or MySQL Workbench
- **macOS**: `brew services start mysql` (if using Homebrew)
- **Linux**: `sudo systemctl start mysql`

#### 4.2 Create Database and Tables
```bash
# Connect to MySQL
mysql -u root -p
# Enter your MySQL root password when prompted
```

```sql
-- Create the database
CREATE DATABASE pdf_db;

-- Use the database
USE pdf_db;

-- Create table for PDF metadata
CREATE TABLE pdfs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for search queries
CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pdf_id INT,
    query TEXT NOT NULL,
    result TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pdf_id) REFERENCES pdfs(id)
);

-- Exit MySQL
EXIT;
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory:

```ini
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DB=pdf_db

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

⚠️ **Important**: Replace `your_mysql_password_here` with your actual MySQL root password.

### Step 6: Run the Application

```bash
# Make sure your virtual environment is activated
# Start the Flask app
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 7: Open in Browser

Navigate to: http://127.0.0.1:5000

## 📖 How to Use

### 1. Upload a PDF
- Click "Choose File" or drag-and-drop a PDF
- Click "Upload and Process"
- Wait for processing (may take 30-60 seconds for large PDFs)

### 2. Search Your Document
- Enter your question in natural language
- Examples:
  - "What are the main conclusions?"
  - "Tell me about the methodology"
  - "What are the key findings?"
- Click "Search"

### 3. Review Results
- See the most relevant text passages
- Results are ranked by relevance
- Each result shows similarity score

## 🧪 Testing & Verification

### Test Database Connection
Visit: http://127.0.0.1:5000/test-db

This will:
- Test MySQL connection
- Insert sample data
- Confirm everything is working

### Test Upload Process
1. Try uploading a small PDF (1-2 pages)
2. Check for success message
3. Try searching for content you know is in the PDF

## 🔧 Troubleshooting

### Common Issues and Solutions

#### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### MySQL connection errors
- Check MySQL server is running
- Verify credentials in `.env` file
- Test connection: `mysql -u root -p`

#### FAISS installation issues
```bash
# Try installing CPU version specifically
pip install faiss-cpu
```

#### PDF processing errors
- Ensure PDF is not password-protected
- Try with a different PDF file
- Check file permissions

#### Port 5000 already in use
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows (then kill PID)
```

## 📊 Performance Tips

### For Large PDFs
- PDFs over 100 pages may take several minutes to process
- Consider splitting very large documents
- Processing happens once; searching is always fast

### For Better Search Results
- Use descriptive, specific queries
- Try different phrasings if results aren't relevant
- Longer queries often work better than single keywords

## 🔒 Security Considerations

- The app runs in development mode by default
- For production deployment:
  - Set `FLASK_ENV=production`
  - Use a proper WSGI server (gunicorn, uWSGI)
  - Implement file upload restrictions
  - Add authentication if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 File Structure Details

### Core Files
- **`app.py`**: Main Flask application with all routes
- **`requirements.txt`**: Python package dependencies
- **`.env`**: Environment variables (you create this)

### Modules
- **`faiss_index/faiss_handler.py`**: Handles vector storage and similarity search
- **`pdf_processor/extract.py`**: Extracts text from PDF files
- **`database/db.py`**: MySQL database operations and queries

### Frontend
- **`templates/index.html`**: Web interface HTML
- **`static/style.css`**: Styling and layout

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## 🆘 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Verify all prerequisites** are installed correctly  
3. **Test with a simple PDF** first
4. **Check the console/terminal** for error messages
5. **Open an issue** on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Error messages
   - Steps to reproduce

## 🚀 What's Next?

Potential enhancements:
- Support for multiple file formats (Word, text files)
- User authentication and file management
- Advanced search filters
- API endpoints for integration
- Docker containerization
- Cloud deployment guides

---

**Happy Searching!** 🔍✨
