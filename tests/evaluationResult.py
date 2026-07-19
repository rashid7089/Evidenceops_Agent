
import json
from pathlib import Path 

def displayRecord(test_id, record_score):
    print(record_score)
    
    print(f"matched_expected_tool: {record_score['matched_expected_tool']} / {record_score['total_expected_tool']}")
    print(f"matched_prohibited_tools: {record_score['matched_prohibited_tools']} / {record_score['total_prohibited_tools']} ")
    print(f"matched_expected_source: {record_score['matched_expected_source']} / {record_score['total_expected_source']}")
    
    total_score = record_score['matched_expected_tool'] + (record_score['total_prohibited_tools']-record_score['matched_prohibited_tools']) + record_score['matched_expected_source']
    max_score = record_score['total_expected_tool'] + record_score['total_prohibited_tools'] + record_score['total_expected_source']
    print("="*80)
    print(f"Total for Test case {test_id}: {total_score} / {max_score} ({total_score/max_score})")


def main():
    with open("tests/EvaluationResult001.json", "r") as file:
        data_from_file = json.load(file)
        for record in data_from_file:
            print("="*80)
            print("*"*80)
            print("="*80)
            print(f"TEST {record['test_number']}. ID: {record['id']}")
            print(f"QUESTION: {record['question']} ")
            print("="*80)
            displayRecord(record['id'], record['evaluation'])
        
if __name__ == "__main__":
    main()