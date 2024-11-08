#!/usr/bin/env python3

import sys
import email
import html2text
from openai import OpenAI
import os

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def extract_text_from_email(email_content):
    msg = email.message_from_string(email_content)
    from_address = msg.get("To", "Unknown")
    to_address = msg.get("Reply-To") or msg.get("From", "Unknown")
    subject = msg.get("Subject", "No subject")
    subject = f"Re: {subject}"
    in_reply_to = msg.get("Message-ID", "")

    headers = f"From: {from_address}\nTo: {to_address}\nSubject: {subject}\nIn-Reply-To: {in_reply_to}\n"

    body_text = "No Text found"

    for part in msg.walk():
        content_type = part.get_content_type()

        if content_type == "text/html":
            html_content = part.get_payload(decode=True)

            charset = part.get_content_charset() or 'utf-8'
            try:
                html_content = html_content.decode(charset)
            except UnicodeDecodeError:
                html_content = html_content.decode('iso-8859-1', errors='ignore')

            body_text = html2text.html2text(html_content)
            break

        elif content_type == "text/plain":
            plain_text = part.get_payload(decode=True)

            charset = part.get_content_charset() or 'utf-8'
            try:
                plain_text = plain_text.decode(charset)
            except UnicodeDecodeError:
                plain_text = plain_text.decode('iso-8859-1', errors='ignore')

            body_text = plain_text
            break

    return headers, body_text

email_content = sys.stdin.read()
headers, body_text = extract_text_from_email(email_content)

ai_system_message = f"-------> Insert your AI prompt here. Describe in detail what you expect from the response. Provide clear instructions so the reply meets your expectations. The more precise and detailed your description, the more relevant the response will be. Be sure to specify the tone or style you would like the reply to have."


completion = client.chat.completions.create(                                                                    
    model="gpt-4o-mini",                                                                                        
    messages=[                                                                                                  
        {"role": "system", "content": ai_system_message},                                                       
        {"role": "user", "content": body_text}                                                            
    ]                                                                                                           
)                                                                                                               
answer = (completion.choices[0].message.content)    

print(headers)
print(answer)
