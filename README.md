# EDM Agentic Workflow

An automated, three-phase agentic workflow orchestrated via **n8n** that streamlines document retrieval, intelligent data extraction (LLM & VLM), and automated document generation for radiation shielding plans.

## 🚀 Project Overview

This project was designed to fully automate the processing of technical documents (such as radiation shielding plans for medical LINAC bunkers). It dramatically reduces manual data entry and analysis time by leveraging Vision Language Models (VLM) and Large Language Models (LLM). The entire process is orchestrated through n8n, ensuring smooth transitions between each of the three functional phases.

### 🔄 Phase 1: Automated Retrieval & Aggregation
- **Web Scraping & Navigation:** Utilizes Selenium (`chromedriver`) to automatically log in to specific web portals to retrieve necessary documents.
- **Document Management:** Downloads, validates, and stores technical PDFs securely in the designated directories, ready for downstream processing.
- **RAG Preparation:** Gathers required text and contexts to ensure accurate LLM inferences.

### 🧠 Phase 2: Intelligent Extraction (LLM/VLM)
- **Document Parsing:** Ingests the downloaded PDFs, seamlessly extracting text, tables, and images.
- **Vision-Language Analysis (VLM):** Analyzes technical floor plans in parallel to identify barrier labels, room types, and construction notes.
- **Large Language Model (LLM) Structuring:** Processes text and tables to extract complex radiation physics requirements (e.g., beam energies, workload, shielding thickness).
- **Reporting:** Generates a structured JSON configuration and a professional Markdown executive summary.

### 📝 Phase 3: Automated Formatting & Proposal Generation
- **Form Filling:** Ingests the Phase 2 outputs and automatically populates standardized forms.
- **Excel Tracking:** Updates Excel trackers and reports.
- **Proposal Generation:** Drafts the final, human-readable proposal, saving countless hours of manual transcription.

## 🛠️ Technology Stack
- **Orchestration:** n8n
- **Core Automation:** Python 3.10+
- **Browser Automation:** Selenium / ChromeDriver
- **AI Integration:** LLMs / VLMs for document QA, extraction, and generation
- **Data Handling:** Pandas, JSON, PyPDF (or similar PDF parsers)

## 📁 Repository Structure
```
├── Phase1/
│   ├── RAG/         # RAG resources
│   ├── Tools/       # Automation binaries (e.g., Chromedriver)
│   └── scripts/     # Download and retrieval scripts
├── Phase2/
│   ├── data/        # Input PDFs and resources
│   ├── output/      # Structured JSON and Summaries
│   └── scripts/     # Main extraction scripts (VLM/LLM handling)
├── Phase3/
│   ├── Input/       # Data ingested from Phase 2
│   ├── scripts/     # Excel modification, form filling, and proposal generation
│   └── templates/   # Blank forms and Excel templates
└── .gitignore       # Git ignore file, protecting .env and binaries
```

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/EDM-Agentic-Workflow.git
   cd EDM-Agentic-Workflow
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Navigate into each phase and install the respective requirements:
   ```bash
   pip install -r Phase1/scripts/requirements.txt
   pip install -r Phase2/scripts/requirements.txt
   pip install -r Phase3/scripts/requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root (or specific phase directories as needed) following the structure of a `.env.example` file (which you should create without real credentials):
   ```env
   PP_USERNAME=your_username
   PP_PASSWORD=your_password
   # Add your specific API Keys for LLM/VLM here
   ```
   *Note: Ensure `.env` is never pushed to public repositories.*

## 🤝 Contributing
Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
