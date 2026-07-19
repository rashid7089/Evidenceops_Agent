from app.orchestrator import run_research
import json
import asyncio

from app.agents.research_agent import build_agent

def openJsonFile():
    with open("tests/evaluation_dataset.jsonl", 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]
            


async def evaluate():
    evaluation_dataset = openJsonFile() 
    # keys = evaluation_dataset[0].keys()
    
    # agent = build_agent(approved_to_save=True)
    # response = await agent.run(user_msg=question)
    # tools_used = [tc.tool_name for tc in response.tool_calls]

    # print("="*80)
    
    # print(response)
    # print(dir(response.tool_calls))
    # print("="*80)

    all_scores = []
    for i, evalTest in enumerate(evaluation_dataset):
        if not evalTest['question'].strip():
            continue
        
        print("="*80)
        print("*"*80)
        print("="*80)
        print(f"TEST {i+1}. ID: {evalTest['id']}")
        print(f"QUESTION: {evalTest['question']} ")
        print("="*80)
        
        response = await run_research(evalTest['question'])
        
        print(response.result)
        print("="*80)

        expected_tool = evalTest['expected_tool'] or ""
        prohibited_tools = evalTest['prohibited_tools'] or []
        expected_source = evalTest['expected_source'] or ""

        record_score = {
            "matched_expected_tool":0,
            "total_expected_tool": min(len(expected_tool), 1), # my new method, to give 0 if there no text and 1 if there is text
            "matched_prohibited_tools":0,
            "total_prohibited_tools": len(prohibited_tools),
            "matched_expected_source":0,
            "total_expected_source": min(len(expected_source), 1)
        }

        # expected_tool
        for tool in response.tools_used:
            if tool == expected_tool:
                record_score['matched_expected_tool'] = 1   
                break

        # prohibited_tools
        for tool in prohibited_tools:
            if tool in response.tools_used:
                record_score['matched_prohibited_tools'] += 1

        # expected_source
        for tool_called in response.tool_calls:
            if "sources" in tool_called.keys():
                for source in tool_called['sources']:
                    if source['file_name'] == expected_source:
                        record_score['matched_expected_source'] = 1
        
        print(record_score)
        
        print(f"matched_expected_tool: {record_score['matched_expected_tool']} / {record_score['total_expected_tool']}")
        print(f"matched_prohibited_tools: {record_score['matched_prohibited_tools']} / {record_score['total_prohibited_tools']} ")
        print(f"matched_expected_source: {record_score['matched_expected_source']} / {record_score['total_expected_source']}")
        
        total_score = record_score['matched_expected_tool'] + (record_score['total_prohibited_tools']-record_score['matched_prohibited_tools']) + record_score['matched_expected_source']
        max_score = record_score['total_expected_tool'] + record_score['total_prohibited_tools'] + record_score['total_expected_source']
        print("="*80)
        print(f"Total for Test case {evalTest['id']}: {total_score} / {max_score} ({total_score/max_score})")
        
        all_scores.append(record_score)

    print("="*80)

    return all_scores



        

    

    # expected_tool

    # prohibited_tools

    # print(dir(response))


    # for js in evaluation_dataset[:1]:
    #     response = await run_research(js['question'], approved_to_save=True)
    #     # for k in keys:
    #     #     print(f"{k}: {js[k]}")
    #     print(response.keys())
    #     print("-------")
    #     print(response)
    #     print("----")
    
    

    # current_question = ""
    # response = await run_research(current_question, approved_to_save=True)
    # print(response)



asyncio.run(evaluate())