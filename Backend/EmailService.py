"""
EmailService.py
Email sending service for JARVIS with multiple providers.
"""

import smtplib
import imaplib
import os
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
from email.message import EmailMessage
import email
from typing import Dict, List, Any, Optional
from datetime import datetime
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Also try to load from jarvis_config.env
load_dotenv("jarvis_config.env")

class JarvisEmailService:
    """
    Email sending service with:
    - Multiple email providers support
    - HTML and plain text emails
    - File attachments
    - Email templates
    - Contact management
    """
    
    def __init__(self, data_dir: str = "Data/email"):
        self.data_dir = data_dir
        self.contacts_file = os.path.join(data_dir, "contacts.json")
        self.templates_file = os.path.join(data_dir, "templates.json")
        self.sent_emails_file = os.path.join(data_dir, "sent_emails.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.contacts = self._load_contacts()
        self.templates = self._load_templates()
        self.sent_emails = self._load_sent_emails()
        
        # Email provider configurations
        self.email_providers = {
            'gmail': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'smtp_port_ssl': 465
            },
            'outlook': {
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'smtp_port_ssl': 465
            },
            'yahoo': {
                'smtp_server': 'smtp.mail.yahoo.com',
                'smtp_port': 587,
                'smtp_port_ssl': 465
            },
            'hotmail': {
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'smtp_port_ssl': 465
            }
        }
        
        # Load email configuration from environment
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        # Auto-detect provider if not configured
        if not self.smtp_server and self.email_address:
            self._auto_detect_provider()
    
    def _load_contacts(self) -> Dict[str, Dict[str, str]]:
        """Load contacts from file."""
        try:
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error loading contacts: {e}")
            return {}
    
    def _save_contacts(self):
        """Save contacts to file."""
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(self.contacts, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving contacts: {e}")
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load email templates from file."""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r') as f:
                    return json.load(f)
            return self._get_default_templates()
        except Exception as e:
            print(f"⚠️ Error loading templates: {e}")
            return self._get_default_templates()
    
    def _save_templates(self):
        """Save email templates to file."""
        try:
            with open(self.templates_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving templates: {e}")
    
    def _load_sent_emails(self) -> List[Dict[str, Any]]:
        """Load sent emails history from file."""
        try:
            if os.path.exists(self.sent_emails_file):
                with open(self.sent_emails_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading sent emails: {e}")
            return []
    
    def _save_sent_emails(self):
        """Save sent emails history to file."""
        try:
            with open(self.sent_emails_file, 'w') as f:
                json.dump(self.sent_emails, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving sent emails: {e}")
    
    def _get_default_templates(self) -> Dict[str, Dict[str, str]]:
        """Get default email templates."""
        return {
            'business': {
                'subject': 'Business Inquiry',
                'body': '''Dear {recipient_name},

I hope this email finds you well. I am writing to {purpose}.

{details}

Please let me know if you have any questions or need additional information.

Best regards,
{sender_name}'''
            },
            'meeting': {
                'subject': 'Meeting Request - {topic}',
                'body': '''Hi {recipient_name},

I would like to schedule a meeting to discuss {topic}.

Proposed time: {meeting_time}
Location: {location}

Agenda:
{agenda}

Please let me know if this time works for you or suggest an alternative.

Best regards,
{sender_name}'''
            },
            'follow_up': {
                'subject': 'Follow-up on {topic}',
                'body': '''Hi {recipient_name},

I wanted to follow up on our previous discussion about {topic}.

{follow_up_details}

Please let me know if you need any clarification or have any updates.

Best regards,
{sender_name}'''
            },
            'thank_you': {
                'subject': 'Thank You',
                'body': '''Dear {recipient_name},

Thank you for {reason}.

{additional_message}

I appreciate your time and consideration.

Best regards,
{sender_name}'''
            },
            'apology': {
                'subject': 'Apology',
                'body': '''Dear {recipient_name},

I sincerely apologize for {reason}.

{explanation}

I will ensure this doesn't happen again and would appreciate the opportunity to make it right.

Best regards,
{sender_name}'''
            }
        }
    
    def _auto_detect_provider(self):
        """Auto-detect email provider from email address."""
        if not self.email_address:
            return
        
        domain = self.email_address.split('@')[1].lower()
        
        if 'gmail.com' in domain:
            provider = 'gmail'
        elif 'outlook.com' in domain or 'hotmail.com' in domain:
            provider = 'outlook'
        elif 'yahoo.com' in domain:
            provider = 'yahoo'
        else:
            # Default to Gmail settings
            provider = 'gmail'
        
        config = self.email_providers[provider]
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        
        print(f"✅ Auto-detected email provider: {provider}")
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   html_body: str = None, attachments: List[str] = None,
                   cc_emails: List[str] = None, bcc_emails: List[str] = None) -> str:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            attachments: List of file paths to attach
            cc_emails: CC recipients (optional)
            bcc_emails: BCC recipients (optional)
        """
        try:
            # Check if email is configured
            if not all([self.smtp_server, self.email_address, self.email_password]):
                return """❌ Email not configured. Please set up email credentials:

Required environment variables:
• EMAIL_ADDRESS - Your email address
• EMAIL_PASSWORD - Your email password (or app password)
• SMTP_SERVER - SMTP server (optional, auto-detected)
• SMTP_PORT - SMTP port (optional, default: 587)

For Gmail: Use an App Password instead of your regular password.
For Outlook: Use your regular password or app password.
"""
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add CC and BCC if provided
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)
            
            # Add recipients
            all_recipients = [to_email]
            if cc_emails:
                all_recipients.extend(cc_emails)
            if bcc_emails:
                all_recipients.extend(bcc_emails)
            
            # Add body
            if html_body:
                # Create both plain and HTML versions
                part1 = MIMEText(body, 'plain')
                part2 = MIMEText(html_body, 'html')
                msg.attach(part1)
                msg.attach(part2)
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.send_message(msg, to_addrs=all_recipients)
            
            # Log sent email
            self._log_sent_email(to_email, subject, all_recipients)
            
            return f"✅ Email sent successfully to {to_email}"
            
        except smtplib.SMTPAuthenticationError:
            return "❌ Email authentication failed. Check your email and password."
        except smtplib.SMTPRecipientsRefused:
            return "❌ Recipient email address is invalid or rejected."
        except smtplib.SMTPException as e:
            return f"❌ Email sending failed: {str(e)}"
        except Exception as e:
            return f"❌ Email error: {str(e)}"
    
    def _log_sent_email(self, to_email: str, subject: str, all_recipients: List[str]):
        """Log sent email to history."""
        email_record = {
            'timestamp': datetime.now().isoformat(),
            'to': to_email,
            'subject': subject,
            'recipients': all_recipients
        }
        
        self.sent_emails.append(email_record)
        
        # Keep only last 100 emails
        if len(self.sent_emails) > 100:
            self.sent_emails = self.sent_emails[-100:]
        
        self._save_sent_emails()
    
    def send_template_email(self, template_name: str, to_email: str, **kwargs) -> str:
        """
        Send email using a template.
        
        Args:
            template_name: Name of the template to use
            to_email: Recipient email address
            **kwargs: Template variables
        """
        try:
            if template_name not in self.templates:
                available_templates = ', '.join(self.templates.keys())
                return f"❌ Template '{template_name}' not found. Available templates: {available_templates}"
            
            template = self.templates[template_name]
            subject = template['subject'].format(**kwargs)
            body = template['body'].format(**kwargs)
            
            return self.send_email(to_email, subject, body)
            
        except KeyError as e:
            return f"❌ Missing template variable: {e}"
        except Exception as e:
            return f"❌ Template email error: {str(e)}"
    
    def add_contact(self, name: str, email: str, phone: str = "", company: str = "", notes: str = "") -> str:
        """Add a contact to the address book."""
        try:
            self.contacts[name.lower()] = {
                'name': name,
                'email': email,
                'phone': phone,
                'company': company,
                'notes': notes,
                'added_date': datetime.now().isoformat()
            }
            
            self._save_contacts()
            return f"✅ Added contact: {name} ({email})"
            
        except Exception as e:
            return f"❌ Error adding contact: {str(e)}"
    
    def get_contact(self, name: str) -> str:
        """Get contact information."""
        try:
            contact = self.contacts.get(name.lower())
            if not contact:
                return f"❌ Contact '{name}' not found"
            
            response = f"📇 **Contact: {contact['name']}**\n\n"
            response += f"📧 **Email:** {contact['email']}\n"
            
            if contact['phone']:
                response += f"📞 **Phone:** {contact['phone']}\n"
            
            if contact['company']:
                response += f"🏢 **Company:** {contact['company']}\n"
            
            if contact['notes']:
                response += f"📝 **Notes:** {contact['notes']}\n"
            
            response += f"📅 **Added:** {contact['added_date']}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting contact: {str(e)}"
    
    def list_contacts(self) -> str:
        """List all contacts."""
        try:
            if not self.contacts:
                return "📇 No contacts found. Use 'add contact [name] [email]' to add contacts."
            
            response = "📇 **Contacts**\n\n"
            
            for name, contact in sorted(self.contacts.items()):
                response += f"👤 **{contact['name']}**\n"
                response += f"   📧 {contact['email']}\n"
                if contact['phone']:
                    response += f"   📞 {contact['phone']}\n"
                if contact['company']:
                    response += f"   🏢 {contact['company']}\n"
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing contacts: {str(e)}"
    
    def create_template(self, name: str, subject: str, body: str) -> str:
        """Create a new email template."""
        try:
            self.templates[name] = {
                'subject': subject,
                'body': body,
                'created_date': datetime.now().isoformat()
            }
            
            self._save_templates()
            return f"✅ Created template: {name}"
            
        except Exception as e:
            return f"❌ Error creating template: {str(e)}"
    
    def list_templates(self) -> str:
        """List all email templates."""
        try:
            if not self.templates:
                return "📄 No email templates found."
            
            response = "📄 **Email Templates**\n\n"
            
            for name, template in self.templates.items():
                response += f"📋 **{name}**\n"
                response += f"   Subject: {template['subject']}\n"
                response += f"   Body: {template['body'][:100]}...\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing templates: {str(e)}"
    
    def get_sent_emails(self, limit: int = 10) -> str:
        """Get recently sent emails."""
        try:
            if not self.sent_emails:
                return "📤 No sent emails found."
            
            recent_emails = self.sent_emails[-limit:]
            recent_emails.reverse()  # Show newest first
            
            response = f"📤 **Recently Sent Emails (Last {len(recent_emails)})**\n\n"
            
            for email in recent_emails:
                timestamp = datetime.fromisoformat(email['timestamp'])
                response += f"📧 **{email['subject']}**\n"
                response += f"   To: {email['to']}\n"
                response += f"   Sent: {timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting sent emails: {str(e)}"
    
    def test_email_connection(self) -> str:
        """Test email configuration and connection."""
        try:
            if not all([self.smtp_server, self.email_address, self.email_password]):
                return "❌ Email not configured. Please set up email credentials first."
            
            # Test connection
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
            
            return f"✅ Email connection successful!\n📧 Server: {self.smtp_server}:{self.smtp_port}\n📧 Email: {self.email_address}"
            
        except smtplib.SMTPAuthenticationError:
            return "❌ Authentication failed. Check your email and password."
        except Exception as e:
            return f"❌ Connection test failed: {str(e)}"
    
    def read_emails(self, limit: int = 5, folder: str = "INBOX", unread_only: bool = False) -> str:
        """
        Read emails from inbox.
        
        Args:
            limit: Number of emails to fetch
            folder: Email folder (INBOX, Sent, Drafts, etc.)
            unread_only: Only fetch unread emails
        """
        try:
            if not all([self.email_address, self.email_password]):
                return "❌ Email not configured. Please set up email credentials first."
            
            # Get IMAP server configuration
            imap_server = self._get_imap_server()
            if not imap_server:
                return "❌ IMAP server not configured for your email provider."
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(self.email_address, self.email_password)
            
            # Select folder
            mail.select(folder)
            
            # Search for emails
            if unread_only:
                status, messages = mail.search(None, 'UNSEEN')
            else:
                status, messages = mail.search(None, 'ALL')
            
            if status != 'OK':
                mail.close()
                mail.logout()
                return "❌ Error searching emails."
            
            # Get email IDs
            email_ids = messages[0].split()
            if not email_ids:
                mail.close()
                mail.logout()
                return f"📧 No emails found in {folder}."
            
            # Get recent emails
            recent_ids = email_ids[-limit:] if len(email_ids) >= limit else email_ids
            recent_ids.reverse()  # Show newest first
            
            email_list = []
            for email_id in recent_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        # Extract email details
                        subject = self._decode_header(email_message.get('Subject', 'No Subject'))
                        sender = self._decode_header(email_message.get('From', 'Unknown Sender'))
                        date = email_message.get('Date', 'Unknown Date')
                        
                        # Get email body
                        body = self._extract_email_body(email_message)
                        
                        # Check if read
                        status_flags = mail.fetch(email_id, '(FLAGS)')[1][0].decode()
                        is_read = '\\Seen' in status_flags
                        
                        email_list.append({
                            'subject': subject,
                            'sender': sender,
                            'date': date,
                            'body': body[:200] + "..." if len(body) > 200 else body,
                            'is_read': is_read,
                            'id': email_id.decode()
                        })
                        
                except Exception as e:
                    print(f"⚠️ Error processing email {email_id}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
            # Format response
            response = f"📧 **{folder} Emails** ({len(email_list)} emails)\n\n"
            
            for i, email_data in enumerate(email_list, 1):
                status_icon = "📬" if not email_data['is_read'] else "📭"
                response += f"{status_icon} **{i}. {email_data['subject']}**\n"
                response += f"   📤 From: {email_data['sender']}\n"
                response += f"   📅 Date: {email_data['date']}\n"
                response += f"   📝 Preview: {email_data['body']}\n\n"
            
            return response
            
        except imaplib.IMAP4.error as e:
            return f"❌ IMAP error: {str(e)}"
        except Exception as e:
            return f"❌ Error reading emails: {str(e)}"
    
    def _get_imap_server(self) -> str:
        """Get IMAP server for email provider."""
        if not self.email_address:
            return None
        
        domain = self.email_address.split('@')[1].lower()
        
        if 'gmail.com' in domain:
            return 'imap.gmail.com'
        elif 'outlook.com' in domain or 'hotmail.com' in domain:
            return 'outlook.office365.com'
        elif 'yahoo.com' in domain:
            return 'imap.mail.yahoo.com'
        else:
            # Default to Gmail
            return 'imap.gmail.com'
    
    def _decode_header(self, header: str) -> str:
        """Decode email header."""
        if not header:
            return "No Subject"
        
        decoded_parts = decode_header(header)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    try:
                        decoded_string += part.decode(encoding)
                    except:
                        decoded_string += part.decode('utf-8', errors='ignore')
                else:
                    decoded_string += part.decode('utf-8', errors='ignore')
            else:
                decoded_string += part
        
        return decoded_string
    
    def _extract_email_body(self, email_message) -> str:
        """Extract email body content."""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        continue
        else:
            try:
                body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(email_message.get_payload())
        
        return body.strip()
    
    def get_unread_emails(self, limit: int = 5) -> str:
        """Get unread emails."""
        return self.read_emails(limit=limit, unread_only=True)
    
    def get_latest_emails(self, limit: int = 5) -> str:
        """Get latest emails."""
        return self.read_emails(limit=limit, unread_only=False)
    
    def mark_email_as_read(self, email_id: str) -> str:
        """Mark an email as read."""
        try:
            if not all([self.email_address, self.email_password]):
                return "❌ Email not configured."
            
            imap_server = self._get_imap_server()
            if not imap_server:
                return "❌ IMAP server not configured."
            
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(self.email_address, self.email_password)
            mail.select('INBOX')
            
            mail.store(email_id, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
            return f"✅ Marked email {email_id} as read."
            
        except Exception as e:
            return f"❌ Error marking email as read: {str(e)}"

    def get_email_help(self) -> str:
        """Get help information for email features."""
        return """📧 **Email Service Help**

🔧 **Setup (Required):**
   • Set EMAIL_ADDRESS environment variable
   • Set EMAIL_PASSWORD environment variable
   • SMTP_SERVER and SMTP_PORT (auto-detected for Gmail/Outlook/Yahoo)

📤 **Sending Emails:**
   • 'send email to john@example.com subject Hello body How are you?'
   • 'email sarah@company.com about Meeting scheduled for tomorrow'
   • 'send email to team@work.com with attachment report.pdf'

📥 **Reading Emails:**
   • 'read my emails' - Show latest emails
   • 'unread emails' - Show unread emails only
   • 'check inbox' - Check your inbox
   • 'latest emails 10' - Show latest 10 emails

📋 **Using Templates:**
   • 'send template business to client@company.com recipient_name John purpose discuss project'
   • 'email template meeting to colleague@work.com topic budget meeting_time tomorrow 2pm'

👥 **Contact Management:**
   • 'add contact John Smith john@example.com 555-1234 Company Inc'
   • 'get contact John Smith'
   • 'list contacts'
   • 'send email to contact John Smith subject Hello'

📄 **Template Management:**
   • 'create template follow_up subject Follow-up on {topic} body Hi {name}...'
   • 'list templates'
   • 'send template follow_up to client@work.com topic proposal name Sarah'

📊 **Email History:**
   • 'sent emails' - Show recently sent emails
   • 'test email' - Test email configuration

💡 **Examples:**
   • 'read my emails' - Check your inbox
   • 'unread emails' - Show unread messages
   • 'send email to manager@company.com subject Weekly Report body Here is this week's report'
   • 'email template thank_you to client@work.com reason your time additional_message for the great meeting'
   • 'add contact Jane Doe jane@company.com 555-5678 Acme Corp Great client'
"""
