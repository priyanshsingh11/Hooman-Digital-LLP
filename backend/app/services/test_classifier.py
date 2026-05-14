import sys
import os
import json

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.services.classifier import classify_support_email

def run_classification_suite():
    """
    Tests the email classifier with various realistic scenarios.
    """
    test_emails = [
        {
            "id": "REFUND",
            "subject": "Double charged for my subscription",
            "body": "Hi, I noticed two charges on my credit card this morning for the same plan. I only have one account. Please refund the duplicate charge immediately."
        },
        {
            "id": "LOGIN",
            "subject": "Locked out of my account",
            "body": "I've tried resetting my password three times but I never receive the email. I need to access my dashboard for a meeting in 10 minutes. Please help!"
        },
        {
            "id": "SECURITY",
            "subject": "Suspicious activity detected",
            "body": "I just received an alert that someone from Russia logged into my account. This wasn't me. Can you lock my account and check if my data is safe?"
        },
        {
            "id": "ANGRY",
            "subject": "YOUR SERVICE IS TERRIBLE",
            "body": "I have been waiting for 3 days for a response to my ticket! If this isn't fixed today I am cancelling my subscription and telling everyone on Twitter how bad your support is."
        },
        {
            "id": "SPAM",
            "subject": "Exclusive offer for your business!!!",
            "body": "Increase your leads by 1000% with our new AI marketing tool. Click here to claim your discount now: http://spam-link.biz/win"
        }
    ]

    print("=" * 70)
    print("AI CUSTOMER SUPPORT - EMAIL CLASSIFICATION TEST SUITE")
    print("=" * 70)

    for email in test_emails:
        print(f"\n[TEST CASE]: {email['id']}")
        print(f"Subject: {email['subject']}")
        print("-" * 20)
        
        result = classify_support_email(email['subject'], email['body'])
        
        # Clean formatting for terminal output
        print(f"CATEGORY:  {result.get('category', 'N/A').upper()}")
        print(f"URGENCY:   {result.get('urgency', 'N/A').upper()}")
        print(f"SENTIMENT: {result.get('sentiment', 'N/A').upper()}")
        print(f"REASONING: {result.get('reasoning', 'No reasoning provided.')}")
        print("*" * 40)

if __name__ == "__main__":
    try:
        run_classification_suite()
    except Exception as e:
        print(f"CRITICAL ERROR IN TEST SUITE: {e}")
    except KeyboardInterrupt:
        print("\nTesting interrupted.")
