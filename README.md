## Project Structure 
- **main.py** : This file contains the main script orchestrating the archiving, comparison, and email sending process. 
- **archiving.py** : An additional file where specific archiving functions can be defined and called from the main script, if necessary. 
- **crawl.log** : This file contains logs generated during the script execution. 
- **requirements.txt** : A file listing all Python dependencies required to run the script.
## Configuration

Before using this script, make sure to install all Python dependencies listed in the `requirements.txt` file.

To configure sending emails, you must complete these fields :

```python

# Sender's email address
SENDER_EMAIL = "your_email@gmail.com"

# Recipient's email address
RECEIVER_EMAIL = "recipient_email@gmail.com"

# Sender's password for the SMTP server
PASSWORD = "your_password"

# SMTP server address
SMTP_SERVER = "smtp.example.com"

# SMTP server port
SMTP_PORT = 587
```



Make sure to replace `"your_email@gmail.com"`, `"recipient_email@gmail.com"`, `"your_password"`, and `"smtp.example.com"` with your actual email credentials and SMTP server address.
## Usage
1. Ensure you have Python installed on your system. 
2. Install dependencies by running `pip install -r requirements.txt`. 
3. Place your Excel file containing the URLs to be archived in the same directory as `main.py`. 
4. Configure the `email_config.py` file as described above.
5. Execute the script using the following command in your terminal:

```bash
python main.py filename.xlsx
```



Make sure to replace `filename.xlsx` with the name of your Excel file containing the URLs.
## Logs

All operations performed by the script will be recorded in the `crawl.log` file, including any errors encountered during execution.
