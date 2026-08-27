import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebFetchTool:
    name = "web_fetch"
    
    description = (
        "Fetch and extract readable text content from a specific web page URL. "
        "Use this when the user wants information from a particular webpage "
        "or when a web search result needs to be inspected in more detail."
    )
    
    parameters = {
        "type" : "object",
        "properties" : {
            "url":{
                "type":"string",
                "description":"The full URL of the webpage to fetch"
            },
        },
        "required" : ["url"]
    }
    
    @staticmethod
    def definition():
        return {
            "type":"function",
            "function":{
                "name":WebFetchTool.name,
                "description":WebFetchTool.description,
                "parameters":WebFetchTool.parameters
            }
        }
    
    @staticmethod
    def execute(url:str):
        try:
            if not url or not url.strip():
                raise ValueError("URL can not be empty")
            prased = urlparse(url)
            
            if prased.scheme not in ("http","https"):
                raise ValueError("URL must be http or https")
            
            response = httpx.get(url,headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                )},
                timeout=15.0,
                follow_redirects=True
            )
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text,"html.parser")
            
            for element in soup([
                "script",
                "style",
                "noscript",
                "svg",
                "nav",
                "footer",
                "header"
            ]):
                element.decompose()
            
            title = (
                soup.title.get_text(" ",strip=True)
                if soup.title
                else ""
            )
            
            text = soup.get_text(
                " ",
                strip=True
            )
            
            text = " ".join(text.split())
            
            return {
                "url":str(response.url),
                "title":title,
                "content":text,
                "length":len(text)
            }
            
        except httpx.TimeoutException:
            raise RuntimeError(
                "Web page fetch timed out."
            )
 
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Web page returned HTTP status "
                f"{e.response.status_code}."
            )

        except httpx.RequestError as e:
            raise RuntimeError(
                f"Web page request failed: {str(e)}"
            )

        except Exception as e:
            print(e)
            raise ValueError(
                f"Web fetch error: {str(e)}"
            )