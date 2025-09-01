"# AIMediBuddy" 
🩺 RAG Medical AI Chatbot

This project is a patient-centric AI chatbot built using RAG (Retrieval-Augmented Generation) and the Gemini API.
It allows users (doctors, nurses, or patients) to upload patient medical reports in PDF format and then interact with the chatbot to ask questions directly from the uploaded file.

The frontend is developed with Streamlit, providing a simple and interactive user interface.

🚀 Features
📄 Upload Patient PDF – Supports lab reports, prescriptions, discharge summaries, etc.
🤖 RAG + Gemini API – Extracts medical context and generates accurate answers.
💬 Interactive Q&A – Users can ask about test results, diagnosis, medications, etc.
🖥️ Streamlit UI – Easy-to-use web app for smooth interaction.
🔒 Patient-Centric – Works only on uploaded files, ensuring focused and secure responses.
🛠️ Tech Stack

Frontend: Streamlit
Backend / AI: Gemini API
RAG (Retrieval-Augmented Generation) for contextual responses
Python Libraries: PyPDF2 / pdfplumber (for PDF parsing), Requests, etc.

📂 Project Workflow
Upload PDF → User uploads patient’s medical report.
Extract Data → System parses the text from PDF.
RAG Processing → Gemini API retrieves and generates context-aware answers.
Chat Interface → User asks questions and gets answers from the uploaded file.


🎯 Use Cases
🏥 Doctors → Faster review of patient records
👨‍⚕️ Nurses → Quick insights from medical reports
👩‍🦰 Patients → Easy understanding of their medical files

📌 Future Enhancements
Multi-PDF support
Integration with hospital databases
Voice-based query support
