import boto.mturk.connection as mt_conn
import boto.mturk as mt

import aws_credentials as creds

sandbox = 'mechanicalturk.sandbox.amazonaws.com'
real = 'mechanicalturk.amazonaws.com'
 
mt_conn = mt_conn.MTurkConnection(
          aws_access_key_id = creds.get_aws_access_key("vicky"),
          aws_secret_access_key = creds.get_aws_secret_access_key("vicky"),
          host = sandbox,
          debug = 1 
)

"""
A collection of tools that interact with the MT interface using boto
Will prompt for commands in terminal
"""

def main():
    command = raw_input("Command: ")
    while not command == "exit":
        if command == "upload_external_question":
            upload_external_question()
        else:
            print "No command " + command + " exists"
            
        command = raw_input("Command: ")
    
def upload_external_question():
    url = "https://mono-align-training.herokuapp.com/"
    title = "Monolingual alignment training"
    description = "Select the words in paraphrase that correspond to each other. Completing all \
                    HITs in this project is necessary to gain qualification for a much larger set."
    keywords = ["align", "sentence", "paraphrase", "pairs", "words", "training"]
    reward = raw_input("Reward for this HIT (in dollars)? ")
    max_assignments = raw_input("Number of assignments for this HIT? ")
    frame_height = 900
    
    question = mt.question.ExternalQuestion(url, frame_height)
    
    create_hit_result = mt_conn.create_hit(
        title = title,
        description = description,
        keywords = keywords,
        question = question,
        reward = mt.price.Price(amount = reward),
        max_assignments = max_assignments,
        response_groups = ( 'Minimal', 'HITDetail' ),
    )
    hit = create_hit_result[0]
    
    print "Created HIT, url=", url, "reward=", reward , "hitID=", hit.HITId, "\n"
    
    
if __name__ == "__main__":
    main()