import sys
import os
import json

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.workflow.workflow import run_orchestrator

def run_integration_test():
    """
    Simulates the full end-to-end automation pipeline for multiple scenarios.
    """
    test_cases = [
        {
            "name": "Refund Request",
            "subject": "Requesting a refund for last month",
            "body": "Hi, I forgot to cancel my subscription and was charged $49. I haven't logged in at all. Can I get a refund?"
        },
        {
            "name": "Technical Issue",
            "subject": "Dashboard is not loading",
            "body": "Whenever I try to open the analytics page, it just shows a white screen. I've tried clearing my cache but nothing works."
        },
        {
            "name": "Security Concern",
            "subject": "Possible account compromise",
            "body": "I'm seeing login attempts from a city I've never been to. Please secure my account immediately!"
        },
        {
            "name": "Angry Customer (High Urgency)",
            "subject": "SYSTEM IS DOWN AND I AM LOSING MONEY",
            "body": "YOUR APP IS NOT WORKING AND MY ENTIRE TEAM IS BLOCKED. FIX THIS NOW OR I AM SUING!!"
        },
        {
            "name": "Spam",
            "subject": "Increase your SEO rankings for cheap",
            "body": "Hello, we noticed your website is not ranking on Google. For just $99 we can get you to page 1."
        },
        {
            "name": "Feature Request",
            "subject": "Request: Slack Integration",
            "body": "It would be great if we could get notifications in Slack when a new ticket is created."
        }
    ]

    print("=" * 80)
    print("AI SUPPORT ORCHESTRATOR - END-TO-END INTEGRATION TEST")
    print("=" * 80)

    for case in test_cases:
        print(f"\n>>> TESTING SCENARIO: {case['name']}")
        print(f"    Subject: {case['subject']}")
        
        # Execute the full workflow
        result = run_orchestrator(case["subject"], case["body"])
        
        # Display Results
        print("\n--- WORKFLOW RESULTS ---")
        print(f"ACTION:             {result['action'].upper()}")
        print(f"CATEGORY:           {result['classification']['category'].upper()}")
        print(f"URGENCY:            {result['classification']['urgency'].upper()}")
        print(f"SENTIMENT:          {result['classification']['sentiment'].upper()}")
        print(f"WORKFLOW SUMMARY:   {result['workflow_summary']}")
        
        print("\n--- RETRIEVED CONTEXT ---")
        if result["retrieved_docs"]:
            for doc in result["retrieved_docs"]:
                print(f"- Source: {doc['source']}")
                print(f"  Snippet: {doc['content'][:150]}...")
        else:
            print("- No relevant help documents found.")
            
        print("\n" + "#" * 60)

if __name__ == "__main__":
    try:
        run_integration_test()
    except Exception as e:
        print(f"CRITICAL TEST FAILURE: {e}")
    except KeyboardInterrupt:
        print("\nTest cancelled.")
