import asyncio

async def function_one():
    while True:
        print("Function one")
        await asyncio.sleep(0.5)
        
        
async def function_two():
    while True:
        print("Function two")
        await asyncio.sleep(1)
        
async def main():
    tasks = [
        asyncio.create_task(function_one()),
        asyncio.create_task(function_two())
        ]
    await asyncio.gather(*tasks)
    
asyncio.run(main())