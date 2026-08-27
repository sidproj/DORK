import httpx
from bs4 import BeautifulSoup

class WebSearchTool:
    name = "web_search"
    
    description = (
        "Search the web for information relevant to the user's request. "
        "Returns a list of search results containing titles, URLs, and snippets."
    )
    
    parameters = {
        "type":"object",
        "properties":{
            "query":{
                "type":"string",
                "description":"The search query to search for on the web"
            },
            "max_result":{
                "type":"integer",
                "description":"Maximum number of search results to return",
                "default":3,
            }
        },
        "required":["query"]
    }
    
    @staticmethod
    def definition():
        return {
            "type":"function",
            "function":{
                "name":WebSearchTool.name,
                "description":WebSearchTool.description,
                "parameters":WebSearchTool.parameters
            }
        }
    
    @staticmethod
    def execute(query:str,max_result:int = 3):
        try:
            if not query or not query.strip():
                raise ValueError("Search query can not be empty")
            
            max_results = max(1,min(max_result,10))
            
            url = "https://html.duckduckgo.com/html"
            
            response = httpx.post(
                url,
                data={
                    "q":query,
                },
                headers={
                    "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/131.0 Safari/537.36"
                    )
                },
                timeout=10.0
            )
            
            print(response)
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text,"html.parser")
            
            results = []
            
            for result in soup.select(".result"):
                title_element = result.select_one(".result__title a")
                snippet_element = result.select_one(".result__snippet")
                
                if not title_element:
                    continue
                
                title = title_element.get_text(" ",strip=True)
                result_url = title_element.get("href")
                
                snippet = (
                    snippet_element.get_text(" ",strip=True)
                    if snippet_element
                    else ""
                )
                
                if not result_url:
                    continue
                    
                results.append({
                    "title":title,
                    "url":result_url,
                    "snippet":snippet
                })
                
                if len(results) >= max_results:
                    break

            return {
                "query":query,
                "results":results,
                "count":len(results)
            }
             
        except httpx.TimeoutException:
            raise RuntimeError("Web search timed out.")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Web search fafiled with HTTP status {e.response.status_code}")
        except httpx.RequestError as e:
            raise RuntimeError(f"Web search request failed: {str(e)}")
        except Exception as e:
            print(e)
            raise ValueError(f"Websearch tool error : {str(e)}")