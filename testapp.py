import asyncio
import re
import os
async def test():
    words = input("hello")
    print(words)


if __name__ == "__main__":
    print("main")
    file = ".\\app\\.system\\logs\\last_update_application_files_response.txt"
    if os.path.exists(file):
        print("exists")
    else:
        print("does not exist")
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    # print(text)
    plan = re.search(r'<application_plan>.*?</application_plan>', text, re.DOTALL)
    print(plan.group(0) if plan else "")
    
    updated_files = re.findall(r'<file name="(.*?)">(.*?)</file>', text, re.DOTALL)
    print(updated_files)
    # asyncio.run(test())