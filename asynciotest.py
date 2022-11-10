# import asyncio
# from aiohttp import ClientSession
# import time
# import math

# from functools import wraps
# from asyncio.proactor_events import _ProactorBasePipeTransport

# def silence_event_loop_closed(func):
#     @wraps(func)
    
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except RuntimeError as e:
#             if str(e) != 'Event loop is closed':
#                 raise
#     return wrapper

# _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

# websites = ['https://google.com', 'https://github.com', 'https://m.facebook.com', 'https://twitter.com'];

# async def main(scrapers, news = []):
    
#     start_time = time.time()
#     tasks = []
#     try:
#         async with ClientSession() as session:
#             for website in websites:
#                 task = asyncio.create_task(scrape_website(session, website))
#                 tasks.append(task)
        
#             html_texts = await asyncio.gather(*tasks)
#             print('TIME TAKEN:', math.floor(time.time() - start_time))
            
#             return html_texts
#     except Exception as e:
#         print('the error is ', e)
#         pass
    

# async def scrape_website(session, website):
#     print('making request to', website)
#     async with session.get(website) as response:
#         print('made request to', website)
#         html_text = await response.text()
#         return html_text[:30]
    

# stuff = asyncio.run(main())
# print(len(stuff))