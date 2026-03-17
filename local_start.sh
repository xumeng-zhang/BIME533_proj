# 1. Navigate to project directory
cd /Users/zhangxumeng/Desktop/BIME533_Proj

# 2. Create a virtual environment (if you don't have one)
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the dashboard
cd dashboard
streamlit run app.py