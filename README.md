# Django QR Code Generator

A fully interactive QR code generator built using *Django*, featuring customizable colors, optional logo upload, user authentication, and live preview functionality.

---

## 🚀 Features

* Generate high-quality QR codes instantly
* Foreground & background color picker
* Optional logo/image embedding
* Live client-side QR preview
* User login & signup system
* Saves QR codes to user account
* Download generated QR codes
* Responsive and clean UI

---

## 🛠 Tech Stack

* *Python 3*
* *Django*
* *SQLite*
* *qrcode (Python library)*
* *Pillow (image processing)*
* *HTML, CSS, JavaScript*
* *Bootstrap/Tailwind (optional)*

---

## 📦 Installation

### 1. Clone the repository


git clone https://github.com/Flashyfury/QRcodegenerator.git
cd QRcodegenerator


### 2. Create a virtual environment


python -m venv venv
.\venv\Scripts\activate   # Windows


### 3. Install all dependencies


pip install -r requirements.txt


### 4. Apply migrations


python manage.py makemigrations
python manage.py migrate


### 5. Start the development server


python manage.py runserver


Now visit:


http://127.0.0.1:8000/


---

## 🔧 Usage

* Enter text/URL to encode
* Choose foreground & background colors
* Upload a logo (optional)
* Preview updates instantly
* Save or download the generated QR code
* Logged-in users can manage all generated QR codes

---

## 🔮 Future Enhancements

* Export QR codes as SVG
* Multiple QR styles and patterns
* Advanced logo placement options
* User analytics dashboard
* Bulk QR code generation

---

## 📄 License

This project is open-source. You are free to modify, use, or extend it.
