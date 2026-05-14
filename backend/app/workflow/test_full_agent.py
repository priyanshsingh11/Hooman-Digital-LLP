import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.workflow.full_agent import run_support_agent

def run_end_to_end_tests():
    """
    Simulates full end-to-end interactions for different support scenarios.
    """
    test_scenarios = [
        {
            "name": "Refund Query",
            "subject": "Need a refund for my last invoice",
            "body": "I was charged twice yesterday for my monthly subscription. Can you please check and refund one of them?"
        },
        {
            "name": "Technical Troubleshooting",
            "subject": "API is returning 429 errors",
            "body": "I am suddenly getting 429 Too Many Requests errors. I haven't changed my integration code. What are the limits?"
        },
        {
            "name": "Security Alert",
            "subject": "Help! My account was hacked",
            "body": "I received an email saying my password was changed, but I didn't do it. Please lock my account!"
        },
        {
            "name": "Angry Customer",
            "subject": "THIS IS UNACCEPTABLE",
            "body": "Your service has been down for 2 hours. I am losing clients because of this! I want to speak to a manager right now!"
        },
        {
            "name": "Spam / Marketing",
            "subject": "Cheap crypto investment opportunity",
            "body": "Buy our new coin now and 100x your money in a week! Don't miss out."
        }
    ]

    print("=" * 80)
    print("AI SUPPORT AGENT - END-TO-END PRODUCTION TEST SUITE")
    print("=" * 80)

    for scenario in test_scenarios:
        print(f"\n[SCENARIO]: {scenario['name']}")
        print(f"Customer Subject: {scenario['subject']}")
        print("-" * 40)
        
        # Execute the full agent pipeline
        result = run_support_agent(scenario["subject"], scenario["body"])
        
        # Display Core Results
        print(f"ACTION:     {result['action'].upper()}")
        print(f"CATEGORY:   {result['classification']['category'].upper()}")
        print(f"URGENCY:    {result['classification']['urgency'].upper()}")
        
        print("\n--- GENERATED AI RESPONSE ---")
        print(result["generated_response"])
        
        print("\n--- KNOWLEDGE SOURCES USED ---")
        if result["retrieved_docs"]:
            for doc in result["retrieved_docs"]:
                print(f"- {doc['source']}")
        else:
            print("- None (Internal Knowledge Only)")
            
        print("\n" + "#" * 60)

if __name__ == "__main__":
    try:
        run_end_to_end_tests()
    except Exception as e:
        print(f"CRITICAL SYSTEM FAILURE: {e}")
    except KeyboardInterrupt:
        print("\nTesting stopped.")
